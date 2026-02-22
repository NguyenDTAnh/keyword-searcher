
"""Script thu thập & phân loại từ khóa cho một destination.

CÁCH DÙNG:
  1) Copy file này, đổi tên theo destination, ví dụ: collect_danang.py
  2) Fill phần `DESTINATION = DestinationConfig(...)` ở đầu file.
  3) Đặt data vào đúng thư mục: data/google_search_console, data/seo_insider, data/google_trend
  4) Chạy: python .clinerules/skills/keyword-searcher/scripts/collect_keywords.py

OUTPUT:
  - File CSV trung gian: reports/[destination]-raw.csv (100 keywords đã xử lý)
  - File CSV này sẽ được format_report.py (keyword-validator) đọc để tạo Report Final.

Yêu cầu quan trọng (giữ nguyên spec keyword-planner.md):
  1) Chuẩn hoá Taxonomy (Cluster Type) trước khi gom cụm – không gom cảm tính.
  2) Chuẩn hoá Geo Scope (In-scope / Out-of-scope / Geo Ambiguous) – không trộn tỉnh.
  3) Nhóm A: ưu tiên dữ liệu GSC (Clicks/Impressions/CTR/Position) – không tự estimate số liệu thiếu.
  4) Nhóm B: cơ hội mở rộng từ SEO Insider + Google Trend (lọc travel intent).
  5) Phân bổ intent tổng 100 keyword theo tỉ lệ 20/40/40.
  6) Bắt buộc ghi rõ Source Folder/File cho từng dòng.
"""

import csv
import glob
import os
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  DESTINATION CONFIG — CHỈ CẦN THAY ĐỔI PHẦN NÀY CHO MỖI DESTINATION      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝


@dataclass
class DestinationConfig:
    """Cấu hình destination-specific. User chỉ cần fill dataclass này."""

    # --- Thông tin cơ bản ---
    name: str
    """Tên hiển thị chính thức. Ví dụ: 'Đà Nẵng', 'Phú Quốc', 'Hà Nội'."""

    slug: str
    """Slug cho filename output. Ví dụ: 'danang', 'phuquoc', 'hanoi'."""

    name_variants: list[str] = field(default_factory=list)
    """Các biến thể tên destination (bao gồm cả không dấu) để detect in-scope.
    Ví dụ cho Đà Nẵng: ['đà nẵng', 'da nang', 'danang']
    Ví dụ cho Phú Quốc: ['phú quốc', 'phu quoc', 'phuquoc']
    """

    # --- Địa lý đặc hữu ---
    entities: list[str] = field(default_factory=list)
    """Các entity đặc hữu (địa danh nổi tiếng) — keyword không cần chứa tên destination
    vẫn được coi là in-scope nếu chứa entity này.
    Ví dụ cho Đà Nẵng: ['cầu rồng', 'bà nà hills', 'bán đảo sơn trà', 'ngũ hành sơn', ...]
    """

    districts: list[str] = field(default_factory=list)
    """Các quận/huyện thuộc destination.
    Ví dụ cho Đà Nẵng: ['hải châu', 'thanh khê', 'liên chiểu', 'sơn trà', 'ngũ hành sơn', ...]
    """

    # --- Landmark & Taxonomy ---
    landmark_keywords: list[str] = field(default_factory=list)
    """Các từ khoá để detect cluster type = 'Địa danh tham quan / Văn hóa - Lịch sử'.
    Sử dụng dạng không dấu (normalized) vì logic match đã strip accent.
    Ví dụ cho Đà Nẵng: ['cau rong', 'ba na', 'ngu hanh son', 'son tra', 'linh ung', ...]
    """

    # --- Cluster Rules ---
    cluster_rules: dict[str, list[dict[str, str]]] = field(default_factory=dict)
    """Rules mapping cho cluster_name() theo cluster_type.
    Format: {cluster_type: [{"pattern": regex_str, "name": display_name}, ...]}

    Mỗi rule được check theo thứ tự, rule đầu tiên match sẽ thắng.
    Nếu không rule nào match → fallback "{Cluster Type mặc định} {destination_name}".

    Ví dụ cho Đà Nẵng:
    {
        "Địa danh tham quan / Văn hóa - Lịch sử": [
            {"pattern": r"(cau rong|dragon bridge)", "name": "Cầu Rồng"},
            {"pattern": r"(ba na|bana)", "name": "Bà Nà Hills"},
            {"pattern": r"(ngu hanh son)", "name": "Ngũ Hành Sơn"},
        ],
        "Lưu trú": [
            {"pattern": r"(my khe|mi khe)", "name": "Khách sạn gần Mỹ Khê"},
            {"pattern": r"(\\b4 sao\\b|4 sao)", "name": "Khách sạn 4 sao Đà Nẵng"},
            {"pattern": r"(\\b5 sao\\b|5 sao)", "name": "Khách sạn 5 sao Đà Nẵng"},
        ],
        "Di chuyển": [
            {"pattern": r"(san bay|airport)", "name": "Sân bay Đà Nẵng & di chuyển"},
            {"pattern": r"\\btour\\b", "name": "Tour Đà Nẵng"},
        ],
        "Ẩm thực (F&B)": [
            {"pattern": r"(banh trang|bánh tráng)", "name": "Bánh tráng cuốn thịt heo"},
            {"pattern": r"(mi quang|mì quảng)", "name": "Mì Quảng Đà Nẵng"},
            {"pattern": r"(hai san|hải sản)", "name": "Hải sản Đà Nẵng"},
        ],
    }
    """

    province_display_overrides: dict[str, str] = field(default_factory=dict)
    """Override tên hiển thị cho các tỉnh out-of-scope (dạng normalized -> display name).
    Khi 1 keyword chứa tên tỉnh khác, script tự title() nhưng có thể sai dấu.
    Dùng dict này để fix.
    Ví dụ: {"phu quoc": "Phú Quốc", "da lat": "Đà Lạt", "da nang": "Đà Nẵng", ...}
    """

    # --- Travel-ish detection (tuỳ chọn mở rộng) ---
    extra_travel_patterns: str = ""
    """Regex pattern bổ sung cho is_travelish(). Nối thêm vào pattern mặc định.
    Ví dụ: r"|bien|bãi biển|lan|diving|snorkeling" (cho destination biển).
    Để trống nếu pattern mặc định đã đủ.
    """


# ┌──────────────────────────────────────────────────────────────────────────────┐
# │  ⬇️  FILL CONFIG CHO DESTINATION CỦA BẠN TẠI ĐÂY  ⬇️                       │
# └──────────────────────────────────────────────────────────────────────────────┘

