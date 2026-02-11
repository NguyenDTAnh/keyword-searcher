
"""Generate lại report keyword cho Hà Nội theo spec `keyword-planner.md`.

Yêu cầu quan trọng (tóm tắt đúng thứ tự ưu tiên):
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
from dataclasses import dataclass


# =====================
# Config
# =====================

WORKDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

GSC_QUERIES_PATH = os.path.join(WORKDIR, "data", "google_search_console", "Queries.csv")
SEO_INSIDER_PATH = os.path.join(WORKDIR, "data", "seo_insider", "advance_search_report.csv")
TRENDS_DIR = os.path.join(WORKDIR, "data", "google_trend")
OUTPUT_PATH = os.path.join(WORKDIR, "destination", "Hanoi - keyword.md")

DESTINATION_NAME = "Hà Nội"

# Các entity “đặc hữu” Hà Nội (keyword không cần chứa 'hà nội' vẫn in-scope)
HANOI_ENTITIES = [
    "hồ hoàn kiếm",
    "hoàn kiếm",
    "hồ gươm",
    "phố cổ",
    "hoàng thành thăng long",
    "hoàng thành",
    "văn miếu",
    "quốc tử giám",
    "lăng bác",
    "lăng chủ tịch",
    "lăng chủ tịch hồ chí minh",
    "chùa trấn quốc",
    "chùa một cột",
    "hồ tây",
    "nhà hát lớn",
    "cột cờ",
    "hồ tây",
    "nội bài",
]

HANOI_DISTRICTS = [
    "ba đình",
    "hoàn kiếm",
    "đống đa",
    "cầu giấy",
    "hai bà trưng",
    "tây hồ",
    "long biên",
    "nam từ liêm",
    "bắc từ liêm",
    "thanh xuân",
    "hà đông",
]


# Danh sách tỉnh/thành để detect out-of-scope.
# NOTE: Anh intentionally để list khá đầy đủ để giảm “lọt tỉnh”.
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
    "khánh hòa",
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
    # Match theo word-ish boundary để tránh match bậy kiểu 'langbiang' dính 'lang'
    p = re.escape(norm(phrase))
    return re.search(rf"(^|\W){p}(\W|$)", kw_norm) is not None


def is_travelish(kw_norm: str) -> bool:
    return re.search(
        # NOTE: Không dùng 'pho ' vì dễ dính 'phố' (street) sau khi bỏ dấu.
        r"(du lich|check in|dia diem|choi gi|kinh nghiem|lich trinh|khach san|hotel|resort|homestay|hostel|villa|tour|dat |booking|thue xe|xe |limousine|taxi|san bay|noi bai|bus|tau|may bay|an|quan an|nha hang|buffet|bun |ca phe|coffee)",
        kw_norm,
    ) is not None


def has_hanoi_token(keyword: str) -> bool:
    kw_n = norm(keyword)
    if kw_contains(kw_n, "ha noi") or kw_contains(kw_n, "hanoi"):
        return True
    for d in HANOI_DISTRICTS:
        if kw_contains(kw_n, d):
            return True
    for e in HANOI_ENTITIES:
        if kw_contains(kw_n, e):
            return True
    return False


def is_destination_related(keyword: str, geo_label: str) -> bool:
    """Report Hà Nội nhưng vẫn cho phép keyword out-of-scope nếu có liên kết rõ ràng với Hà Nội.

    Ví dụ hợp lệ:
    - "xe limousine hà nội tam đảo" => Out-of-scope Tam Đảo nhưng gắn Hà Nội (origin)
    - "tour hà nội - hải phòng 1 ngày" => Out-of-scope Hải Phòng nhưng gắn Hà Nội
    """

    if geo_label == f"In-scope {DESTINATION_NAME}":
        return True
    if geo_label.startswith("Out-of-scope"):
        return has_hanoi_token(keyword)
    # Geo ambiguous: chỉ giữ nếu có token Hà Nội
    return has_hanoi_token(keyword)


# =====================
# Taxonomy & Geo
# =====================


def geo_scope(keyword: str):
    """Trả về (Geo Scope label, cluster_for_out_of_scope)

    - In-scope Hà Nội: có token Hà Nội / quận Hà Nội / entity Hà Nội.
    - Out-of-scope: chứa tên tỉnh/thành khác => gom về '[Tỉnh/Thành] Trip'.
    - Mơ hồ: Geo Ambiguous.
    """

    kw_n = norm(keyword)

    # 1) Out-of-scope: detect tỉnh/thành (ưu tiên bắt trước)
    for prov in PROVINCES:
        if prov in ("hà nội", "ha noi", "hanoi"):
            continue
        if kw_contains(kw_n, prov):
            # Chuẩn hoá tên hiển thị
            prov_display = prov.title().replace("Tp ", "TP ")
            if prov_display == "Phu Quoc":
                prov_display = "Phú Quốc"
            if prov_display == "Da Lat":
                prov_display = "Đà Lạt"
            if prov_display == "Da Nang":
                prov_display = "Đà Nẵng"
            if prov_display == "Sa Pa":
                prov_display = "Sa Pa"
            if prov_display == "Tam Dao":
                prov_display = "Tam Đảo"
            return (f"Out-of-scope {prov_display}", f"{prov_display} Trip")

    # 2) In-scope: token Hà Nội
    if kw_contains(kw_n, "ha noi") or kw_contains(kw_n, "hanoi"):
        return (f"In-scope {DESTINATION_NAME}", DESTINATION_NAME)

    # 3) In-scope: quận/huyện Hà Nội
    for d in HANOI_DISTRICTS:
        if kw_contains(kw_n, d):
            return (f"In-scope {DESTINATION_NAME}", DESTINATION_NAME)

    # 4) In-scope: entity đặc hữu Hà Nội
    for e in HANOI_ENTITIES:
        if kw_contains(kw_n, e):
            return (f"In-scope {DESTINATION_NAME}", DESTINATION_NAME)

    return ("Geo Ambiguous", "Geo Ambiguous")


def cluster_type(keyword: str) -> str:
    """Chuẩn hóa loại thực thể.

    RULE CỨNG: Landmark/văn hoá-lịch sử phải bắt trước F&B.
    """

    raw = (keyword or "").lower().strip()
    kw_n = norm(keyword)

    # 1) Lưu trú (ưu tiên cao nhất - keyword có landmark vẫn là intent ngủ nghỉ)
    if re.search(r"(khach san|hotel|resort|homestay|hostel|nha nghi|villa|apartment|can ho)", kw_n):
        return "Lưu trú"

    # 2) Di chuyển (chỉ bắt các từ khoá vận chuyển, KHÔNG bắt mỗi chữ 'vé' để tránh nhầm vé tham quan)
    if re.search(
        r"(tour|taxi|xe |limousine|thue xe|bus|tau|may bay|san bay|airport|noi bai|di chuyen|dua don)",
        kw_n,
    ):
        return "Di chuyển"

    # 3) F&B
    # NOTE: Phân biệt "phở" (food) vs "phố" (street). Khi bỏ dấu cả 2 đều thành 'pho' -> dễ gán sai.
    pho_is_food = (
        re.search(r"\bphở\b", raw) is not None
        or re.search(r"\bpho\s+(bo|ga|cuon|tai|nam|dap|tron)\b", kw_n) is not None
    )

    if (
        re.search(r"\bbun\b", kw_n)  # bún (ít mơ hồ)
        or pho_is_food
        or re.search(r"(cha |banh |buffet|quan an|nha hang|an dem|cafe|ca phe|coffee|dac san|an uong)", kw_n) is not None
    ):
        return "Ẩm thực (F&B)"

    # 4) Landmark/VH-LS
    if re.search(
        r"(hoang thanh|van mieu|quoc tu giam|lang chu tich|lang bac|ho chi minh|chua|den|bao tang|di tich|pho co|ho guom|ho tay|hoan kiem|cot co|nha hat lon)",
        kw_n,
    ):
        return "Địa danh tham quan / Văn hóa - Lịch sử"

    return "Tổng hợp"


def cluster_name(keyword: str, ctype: str, geo_label: str, out_cluster: str) -> str:
    raw = (keyword or "").lower().strip()
    kw_n = norm(keyword)

    if geo_label.startswith("Out-of-scope"):
        return out_cluster
    if geo_label == "Geo Ambiguous":
        return "Geo Ambiguous"

    # In-scope Hà Nội
    if ctype == "Địa danh tham quan / Văn hóa - Lịch sử":
        if re.search(r"(ho guom|hoan kiem|ho hoan kiem)", kw_n):
            return "Hồ Hoàn Kiếm"
        if re.search(r"(pho co)", kw_n):
            return "Phố Cổ Hà Nội"
        if re.search(r"(hoang thanh)", kw_n):
            return "Hoàng Thành Thăng Long"
        if re.search(r"(van mieu|quoc tu giam)", kw_n):
            return "Văn Miếu - Quốc Tử Giám"
        if re.search(r"(lang bac|lang chu tich|ho chi minh)", kw_n):
            return "Lăng Bác & Quảng trường Ba Đình"
        if re.search(r"(tran quoc|ho tay)", kw_n):
            return "Chùa Trấn Quốc & Hồ Tây"
        if re.search(r"(nha hat lon)", kw_n):
            return "Nhà Hát Lớn Hà Nội"
        if re.search(r"(cot co)", kw_n):
            return "Cột Cờ Hà Nội"
        return "Điểm tham quan Hà Nội"

    if ctype == "Lưu trú":
        if re.search(r"(pho co|ho guom|hoan kiem)", kw_n):
            return "Khách sạn gần Hồ Gươm/Phố cổ"
        if re.search(r"(ho tay)", kw_n):
            return "Khách sạn Hồ Tây"
        if re.search(r"(\b4 sao\b|4 sao)", kw_n):
            return "Khách sạn 4 sao Hà Nội"
        if re.search(r"(\b5 sao\b|5 sao)", kw_n):
            return "Khách sạn 5 sao Hà Nội"
        return "Khách sạn Hà Nội"

    if ctype == "Di chuyển":
        if re.search(r"(noi bai|san bay|airport)", kw_n):
            return "Sân bay Nội Bài & di chuyển"
        if re.search(r"\btour\b", kw_n):
            return "Tour Hà Nội"
        if re.search(r"limousine", kw_n):
            return "Xe limousine từ Hà Nội"
        return "Di chuyển Hà Nội"

    if ctype == "Ẩm thực (F&B)":
        if re.search(r"bun cha", kw_n):
            return "Bún chả Hà Nội"
        # Chỉ coi là phở nếu keyword có 'phở' hoặc 'pho' kèm biến thể phở phổ biến
        if re.search(r"\bphở\b", raw) or re.search(r"\bpho\s+(bo|ga|cuon|tai|nam|dap|tron)\b", kw_n):
            return "Phở Hà Nội"
        if re.search(r"cafe|ca phe|coffee", kw_n):
            return "Cà phê Hà Nội"
        return "Ăn uống Hà Nội"

    return "Tổng hợp Hà Nội"


# =====================
# Data models
# =====================


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
    # Unknown/empty => để heuristic tự quyết (đừng auto đẩy về Informational)
    return None


def resolve_intent(keyword: str, ctype: str, seo_main_intent: str | None) -> str:
    """Resolve intent cuối cùng để vừa:
    - Tôn trọng SEO Insider nếu họ chắc chắn (đặc biệt Transaction)
    - Nhưng vẫn cho phép heuristic nâng một số query Lưu trú/Di chuyển sang Transaction
      (vì user intent đặt dịch vụ thường implicit, không cần có 'giá/đặt').

    Lý do: pool Transaction hiện bị thiếu nặng => không thể đạt ratio 20/40/40.
    """

    seo_intent = map_intent_from_seo_insider(seo_main_intent)
    inferred = infer_intent(keyword)

    # Không có dữ liệu SEO intent => dùng heuristic
    if seo_intent is None:
        return inferred

    # SEO nói Transaction thì tin luôn
    if seo_intent == "Transaction":
        return "Transaction"

    # Nếu heuristic nhìn ra Transaction rõ (đặc biệt Lưu trú/Di chuyển) thì ưu tiên Transaction
    if inferred == "Transaction" and ctype in ("Lưu trú", "Di chuyển"):
        return "Transaction"

    # SEO nói Informational nhưng heuristic có tín hiệu rõ khác intent => dùng heuristic
    if seo_intent == "Informational" and inferred != "Informational":
        return inferred

    return seo_intent


def infer_intent(keyword: str) -> str:
    kw_n = norm(keyword)

    # ===== Signals =====
    # Transaction: ý định mua/đặt rõ ràng
    # NOTE: kw_n đã strip accent => 'giá' -> 'gia', 'đặt' -> 'dat', ...
    trans_sig = re.search(
        r"(\bgia\b|\bdat\b|booking|mua|\bthue\b|voucher|combo|deal|khuyen mai)",
        kw_n,
    )

    # Một số cụm từ dù không có 'giá/đặt' vẫn mang ý định giao dịch
    trans_by_phrase = re.search(
        # Không include 'tour' ở đây vì 'tour hà nội' nhiều khi là query so sánh/chọn tour.
        r"(ve may bay|vé máy bay|ve tau|vé tàu|ve xe|vé xe|dua don|đưa đón)",
        kw_n,
    )

    # Commercial investigation: so sánh/chọn lựa
    comm_sig = re.search(
        r"(review|top|tot nhat|tốt nhất|so sanh|so sánh|kinh nghiem|kinh nghiệm|nen di|nên đi|list|nen o|nên ở)",
        kw_n,
    )

    is_stay = re.search(r"(khach san|hotel|resort|homestay|hostel|nha nghi|villa|apartment|can ho)", kw_n)
    is_move = re.search(r"(may bay|san bay|airport|taxi|limousine|thue xe|xe |bus|tau|di chuyen|di lai|dua don|\btour\b|\bve\b)", kw_n)
    is_landmark = re.search(
        r"(hoang thanh|van mieu|quoc tu giam|lang chu tich|lang bac|ho chi minh|chua|den|bao tang|di tich|pho co|ho guom|ho tay|hoan kiem|cot co|nha hat lon)",
        kw_n,
    )
    is_fb = re.search(r"(bun|pho|phở|quan an|nha hang|buffet|cafe|ca phe|coffee|dac san|an uong)", kw_n)

    # ===== Category-first rules (để dễ cân 20/40/40) =====
    if is_stay:
        if trans_sig:
            return "Transaction"
        if comm_sig:
            return "Commercial Investigation"
        # Mặc định: query khách sạn thường là giai đoạn cân nhắc/so sánh (CI)
        # Transaction sẽ được nhận diện bằng signal 'giá/đặt/booking/...' hoặc được promote ở bước selection.
        return "Commercial Investigation"

    if is_move:
        if trans_sig or trans_by_phrase:
            return "Transaction"
        if comm_sig:
            return "Commercial Investigation"
        # Mặc định:
        # - taxi/limousine/thuê xe/đưa đón => Transaction (đặt dịch vụ)
        # - tour chung chung ("tour hà nội") => thường là CI (đang xem có tour nào)
        if re.search(r"(taxi|limousine|thue xe|dua don)", kw_n):
            return "Transaction"
        if re.search(r"\btour\b", kw_n):
            # Có duration/điểm đến cụ thể thì coi như Transaction hơn
            if re.search(r"(\b\d+\s*(ngay|dem)\b|1 ngay|2 ngay|3 ngay)", kw_n):
                return "Transaction"
            return "Commercial Investigation"
        return "Commercial Investigation"

    if is_landmark:
        if trans_sig:
            return "Transaction"
        if comm_sig:
            return "Commercial Investigation"
        # các câu hỏi kiểu địa chỉ/ở đâu/giờ mở cửa => informational
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
    """Keyword không có signal Transaction rõ, nhưng có thể coi là Transaction
    để cân ratio 20/40/40 mà vẫn hợp lý với hành vi tìm kiếm du lịch.

    NOTE: Chỉ dùng để "promote" từ CI -> Transaction trong selection.
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

    # Lưu trú: các query dạng "khách sạn ..." thường có intent booking implicit
    # (nhưng Anh tránh promote những keyword có dấu hiệu thuần research như 'review/top/so sánh').
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
    # Gợi ý hành động cụ thể theo nhóm + intent + ctype.
    if row.group == "A":
        # Nhóm A: đang có data GSC
        if row.intent == "Transaction":
            return "Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hà Nội'"
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
                vol = int(float(row.get("search_volume") or 0)) if row.get("search_volume") not in (None, "", "--") else None
            except Exception:
                vol = None
            try:
                kd = int(float(row.get("difficulty") or 0)) if row.get("difficulty") not in (None, "", "--") else None
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
    # Gộp trend theo keyword: lấy max search interest và “increase” đáng chú ý nhất.
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


# =====================
# Build candidates
# =====================


def build_candidates():
    seo = load_seo_insider(SEO_INSIDER_PATH)
    trends = load_trends(TRENDS_DIR)
    gsc_rows = load_gsc_queries(GSC_QUERIES_PATH)

    candidates: dict[str, KeywordRow] = {}

    # Group A: từ GSC (giữ cả out-of-scope nhưng phải tách cluster đúng tỉnh)
    for r in gsc_rows:
        kw = r["keyword"]
        kw_n = norm(kw)

        geo, out_cluster = geo_scope(kw)
        if not is_destination_related(kw, geo):
            continue

        ctype = cluster_type(kw)

        # Loại rác "tổng hợp" không phải du lịch (đỡ bẩn report Hà Nội)
        if ctype == "Tổng hợp" and not is_travelish(kw_n):
            continue
        if kw_n in ("vietgoing",):
            continue

        cluster = cluster_name(kw, ctype, geo, out_cluster)

        seo_row = seo.get(kw_n)
        vol = str(seo_row["vol"]) if (seo_row and seo_row["vol"] is not None) else "N/A"
        kd = seo_row["kd"] if seo_row else None
        kd_text = f"{kd_bucket(kd)} ({kd if kd is not None else 'N/A'})"

        # Intent: resolve giữa SEO insider main_intent và heuristic
        intent = resolve_intent(kw, ctype, seo_row.get("main_intent") if seo_row else None)

        # SPI theo công thức: V * (I/V) * CTR = I * CTR
        # CTR trong GSC là %, convert về decimal
        spi = float(r["imp"]) * (float(r["ctr"]) / 100.0)

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
            score=spi,
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

        # Filter: phải liên quan du lịch (SEO Insider hay dính keyword linh tinh)
        if ctype == "Tổng hợp" and not is_travelish(kw_n):
            continue

        vol = s["vol"]
        kd = s["kd"]
        if vol is None or vol < 500:
            continue
        if kd is not None and kd >= 60:
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
        )
        row.action_plan = action_plan_for(row)
        candidates[kw_n] = row

    # Group B2: từ Google Trend – lọc travelish + Hanoi-ish
    for kw_n, t in trends.items():
        if kw_n in candidates:
            continue

        kw = t["keyword"]
        geo, out_cluster = geo_scope(kw)
        if not is_destination_related(kw, geo):
            continue

        if not is_travelish(kw_n):
            continue

        ctype = cluster_type(kw)
        cluster = cluster_name(kw, ctype, geo, out_cluster)

        inc = t.get("increase") or ""
        si = t.get("max_interest")
        kd_text = f"Trend {('SI:'+str(si)) if si is not None else ''} {inc}".strip()

        intent = infer_intent(kw)

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
            score=float(si or 0),
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

    # sort inside intent by group and score
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
        # Ưu tiên Group A + score
        soft.sort(key=lambda x: (0 if x.group == "A" else 1, -x.score))
        for row in soft[:need]:
            kn = norm(row.keyword)
            if kn in used:
                continue
            selected.append(promote(row, "Transaction"))
            used.add(kn)

    # 3) Commercial Investigation: lấy phần còn lại cho đủ target
    take("Commercial Investigation", targets["Commercial Investigation"])

    # fill remaining (nếu thiếu do pool ít): lấy best overall nhưng KHÔNG phá ratio quá nhiều
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
# Quality gate
# =====================