DESTINATION = DestinationConfig(
    name="Đà Nẵng",            
    slug="da-nang",                        

    name_variants=[
        "đà nẵng", "da nang", "danang"
    ],

    entities=[
        "cầu rồng", "cau rong",
        "bà nà hills", "ba na hills", "bà nà", "ba na",
        "bán đảo sơn trà", "ban dao son tra", "sơn trà", "son tra",
        "ngũ hành sơn", "ngu hanh son",
        "chùa linh ứng", "chua linh ung", "linh ứng", "linh ung",
        "đèo hải vân", "deo hai van",
        "mỹ khê", "my khe",
        "chợ cồn", "cho con",
        "chợ hàn", "cho han",
        "asia park", "công viên châu á", "cong vien chau a"
    ],

    districts=[
        "hải châu", "thanh khê", "liên chiểu", "sơn trà", "ngũ hành sơn", "cẩm lệ", "hòa vang", "hoàng sa"
    ],

    landmark_keywords=[
        "cau rong", "ba na", "son tra", "ngu hanh son", "linh ung", "deo hai van", 
        "cho con", "cho han", "asia park", "cong vien chau a", "ban dao"
    ],

    cluster_rules={
        "Địa danh tham quan / Văn hóa - Lịch sử": [
            {"pattern": r"(cau rong)", "name": "Cầu Rồng"},
            {"pattern": r"(ba na)", "name": "Bà Nà Hills"},
            {"pattern": r"(ngu hanh son)", "name": "Ngũ Hành Sơn"},
            {"pattern": r"(son tra)", "name": "Bán đảo Sơn Trà"},
            {"pattern": r"(linh ung)", "name": "Chùa Linh Ứng"},
            {"pattern": r"(deo hai van)", "name": "Đèo Hải Vân"},
            {"pattern": r"(cho con|cho han)", "name": "Chợ Cồn/Hàn"},
            {"pattern": r"(asia park|cong vien chau a)", "name": "Asia Park"},
        ],
        "Lưu trú": [
            {"pattern": r"(my khe|mi khe)", "name": "Khách sạn gần Mỹ Khê"},
            {"pattern": r"(resort)", "name": "Resort Đà Nẵng"},
            {"pattern": r"(\b4 sao\b|4 sao)", "name": "Khách sạn 4 sao Đà Nẵng"},
            {"pattern": r"(\b5 sao\b|5 sao)", "name": "Khách sạn 5 sao Đà Nẵng"},
            {"pattern": r"(homestay)", "name": "Homestay Đà Nẵng"},
            {"pattern": r"(khach san|hotel)", "name": "Khách sạn Đà Nẵng"},
        ],
        "Di chuyển": [
            {"pattern": r"(san bay|airport)", "name": "Sân bay Đà Nẵng"},
            {"pattern": r"(ve may bay|may bay)", "name": "Vé máy bay đi Đà Nẵng"},
            {"pattern": r"(thue xe may|xe may)", "name": "Thuê xe máy Đà Nẵng"},
            {"pattern": r"(xe khach|limousine|giuong nam)", "name": "Xe khách đi Đà Nẵng"},
            {"pattern": r"\btour\b", "name": "Tour Đà Nẵng"},
        ],
        "Ẩm thực (F&B)": [
            {"pattern": r"(banh trang|bánh tráng)", "name": "Bánh tráng cuốn thịt heo"},
            {"pattern": r"(mi quang|mì quảng)", "name": "Mì Quảng Đà Nẵng"},
            {"pattern": r"(hai san|hải sản)", "name": "Hải sản Đà Nẵng"},
            {"pattern": r"(bun cha ca|bún chả cá)", "name": "Bún chả cá Đà Nẵng"},
            {"pattern": r"(quan an|nha hang)", "name": "Quán ăn ngon Đà Nẵng"},
        ],
    },

    province_display_overrides={
        "da nang": "Đà Nẵng",
    },

    extra_travel_patterns="|bien|bãi biển|lan|diving|snorkeling",
)


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PHẦN DƯỚI ĐÂY KHÔNG CẦN CHỈNH SỬA (trừ khi muốn custom logic)           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝


# =====================
# Derived config
# =====================