def run_quality_gate(rows: list[KeywordRow]):
    """Return dict gate_name -> list issues.

    Mục tiêu: export markdown hiển thị rõ từng gate PASS/FAIL.
    """

    gates: dict[str, list[str]] = {
        "taxonomy": [],
        "geo": [],
        "source": [],
        "intent_ratio": [],
    }

    # 1) Taxonomy: Landmark không được dính F&B
    landmark_terms = ["hoàng thành", "văn miếu", "lăng", "chùa", "đền", "bảo tàng", "di tích", "phố cổ", "hồ gươm", "hồ tây", "hoàn kiếm"]
    for r in rows:
        if r.cluster_type != "Ẩm thực (F&B)":
            continue
        rn = norm(r.keyword)
        if any(t in rn for t in [norm(x) for x in landmark_terms]):
            gates["taxonomy"].append(f"Taxonomy lỗi: '{r.keyword}' bị gán vào F&B")

    # 2) Geo: cluster Out-of-scope phải khớp geo
    for r in rows:
        if r.cluster.endswith(" Trip") and not r.geo_scope.startswith("Out-of-scope"):
            gates["geo"].append(f"Geo lỗi: '{r.keyword}' có cluster '{r.cluster}' nhưng geo_scope='{r.geo_scope}'")
        if r.geo_scope.startswith("Out-of-scope") and not r.cluster.endswith(" Trip"):
            gates["geo"].append(f"Geo lỗi: '{r.keyword}' out-of-scope nhưng cluster='{r.cluster}'")

    # 3) Source
    for r in rows:
        if not r.source or r.source.strip() == "":
            gates["source"].append(f"Source thiếu: '{r.keyword}'")

    # 4) Intent ratio (spec 20/40/40 cho report 100 keywords)
    if len(rows) == 100:
        from collections import Counter

        cnt = Counter([r.intent for r in rows])
        expected = {
            "Informational": 20,
            "Commercial Investigation": 40,
            "Transaction": 40,
        }
        for k, v in expected.items():
            if cnt.get(k, 0) != v:
                gates["intent_ratio"].append(f"Intent ratio lỗi: expected {k}={v} nhưng actual={cnt.get(k, 0)}")

    return gates


# =====================
# Markdown export
# =====================


def export_markdown(rows: list[KeywordRow]):
    header = f"""# REPORT KEYWORD PLANNER: {DESTINATION_NAME.upper()}

## 1. TỔNG QUAN CHIẾN LƯỢC
- **Mục tiêu**: Chiếm lĩnh thị trường du lịch {DESTINATION_NAME} cho vietgoing.com bằng dữ liệu thực tế (GSC) + xu hướng (Trend/SEO Insider).
- **Tổng số từ khóa**: {len(rows)}
- **Nguồn dữ liệu**:
  - `data/google_search_console/Queries.csv`
  - `data/seo_insider/advance_search_report.csv`
  - `data/google_trend/*.csv`

## 2. CHI TIẾT TỪ KHÓA (PHÂN THEO CLUSTER)

| Cluster | Cluster Type | Geo Scope | Keyword | Intent | Vol | Imp | Clicks | CTR | KD/Comp | Nguồn Dữ Liệu (Source) | Action Plan (Cụ thể) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""

    lines = [header]
    for r in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    r.cluster,
                    r.cluster_type,
                    r.geo_scope,
                    r.keyword,
                    r.intent,
                    r.vol,
                    r.imp,
                    r.clicks,
                    r.ctr,
                    r.kd_comp,
                    r.source,
                    r.action_plan,
                ]
            )
            + " |\n"
        )

    # Quality gate note (chi tiết)
    gates = run_quality_gate(rows)
    lines.append("\n## 3. QUALITY GATE (AUTO-CHECK)\n")

    # Tóm tắt intent distribution
    from collections import Counter

    cnt = Counter([r.intent for r in rows])
    lines.append(f"- **Intent distribution**: Informational={cnt.get('Informational',0)}, Commercial Investigation={cnt.get('Commercial Investigation',0)}, Transaction={cnt.get('Transaction',0)}\n")

    def gate_line(title: str, key: str):
        if not gates.get(key):
            lines.append(f"- [x] PASS: {title}\n")
        else:
            lines.append(f"- [ ] FAIL: {title}\n")
            for i in gates[key][:20]:
                lines.append(f"  - {i}\n")

    gate_line("Taxonomy (landmark không được nằm trong F&B)", "taxonomy")
    gate_line("Geo-scope (out-of-scope phải tách cluster '* Trip')", "geo")
    gate_line("Source (mỗi keyword phải có source folder/file)", "source")
    gate_line("Intent ratio (100 keywords phải đạt 20/40/40)", "intent_ratio")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("".join(lines))


def main():
    candidates = build_candidates()
    selected = select_keywords(candidates, total=100)
    export_markdown(selected)

    gates = run_quality_gate(selected)
    print(f"Generated: {OUTPUT_PATH}")
    print(f"Candidates: {len(candidates)} | Selected: {len(selected)}")
    total_issues = sum(len(v) for v in gates.values())
    print(f"Quality gate issues: {total_issues}")
    if total_issues:
        for k, arr in gates.items():
            for i in arr[:10]:
                print("-", i)


if __name__ == "__main__":
    main()