def find_repo_root(start_dir: str) -> str:
    """Tìm repo root một cách "trâu bò" để script chạy ổn dù file nằm ở đâu.

    Tiêu chí: folder có đủ `data/` và `reports/`.
    """
    cur = os.path.abspath(start_dir)
    while True:
        if os.path.isdir(os.path.join(cur, "data")) and os.path.isdir(os.path.join(cur, "reports")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            # Không tìm thấy, fallback về CWD hiện tại
            return os.path.abspath(os.getcwd())
        cur = parent


WORKDIR = find_repo_root(os.path.dirname(__file__))

GSC_QUERIES_PATH = os.path.join(WORKDIR, "data", "google_search_console", "Queries.csv")
SEO_INSIDER_PATH = os.path.join(WORKDIR, "data", "seo_insider", "advance_search_report.csv")
TRENDS_DIR = os.path.join(WORKDIR, "data", "google_trend")
GOOGLE_PLANNER_DIR = os.path.join(WORKDIR, "data", "google_planner")
WEB_SUGGEST_DIR = os.path.join(WORKDIR, "data", "web_suggest")

# Output CSV trung gian — format_report.py sẽ đọc file này
OUTPUT_CSV = os.path.join(WORKDIR, "data", "raw", f"{DESTINATION.slug}-raw.csv")


# Danh sách tỉnh/thành để detect out-of-scope.
# NOTE: List khá đầy đủ để giảm "lọt tỉnh". Phần exclude destination hiện tại tự động.
PROVINCES = [
    "an giang",
    "bà rịa - vũng tàu",
    "bạc liêu",
    "bắc giang",
    "bắc kạn",
    "bắc ninh",
    "bến tre",
    "bình định",
    "bình dương",
    "bình phước",
    "bình thuận",
    "cà mau",
    "cần thơ",
    "cao bằng",
    "đà nẵng",
    "đắk lắk",
    "đắk nông",
    "điện biên",
    "đồng nai",
    "đồng tháp",
    "gia lai",
    "hà giang",
    "hà nam",
    "hà nội",
    "hà tĩnh",
    "hải dương",
    "hải phòng",
    "hậu giang",
    "hòa bình",
    "hưng yên",
    "khánh hòa",
    "kiên giang",
    "kon tum",
    "lai châu",
    "lâm đồng",
    "lạng sơn",
    "lào cai",
    "long an",
    "nam định",
    "nghệ an",
    "ninh bình",
    "ninh thuận",
    "phú thọ",
    "phú yên",
    "quảng bình",
    "quảng nam",
    "quảng ngãi",
    "quảng ninh",
    "quảng trị",
    "sóc trăng",
    "sơn la",
    "tây ninh",
    "thái bình",
    "thái nguyên",
    "thanh hóa",
    "thừa thiên huế",
    "tiền giang",
    "tp hồ chí minh",
    "trà vinh",
    "tuyên quang",
    "vĩnh long",
    "vĩnh phúc",
    "yên bái",
    # Thêm các biến thể phổ biến (không dấu + viết liền)
    "phú quốc",
    "tam đảo",
    "sầm sơn",
    "đồng văn",
    "sa pa",
    "sapa",
    "đà lạt",
    "huế",
    "hue",
    "nha trang",
    "vũng tàu",
    "vung tau",
    "quy nhơn",
    "quy nhon",
    "hạ long",
    "ha long",
    "sài gòn",
    "sai gon",
    "saigon",
    "hồ chí minh",
    "ho chi minh",
    "tphcm",
    "tp hcm",
    "quận 1",
    "quan 1",
    "quận 3",
    "quan 3",
]

# Tự động build set các normalized variant của destination để exclude khỏi PROVINCES
_DESTINATION_NORM_VARIANTS = {norm_text for v in DESTINATION.name_variants for norm_text in [v]}


# =====================
# Helpers: normalize / parsing
# =====================


def strip_accents(text: str) -> str:
    """Bỏ dấu để match địa danh ổn định hơn."""
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return unicodedata.normalize("NFC", text)


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", strip_accents(text).lower()).strip()


def kw_contains(kw_norm: str, phrase: str) -> bool:
    """Match theo word-ish boundary để tránh match bậy kiểu 'langbiang' dính 'lang'."""
    p = re.escape(norm(phrase))
    return re.search(rf"(^|\W){p}(\W|$)", kw_norm) is not None


def is_travelish(kw_norm: str) -> bool:
    """Kiểm tra keyword có liên quan travel hay không."""
    base_pattern = (
        r"(du lich|check in|dia diem|choi gi|kinh nghiem|lich trinh"
        r"|khach san|hotel|resort|homestay|hostel|villa"
        r"|tour|dat |booking|thue xe|xe |limousine|taxi|san bay|bus|tau|may bay"
        r"|an|quan an|nha hang|buffet|bun |ca phe|coffee)"
    )
    # Nối thêm extra_travel_patterns từ config (nếu có)
    extra = DESTINATION.extra_travel_patterns.strip()
    if extra:
        # User truyền dạng "|pattern1|pattern2" hoặc "pattern1|pattern2" đều OK
        if not extra.startswith("|"):
            extra = "|" + extra
        pattern = base_pattern[:-1] + extra + ")"
    else:
        pattern = base_pattern

    return re.search(pattern, kw_norm) is not None


# Danh sách các thuật ngữ liên quan đến nước ngoài/nội địa để lọc
FOREIGN_TERMS = [
    "thai lan", "thailand", "han quoc", "korea", "nhat ban", "japan", "trung quoc", "china",
    "singapore", "malaysia", "campuchia", "cambodia", "lao", "laos", "myanmar",
    "chau au", "europe", "my", "usa", "duc", "germany", "phap", "france", "anh", "uk",
    "uc", "australia", "dai loan", "taiwan", "hong kong", "macau",
    "nuoc ngoai", "quoc te", "nga", "russia", "thuy sy", "italy", "italia", "ha lan", "philippines"
]

def is_foreign_related(kw_n: str) -> bool:
    """Kiểm tra keyword có liên quan đến tour nước ngoài hay không."""
    # Chỉ lọc nếu có chữ "tour" hoặc "du lich" đi kèm với tên nước ngoài
    # để tránh lọc nhầm các entity có tên trùng (hiếm gặp nhưng an toàn hơn)
    if not re.search(r"(tour|du lich|ve may bay|ve tau)", kw_n):
        return False
        
    for term in FOREIGN_TERMS:
        if kw_contains(kw_n, term):
            return True
    return False



def has_destination_token(keyword: str) -> bool:
    """Kiểm tra keyword có chứa token destination (name variants, districts, entities) hay không."""
    kw_n = norm(keyword)

    # Check name variants
    for variant in DESTINATION.name_variants:
        if kw_contains(kw_n, variant):
            return True

    # Check districts
    for d in DESTINATION.districts:
        if kw_contains(kw_n, d):
            return True

    # Check entities
    for e in DESTINATION.entities:
        if kw_contains(kw_n, e):
            return True

    return False


def is_destination_related(keyword: str, geo_label: str) -> bool:
    """Cho phép keyword out-of-scope nếu có liên kết rõ ràng với destination.

    Ví dụ hợp lệ:
    - "xe limousine đà nẵng hội an" => Out-of-scope Hội An nhưng gắn Đà Nẵng (origin)
    - "tour đà nẵng - huế 1 ngày" => Out-of-scope Huế nhưng gắn Đà Nẵng
    """
    if geo_label == f"In-scope {DESTINATION.name}":
        return True
    if geo_label.startswith("Out-of-scope"):
        return has_destination_token(keyword)
    # Geo ambiguous: chỉ giữ nếu có token destination
    return has_destination_token(keyword)


# =====================
# Taxonomy & Geo
# =====================


def _is_destination_variant(province_norm: str) -> bool:
    """Check xem 1 province string (normalized) có phải là variant của destination hay không.
    Dùng để exclude destination hiện tại ra khỏi PROVINCES check.
    """
    for v in DESTINATION.name_variants:
        if norm(v) == norm(province_norm):
            return True
    return False


def geo_scope(keyword: str):
    """Trả về (Geo Scope label, cluster_for_out_of_scope)

    - In-scope {destination}: có token destination / quận / entity.
    - Out-of-scope: chứa tên tỉnh/thành khác => gom về '[Tỉnh/Thành] Trip'.
    - Mơ hồ: Geo Ambiguous.
    """
    kw_n = norm(keyword)

    # 1) In-scope: entity đặc hữu (Ưu tiên entity để catch "Lăng Bác Hồ", "TT Hội nghị Quốc gia"...)
    # Tránh bị "out-of-scope" oan nếu entity chứa tên tỉnh khác (dù hiếm).
    for e in DESTINATION.entities:
        if kw_contains(kw_n, e):
            return (f"In-scope {DESTINATION.name}", DESTINATION.name)

    # 2) Out-of-scope: detect tỉnh/thành khác (ưu tiên bắt trước name generic)
    for prov in PROVINCES:
        # Skip nếu province là chính destination hiện tại
        if _is_destination_variant(prov):
            continue
        if kw_contains(kw_n, prov):
            # Chuẩn hoá tên hiển thị
            prov_norm = norm(prov)
            # Check override từ config trước
            prov_display = DESTINATION.province_display_overrides.get(prov_norm)
            if not prov_display:
                prov_display = prov.title().replace("Tp ", "TP ")
            return (f"Out-of-scope {prov_display}", f"{prov_display} Trip")

    # 3) In-scope: name variants
    for v in DESTINATION.name_variants:
        if kw_contains(kw_n, v):
            return (f"In-scope {DESTINATION.name}", DESTINATION.name)

    # 4) In-scope: quận/huyện
    for d in DESTINATION.districts:
        if kw_contains(kw_n, d):
            return (f"In-scope {DESTINATION.name}", DESTINATION.name)

    return ("Geo Ambiguous", "Geo Ambiguous")


def cluster_type(keyword: str) -> str:
    """Chuẩn hóa loại thực thể.

    RULE CỨNG: Landmark/văn hoá-lịch sử phải bắt trước F&B.
    """
    kw_n = norm(keyword)

    # 1) Lưu trú (ưu tiên cao nhất)
    if re.search(r"(khach san|hotel|resort|homestay|hostel|nha nghi|villa|apartment|can ho)", kw_n):
        return "Lưu trú"

    # 2) Di chuyển
    if re.search(
        r"(tour|taxi|xe |limousine|thue xe|bus|tau|may bay|san bay|airport|di chuyen|dua don)",
        kw_n,
    ):
        return "Di chuyển"

    # 3) F&B
    # NOTE: Phân biệt "phở" (food) vs "phố" (street). Bỏ dấu cả 2 đều thành 'pho'.
    raw = (keyword or "").lower().strip()
    pho_is_food = (
        re.search(r"\bphở\b", raw) is not None
        or re.search(r"\bpho\s+(bo|ga|cuon|tai|nam|dap|tron)\b", kw_n) is not None
    )

    if (
        re.search(r"\bbun\b", kw_n)
        or pho_is_food
        or re.search(
            r"(cha |banh |buffet|quan an|nha hang|an dem|cafe|ca phe|coffee|dac san|an uong)",
            kw_n,
        )
        is not None
    ):
        return "Ẩm thực (F&B)"

    # 4) Landmark/VH-LS — build regex từ config
    if DESTINATION.landmark_keywords:
        landmark_pattern = "|".join(re.escape(lk) for lk in DESTINATION.landmark_keywords)
        # Thêm generic landmark keywords (chùa, đền, bảo tàng, di tích, ...)
        landmark_pattern += r"|chua|den|bao tang|di tich"
        if re.search(rf"({landmark_pattern})", kw_n):
            return "Địa danh tham quan / Văn hóa - Lịch sử"
    else:
        # Fallback: chỉ dùng generic landmark keywords
        if re.search(r"(chua|den|bao tang|di tich)", kw_n):
            return "Địa danh tham quan / Văn hóa - Lịch sử"

    return "Tổng hợp"


def cluster_name(keyword: str, ctype: str, geo_label: str, out_cluster: str) -> str:
    """Gán tên cluster dựa trên cluster_rules từ config.

    Logic: Duyệt rules theo cluster_type, rule đầu tiên match thắng.
    Fallback: "{Tên mặc định} {DESTINATION.name}" hoặc out_cluster / Geo Ambiguous.
    """
    kw_n = norm(keyword)

    # Out-of-scope => dùng cluster out-of-scope (vd: "Đà Lạt Trip")
    if geo_label.startswith("Out-of-scope"):
        return out_cluster
    if geo_label == "Geo Ambiguous":
        return "Geo Ambiguous"

    # In-scope => check rules từ config
    rules = DESTINATION.cluster_rules.get(ctype, [])
    for rule in rules:
        if re.search(rule["pattern"], kw_n):
            return rule["name"]

    # Fallback theo cluster_type
    fallback_map = {
        "Địa danh tham quan / Văn hóa - Lịch sử": f"Điểm tham quan {DESTINATION.name}",
        "Lưu trú": f"Khách sạn {DESTINATION.name}",
        "Di chuyển": f"Di chuyển {DESTINATION.name}",
        "Ẩm thực (F&B)": f"Ăn uống {DESTINATION.name}",
        "Tổng hợp": f"Tổng hợp {DESTINATION.name}",
    }
    return fallback_map.get(ctype, f"Tổng hợp {DESTINATION.name}")


# =====================
# Data models
# =====================

# Các cột CSV output — format_report.py sẽ đọc đúng theo thứ tự này
CSV_COLUMNS = [
    "keyword", "cluster", "cluster_type", "geo_scope", "intent",
    "vol", "imp", "clicks", "ctr", "kd_comp",
    "source", "action_plan", "group", "score",
    "yoy", "bid_high",
]


@dataclass
class KeywordRow:
    keyword: str
    cluster: str
    cluster_type: str
    geo_scope: str
    intent: str
    vol: str
    imp: str
    clicks: str
    ctr: str
    kd_comp: str
    source: str
    action_plan: str
    group: str
    score: float
    yoy: str = "N/A"
    bid_high: str = "N/A"


def map_intent_from_seo_insider(main_intent: str) -> str | None:
    mi = (main_intent or "").strip().lower()
    if mi in ("transactional", "transaction"):
        return "Transaction"
    if mi in ("commercial", "commercial investigation"):
        return "Commercial Investigation"
    if mi in ("informational", "information"):
        return "Informational"
    # navigational: gần với commercial investigation
    if mi in ("navigational",):
        return "Commercial Investigation"
    # Unknown/empty => để heuristic tự quyết
    return None


def resolve_intent(keyword: str, ctype: str, seo_main_intent: str | None) -> str:
    """Resolve intent cuối cùng, kết hợp SEO Insider + heuristic.

    Ưu tiên:
    - SEO nói Transaction → tin luôn
    - Heuristic phát hiện Transaction cho Lưu trú/Di chuyển → ưu tiên Transaction
    - SEO nói Informational nhưng heuristic khác → dùng heuristic
    """
    seo_intent = map_intent_from_seo_insider(seo_main_intent)
    inferred = infer_intent(keyword)

    # Không có dữ liệu SEO intent => dùng heuristic
    if seo_intent is None:
        return inferred

    # SEO nói Transaction thì tin luôn
    if seo_intent == "Transaction":
        return "Transaction"

    # Heuristic phát hiện Transaction cho Lưu trú/Di chuyển => ưu tiên Transaction
    if inferred == "Transaction" and ctype in ("Lưu trú", "Di chuyển"):
        return "Transaction"

    # SEO nói Informational nhưng heuristic có tín hiệu rõ khác intent => dùng heuristic
    if seo_intent == "Informational" and inferred != "Informational":
        return inferred

    return seo_intent


def infer_intent(keyword: str) -> str:
    """Heuristic phân loại intent dựa trên keyword patterns."""
    kw_n = norm(keyword)

    # ===== Signals =====
    # Transaction: ý định mua/đặt rõ ràng
    trans_sig = re.search(
        r"(\bgia\b|\bdat\b|booking|mua|\bthue\b|voucher|combo|deal|khuyen mai)",
        kw_n,
    )

    # Một số cụm từ dù không có 'giá/đặt' vẫn mang ý định giao dịch
    trans_by_phrase = re.search(
        r"(ve may bay|vé máy bay|ve tau|vé tàu|ve xe|vé xe|dua don|đưa đón)",
        kw_n,
    )

    # Commercial investigation: so sánh/chọn lựa
    comm_sig = re.search(
        r"(review|top|tot nhat|tốt nhất|so sanh|so sánh|kinh nghiem|kinh nghiệm|nen di|nên đi|list|nen o|nên ở)",
        kw_n,
    )

    is_stay = re.search(r"(khach san|hotel|resort|homestay|hostel|nha nghi|villa|apartment|can ho)", kw_n)
    is_move = re.search(
        r"(may bay|san bay|airport|taxi|limousine|thue xe|xe |bus|tau|di chuyen|di lai|dua don|\btour\b|\bve\b)",
        kw_n,
    )
    is_landmark = bool(DESTINATION.landmark_keywords) and re.search(
        "|".join(re.escape(lk) for lk in DESTINATION.landmark_keywords)
        + r"|chua|den|bao tang|di tich",
        kw_n,
    )
    is_fb = re.search(r"(bun|pho|phở|quan an|nha hang|buffet|cafe|ca phe|coffee|dac san|an uong)", kw_n)

    # ===== Category-first rules (để dễ cân 20/40/40) =====
    if is_stay:
        if trans_sig:
            return "Transaction"
        if comm_sig:
            return "Commercial Investigation"
        return "Commercial Investigation"

    if is_move:
        if trans_sig or trans_by_phrase:
            return "Transaction"
        if comm_sig:
            return "Commercial Investigation"
        if re.search(r"(taxi|limousine|thue xe|dua don)", kw_n):
            return "Transaction"
        if re.search(r"\btour\b", kw_n):
            if re.search(r"(\b\d+\s*(ngay|dem)\b|1 ngay|2 ngay|3 ngay)", kw_n):
                return "Transaction"
            return "Commercial Investigation"
        return "Commercial Investigation"

    if is_landmark:
        if trans_sig:
            return "Transaction"
        if comm_sig:
            return "Commercial Investigation"
        return "Informational"

    if is_fb:
        if trans_sig:
            return "Transaction"
        if comm_sig:
            return "Commercial Investigation"
        return "Informational"

    # fallback
    if trans_sig:
        return "Transaction"
    if comm_sig:
        return "Commercial Investigation"
    return "Informational"


def _has_comm_sig(kw_n: str) -> bool:
    return (
        re.search(
            r"(review|top|tot nhat|tốt nhất|so sanh|so sánh|kinh nghiem|kinh nghiệm|nen di|nên đi|list|nen o|nên ở)",
            kw_n,
        )
        is not None
    )


def _is_soft_transaction_candidate(row: KeywordRow) -> bool:
    """Keyword không có signal Transaction rõ, nhưng có thể promote từ CI -> Transaction
    để cân ratio 20/40/40 mà vẫn hợp lý với hành vi tìm kiếm du lịch.
    """
    if row.intent != "Commercial Investigation":
        return False
    if row.cluster_type not in ("Lưu trú", "Di chuyển"):
        return False

    kw_n = norm(row.keyword)
    if _has_comm_sig(kw_n):
        return False

    # Các query di chuyển kiểu đặt dịch vụ
    if row.cluster_type == "Di chuyển":
        if re.search(r"(taxi|limousine|thue xe|dua don)", kw_n):
            return True
        if re.search(r"\btour\b", kw_n) and re.search(r"(\b\d+\s*(ngay|dem)\b|1 ngay|2 ngay|3 ngay)", kw_n):
            return True
        return False

    # Lưu trú: query dạng "khách sạn ..." thường có intent booking implicit
    if row.cluster_type == "Lưu trú":
        return True

    return False


def kd_bucket(kd: int | None) -> str:
    if kd is None:
        return "N/A"
    if kd < 30:
        return "Low"
    if kd < 60:
        return "Medium"
    return "High"


def action_plan_for(row: KeywordRow) -> str:
    """Gợi ý hành động cụ thể theo nhóm + intent + cluster_type.
    Dùng DESTINATION.name thay vì hardcode.
    """
    dest = DESTINATION.name

    if row.group == "A":
        if row.intent == "Transaction":
            return f"Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub '{dest}'"
        if row.intent == "Commercial Investigation":
            return "Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR"
        return "Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3"

    # Nhóm B: cơ hội mới
    if row.intent == "Transaction":
        return "Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ"
    if row.intent == "Commercial Investigation":
        return "Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC"
    return "Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ"


# =====================
# Loaders
# =====================


def load_gsc_queries(path: str):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            kw = (row.get("Top queries") or "").strip()
            if not kw:
                continue
            try:
                clicks = int(float(row.get("Clicks") or 0))
                imp = int(float(row.get("Impressions") or 0))
                ctr = float((row.get("CTR") or "0").replace("%", ""))
                pos = float(row.get("Position") or 0)
            except Exception:
                continue
            rows.append(
                {
                    "keyword": kw,
                    "clicks": clicks,
                    "imp": imp,
                    "ctr": ctr,
                    "pos": pos,
                    "source": f"data/google_search_console/{os.path.basename(path)}",
                }
            )
    return rows


def load_seo_insider(path: str):
    data = {}
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            kw = (row.get("keyword") or "").strip()
            if not kw:
                continue
            try:
                vol = (
                    int(float(row.get("search_volume") or 0))
                    if row.get("search_volume") not in (None, "", "--")
                    else None
                )
            except Exception:
                vol = None
            try:
                kd = (
                    int(float(row.get("difficulty") or 0))
                    if row.get("difficulty") not in (None, "", "--")
                    else None
                )
            except Exception:
                kd = None

            data[norm(kw)] = {
                "keyword": kw,
                "vol": vol,
                "kd": kd,
                "main_intent": row.get("main_intent"),
                "source": f"data/seo_insider/{os.path.basename(path)}",
            }
    return data


def load_trends(dir_path: str):
    """Gộp trend theo keyword: lấy max search interest và "increase" đáng chú ý nhất."""
    agg = {}
    for path in glob.glob(os.path.join(dir_path, "*.csv")):
        with open(path, newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            if not r.fieldnames or "query" not in r.fieldnames:
                continue
            for row in r:
                q = (row.get("query") or "").strip()
                if not q:
                    continue
                qn = norm(q)
                si_raw = (row.get("search interest") or "").strip()
                inc_raw = (row.get("increase percent") or "").strip()

                try:
                    si = int(si_raw) if si_raw.isdigit() else None
                except Exception:
                    si = None

                cur = agg.get(qn)
                if not cur:
                    agg[qn] = {
                        "keyword": q,
                        "max_interest": si,
                        "increase": inc_raw,
                        "sources": {f"data/google_trend/{os.path.basename(path)}"},
                    }
                else:
                    cur["sources"].add(f"data/google_trend/{os.path.basename(path)}")
                    if si is not None and (cur["max_interest"] is None or si > cur["max_interest"]):
                        cur["max_interest"] = si
                    # Ưu tiên breakout
                    if cur["increase"] != "Breakout" and inc_raw == "Breakout":
                        cur["increase"] = "Breakout"

    return agg


def load_google_planner(dir_path: str):
    """Load keyword từ Google Keyword Planner (folder theo destination)."""
    data = {}
    if not os.path.exists(dir_path):
        return data

    def _parse_planner_int(val: str) -> int:
        """Parse volume kiểu Planner: "1,000", "1000", "1K", "1K – 10K".
        Không tự áng chừng số liệu ngoài pattern này.
        """
        if val is None:
            return 0
        s = str(val).strip()
        if not s or s in ("--", "N/A"):
            return 0
        # Range dạng "1K – 10K" (en dash) hoặc "1K - 10K"
        if "–" in s or "-" in s:
            parts = re.split(r"\s*[–-]\s*", s)
            parts = [p for p in parts if p.strip()]
            if len(parts) >= 1:
                return _parse_planner_int(parts[0])
        # Suffix K/M
        m = re.match(r"^([0-9]+(?:[\.,][0-9]+)?)\s*([kKmM])$", s)
        if m:
            num = float(m.group(1).replace(",", "."))
            mul = 1000 if m.group(2).lower() == "k" else 1_000_000
            return int(num * mul)
        # Plain integer with separators
        s2 = re.sub(r"[^0-9]", "", s)
        return int(s2) if s2.isdigit() else 0

    for path in glob.glob(os.path.join(dir_path, "*.csv")):
        with open(path, newline="", encoding="utf-16") as f: # Planner usually UTF-16 LE
            try:
                # Skip first line if it's metadata (common in Planner exports)
                # But CSV DictReader might handle if headers are clear.
                # Often Planner exports have 2 header lines or title.
                # Let's try reading safely.
                content = f.read()
            except UnicodeError:
                # Try utf-8 if utf-16 fails
                with open(path, newline="", encoding="utf-8") as f2:
                    content = f2.read()

        # Fix malformed lines or skip metadata
        lines = content.splitlines()
        start_line = 0
        for i, line in enumerate(lines):
            # Check for multiple columns to distinguish header from title "Keyword Stats..."
            if (("Keyword" in line or "Keyword phrase" in line) 
                and ("Avg. monthly searches" in line 
                     or "Average monthly searches" in line 
                     or "Currency" in line
                     or "Số lần tìm kiếm" in line)):
                start_line = i
                break
        
        reader = csv.DictReader(lines[start_line:], delimiter='\t') # Planner often tab-separated or comma
        if not reader.fieldnames or ("Keyword" not in reader.fieldnames and "Keyword phrase" not in reader.fieldnames):
             reader = csv.DictReader(lines[start_line:], delimiter=',')
        
        for row in reader:
            kw = row.get("Keyword") or row.get("Keyword phrase")
            if not kw:
                continue
            kw = kw.strip()
            
            # Parse Volume
            vol_str = (
                row.get("Avg. monthly searches")
                or row.get("Average monthly searches")
                or row.get("Số lần tìm kiếm trung bình hàng tháng")
                or "0"
            )
            vol = _parse_planner_int(vol_str)
                
            # Parse Competition
            comp = row.get("Competition") # Low/Medium/High
            comp_idx = row.get("Competition (indexed value)")
            
            # Parse YoY Change
            yoy_raw = (
                row.get("YoY change")
                or row.get("Year-over-year change")
                or row.get("Thay đổi so với cùng kỳ năm trước")
                or "0%"
            )
            yoy = 0.0
            try:
                if yoy_raw and yoy_raw != "--":
                    yoy = float(yoy_raw.replace("%", "").replace("+", "").strip())
            except Exception:
                yoy = 0.0

            # Parse Top of page bid (high range)
            bid_high_raw = (
                row.get("Top of page bid (high range)")
                or row.get("Giá thầu đầu trang (khoảng cao)")
                or "0"
            )
            bid_high = 0.0
            try:
                if bid_high_raw and bid_high_raw != "--":
                    # Remove currency symbols and separators (comma, dot depending on locale)
                    # Simple heuristic: remove non-digit chars except dot/comma?
                    # Better: keep digits, dot, comma. 
                    # Assuming standard numeric format 1,000.00 or 1.000,00
                    # Let's just remove non-digits to be safe if it is an integer currency like VND, 
                    # but for USD it might be decimal. 
                    # Chấp nhận rủi ro đơn giản hóa: remove non-digitchars
                    # Nhưng nếu là 0.50 thì sao? -> 050 -> 50. Sai.
                    # Cách an toàn hơn: Extract số đầu tiên tìm thấy.
                    clean_str = re.sub(r"[^0-9\.,]", "", bid_high_raw)
                    if "," in clean_str and "." in clean_str:
                         # 1,234.56 or 1.234,56
                         if clean_str.find(",") < clean_str.find("."):
                             clean_str = clean_str.replace(",", "")
                         else:
                             clean_str = clean_str.replace(".", "").replace(",", ".")
                    elif "," in clean_str:
                         # 1,234 or 1,23 -> assume comma is thousand separator if collected is mainly huge numbers? 
                         # Or decimal? Google Planner CSV usually follows account locale.
                         # Safe bet: just treat comma/dot as separators if they appear once?
                         # Let's try simple float parsing after replacing comma with dot if comma is decimal separator
                         clean_str = clean_str.replace(",", "") # Assume comma is thousands separator usually
                    
                    bid_high = float(clean_str)
            except Exception:
                bid_high = 0.0

            data[norm(kw)] = {
                "keyword": kw,
                "vol": vol,
                "competition": comp,
                "competition_index": comp_idx,
                "yoy": yoy,
                "bid_high": bid_high,
                "source": f"data/google_planner/{os.path.basename(dir_path)}/{os.path.basename(path)}"
            }
    return data


def load_web_suggest(path: str):
    """Load keyword bổ sung từ web search (tự thu thập khi data nội bộ thiếu)."""
    data = {}
    if not os.path.exists(path):
        return data

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            kw = (row.get("keyword") or row.get("Keyword") or "").strip()
            if not kw:
                continue
            
            data[norm(kw)] = {
                "keyword": kw,
                "vol": row.get("vol") or row.get("volume") or "N/A",
                "source": f"web ({os.path.basename(path)})"
            }
    return data


# =====================
# Build candidates
# =====================


def build_candidates():
    seo = load_seo_insider(SEO_INSIDER_PATH)
    trends = load_trends(TRENDS_DIR)
    gsc_rows = load_gsc_queries(GSC_QUERIES_PATH)
    
    # Load Google Planner for this destination
    planner_path = os.path.join(GOOGLE_PLANNER_DIR, DESTINATION.slug)
    planner_data = load_google_planner(planner_path)

    candidates: dict[str, KeywordRow] = {}

    # Group A: từ GSC (giữ cả out-of-scope nhưng phải tách cluster đúng tỉnh)
    for r in gsc_rows:
        kw = r["keyword"]
        kw_n = norm(kw)

        geo, out_cluster = geo_scope(kw)
        if not is_destination_related(kw, geo):
            continue

        ctype = cluster_type(kw)

        # Loại rác "tổng hợp" không phải du lịch
        if ctype == "Tổng hợp" and not is_travelish(kw_n):
            continue
        if kw_n in ("vietgoing",):
            continue
        
        # Lọc bỏ từ khoá nhạy cảm/không phù hợp (tình yêu, tình nhân)
        if re.search(r"(tinh yeu|tinh nhan)", kw_n):
            continue


        cluster = cluster_name(kw, ctype, geo, out_cluster)

        seo_row = seo.get(kw_n)
        vol = str(seo_row["vol"]) if (seo_row and seo_row["vol"] is not None) else "N/A"
        kd = seo_row["kd"] if seo_row else None
        kd_text = f"{kd_bucket(kd)} ({kd if kd is not None else 'N/A'})"

        # Intent: resolve giữa SEO insider main_intent và heuristic
        intent = resolve_intent(kw, ctype, seo_row.get("main_intent") if seo_row else None)

        # SPI = Clicks trực tiếp từ dữ liệu GSC
        spi_val = float(r["clicks"])

        row = KeywordRow(
            keyword=kw.lower(),
            cluster=cluster,
            cluster_type=ctype,
            geo_scope=geo,
            intent=intent,
            vol=vol,
            imp=str(r["imp"]),
            clicks=str(r["clicks"]),
            ctr=f"{r['ctr']}%",
            kd_comp=kd_text,
            source=r["source"],
            action_plan="",
            group="A",
            score=spi_val,
            yoy="N/A",
            bid_high="N/A",
        )
        row.action_plan = action_plan_for(row)
        candidates[kw_n] = row

    # Group B1: từ SEO Insider (opportunity) – lọc travelish, KD thấp, volume đủ
    for kw_n, s in seo.items():
        if kw_n in candidates:
            continue
        kw = s["keyword"]

        geo, out_cluster = geo_scope(kw)
        if not is_destination_related(kw, geo):
            continue

        ctype = cluster_type(kw)
        cluster = cluster_name(kw, ctype, geo, out_cluster)

        # Filter: phải liên quan du lịch
        if ctype == "Tổng hợp" and not is_travelish(kw_n):
            continue

        vol = s["vol"]
        kd = s["kd"]
        if vol is None or vol < 500:
            continue
        if kd is not None and kd >= 60:
            continue

        # Lọc bỏ từ khoá nhạy cảm/không phù hợp (tình yêu, tình nhân)
        if re.search(r"(tinh yeu|tinh nhan)", kw_n):
            continue

        intent = resolve_intent(kw, ctype, s.get("main_intent"))


        kd_text = f"{kd_bucket(kd)} ({kd if kd is not None else 'N/A'})"

        score = float(vol) * (1.0 if kd is None else (1.0 - min(kd, 80) / 100.0))

        row = KeywordRow(
            keyword=kw.lower(),
            cluster=cluster,
            cluster_type=ctype,
            geo_scope=geo,
            intent=intent,
            vol=str(vol),
            imp="N/A",
            clicks="N/A",
            ctr="N/A",
            kd_comp=kd_text,
            source=s["source"],
            action_plan="",
            group="B",
            score=score,
            yoy="N/A",
            bid_high="N/A",
        )
        row.action_plan = action_plan_for(row)
        candidates[kw_n] = row

    # Group B2: từ Google Trend – lọc travelish + destination-ish
    for kw_n, t in trends.items():
        if kw_n in candidates:
            continue

        kw = t["keyword"]
        geo, out_cluster = geo_scope(kw)
        if not is_destination_related(kw, geo):
            continue

        if not is_travelish(kw_n):
            continue

        # Lọc tour nước ngoài (nguồn Trends)
        if is_foreign_related(kw_n):
            continue

        ctype = cluster_type(kw)
        cluster = cluster_name(kw, ctype, geo, out_cluster)

        inc = t.get("increase") or ""
        si = t.get("max_interest")
        kd_text = f"Trend {('SI:'+str(si)) if si is not None else ''} {inc}".strip()

        intent = infer_intent(kw)

        # Ưu tiên khách sạn/resort: tăng score
        score = float(si or 0)
        if ctype == "Lưu trú":
            score *= 1.5

        row = KeywordRow(
            keyword=kw.lower(),
            cluster=cluster,
            cluster_type=ctype,
            geo_scope=geo,
            intent=intent,
            vol="N/A",
            imp="N/A",
            clicks="N/A",
            ctr="N/A",
            kd_comp=kd_text,
            source="; ".join(sorted(t["sources"])),
            action_plan="",
            group="B",
            score=score,
            yoy=t.get("increase", "N/A"),
            bid_high="N/A",
        )
        row.action_plan = action_plan_for(row)
        candidates[kw_n] = row

    # Group B3: Từ Google Planner (bổ sung)
    for kw_n, p in planner_data.items():
        if kw_n in candidates:
            continue
            
        kw = p["keyword"]
        geo, out_cluster = geo_scope(kw)
        if not is_destination_related(kw, geo):
            continue

        # Filter: phải liên quan du lịch (tương tự SEO insider)
        ctype = cluster_type(kw)
        if ctype == "Tổng hợp" and not is_travelish(kw_n):
            continue

        # Lọc tour nước ngoài (nguồn Planner)
        if is_foreign_related(kw_n):
            continue

        cluster = cluster_name(kw, ctype, geo, out_cluster)
        
        vol = p["vol"]
        if vol < 20: # Filter low volume noise
            continue
            
        # Lọc bỏ từ khoá nhạy cảm/không phù hợp (tình yêu, tình nhân)
        if re.search(r"(tinh yeu|tinh nhan)", kw_n):
            continue

        intent = resolve_intent(kw, ctype, None)

        
        kd_text = f"Planner ({p['competition'] or 'N/A'})"
        
        # Scoring Logic: Volume High + Comp Low/Medium -> YoY + Bid High
        # 1. Base: Volume
        base_score = float(vol)
        
        # 2. Competition Factor (Ưu tiên Low/Medium)
        comp_val = (p["competition"] or "").lower()
        if comp_val == "low":
            comp_factor = 1.5
        elif comp_val == "medium":
            comp_factor = 1.2
        elif comp_val == "high":
            comp_factor = 0.8
        else:
            comp_factor = 1.0
            
        # 3. Bonus Factor (YoY > 0, Bid High > 0)
        bonus_multiplier = 1.0
        
        # YoY tăng trưởng -> là trend -> ưu tiên
        if p["yoy"] > 0:
            bonus_multiplier += 0.2
            
        # Bid High cao -> Transactional intent cao -> ưu tiên
        # (Ngưỡng bid check tương đối > 0 là được bonus nhẹ)
        if p["bid_high"] > 0:
            bonus_multiplier += 0.1
            
        score = base_score * comp_factor * bonus_multiplier
        
        # Ưu tiên khách sạn/resort
        if ctype == "Lưu trú":
            score *= 1.5

        row = KeywordRow(
            keyword=kw.lower(),
            cluster=cluster,
            cluster_type=ctype,
            geo_scope=geo,
            intent=intent,
            vol=str(vol),
            imp="N/A",
            clicks="N/A",
            ctr="N/A",
            kd_comp=kd_text,
            source=p["source"],
            action_plan="",
            group="B",
            score=score,
            yoy=f"{p.get('yoy', 0.0):.1f}%" if p.get('yoy') else "0%",
            bid_high=f"{p.get('bid_high', 0.0):,.0f}" if p.get('bid_high') else "0",
        )
        row.action_plan = action_plan_for(row)
        candidates[kw_n] = row

    # Group B4: Từ Web Suggest (bổ sung cuối cùng nếu vẫn thiếu)
    web_suggest_path = os.path.join(WEB_SUGGEST_DIR, f"{DESTINATION.slug}.csv")
    web_data = load_web_suggest(web_suggest_path)
    for kw_n, w in web_data.items():
        if kw_n in candidates:
            continue
            
        kw = w["keyword"]
        geo, out_cluster = geo_scope(kw)
        if not is_destination_related(kw, geo):
            continue

        ctype = cluster_type(kw)
        if ctype == "Tổng hợp" and not is_travelish(kw_n):
            continue

        # Lọc tour nước ngoài (nguồn Web)
        if is_foreign_related(kw_n):
            continue

        cluster = cluster_name(kw, ctype, geo, out_cluster)
        
        intent = resolve_intent(kw, ctype, None)

        # Ưu tiên khách sạn/resort
        score = 5.0
        if ctype == "Lưu trú":
            score = 10.0 # Tăng nhẹ để nổi bật hơn web suggest khác

        row = KeywordRow(
            keyword=kw.lower(),
            cluster=cluster,
            cluster_type=ctype,
            geo_scope=geo,
            intent=intent,
            vol=str(w["vol"]),
            imp="N/A",
            clicks="N/A",
            ctr="N/A",
            kd_comp="N/A (web)",
            source=w["source"],
            action_plan="",
            group="B",
            score=score,
            yoy="N/A",
            bid_high="N/A",
        )
        row.action_plan = action_plan_for(row)
        candidates[kw_n] = row

    return list(candidates.values())


# =====================
# Selection logic (100 keywords, intent 20/40/40)
# =====================


def select_keywords(candidates: list[KeywordRow], total: int = 100):
    # Ưu tiên Group A trước, sau đó Group B.
    buckets = defaultdict(list)
    for c in candidates:
        buckets[c.intent].append(c)

    # Sort inside intent by group and score
    for intent, arr in buckets.items():
        arr.sort(key=lambda x: (0 if x.group == "A" else 1, -x.score))

    targets = {
        "Informational": int(total * 0.2),
        "Commercial Investigation": int(total * 0.4),
        "Transaction": total - int(total * 0.2) - int(total * 0.4),
    }

    def promote(row: KeywordRow, new_intent: str) -> KeywordRow:
        """Clone row và override intent + action_plan để output đúng bucket."""
        r2 = KeywordRow(**{**row.__dict__})
        r2.intent = new_intent
        r2.action_plan = action_plan_for(r2)
        return r2

    def take(intent: str, target: int):
        """Lấy keyword từ bucket theo thứ tự ưu tiên, bỏ qua duplicate."""
        for row in buckets.get(intent, []):
            if sum(1 for r in selected if r.intent == intent) >= target:
                break
            kn = norm(row.keyword)
            if kn in used:
                continue
            selected.append(row)
            used.add(kn)

    selected: list[KeywordRow] = []
    used = set()

    # 1) Informational: lấy strict đủ 20
    take("Informational", targets["Informational"])

    # 2) Transaction: lấy strict trước, thiếu thì promote từ CI (soft transaction)
    trans_target = targets["Transaction"]
    take("Transaction", trans_target)

    if sum(1 for r in selected if r.intent == "Transaction") < trans_target:
        need = trans_target - sum(1 for r in selected if r.intent == "Transaction")
        ci_pool = buckets.get("Commercial Investigation", [])
        soft = [r for r in ci_pool if norm(r.keyword) not in used and _is_soft_transaction_candidate(r)]
        soft.sort(key=lambda x: (0 if x.group == "A" else 1, -x.score))
        for row in soft[:need]:
            kn = norm(row.keyword)
            if kn in used:
                continue
            selected.append(promote(row, "Transaction"))
            used.add(kn)

    # 3) Commercial Investigation: lấy phần còn lại cho đủ target
    take("Commercial Investigation", targets["Commercial Investigation"])

    # Fill remaining (nếu thiếu do pool ít): lấy best overall
    if len(selected) < total:
        rest = [c for c in candidates if norm(c.keyword) not in used]
        rest.sort(key=lambda x: (0 if x.group == "A" else 1, -x.score))
        for row in rest:
            if len(selected) >= total:
                break
            selected.append(row)
            used.add(norm(row.keyword))

    # Sắp xếp theo Cluster (alpha), rồi Group A trước.
    selected.sort(key=lambda x: (x.cluster.lower(), 0 if x.group == "A" else 1, -x.score))
    return selected[:total]


# =====================
# CSV Export
# =====================


def export_csv(rows: list[KeywordRow]):
    """Xuất 100 keywords đã xử lý ra file CSV trung gian cho format_report.py."""
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for r in rows:
            writer.writerow({
                "keyword": r.keyword,
                "cluster": r.cluster,
                "cluster_type": r.cluster_type,
                "geo_scope": r.geo_scope,
                "intent": r.intent,
                "vol": r.vol,
                "imp": r.imp,
                "clicks": r.clicks,
                "ctr": r.ctr,
                "kd_comp": r.kd_comp,
                "source": r.source,
                "action_plan": r.action_plan,
                "group": r.group,
                "score": r.score,
                "yoy": r.yoy,
                "bid_high": r.bid_high,
            })


def main():
    # Validate config trước khi chạy
    if not DESTINATION.name or DESTINATION.name.startswith("<"):
        print("❌ ERROR: Chưa fill DestinationConfig! Mở file và thay đổi phần DESTINATION = DestinationConfig(...).")
        return

    if not DESTINATION.name_variants:
        print("⚠️  WARNING: name_variants trống. Script sẽ không detect được in-scope keywords.")

    candidates = build_candidates()
    selected = select_keywords(candidates, total=100)
    export_csv(selected)

    print(f"✅ Exported: {OUTPUT_CSV}")
    print(f"   Candidates: {len(candidates)} | Selected: {len(selected)}")
    print(f"\n👉 Bước tiếp: Chạy format_report.py để tạo Report Final.")
    print(f"   python .clinerules/skills/keyword-validator/scripts/format_report.py")


if __name__ == "__main__":
    main()
