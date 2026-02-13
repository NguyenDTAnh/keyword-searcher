
"""Script thu thập & phân loại từ khóa cho một destination.

CÁCH DÙNG:
  1) Copy file này, đổi tên theo destination, ví dụ: collect_danang.py
  2) Fill phần `DESTINATION = DestinationConfig(...)` ở đầu file.
  3) Đặt data vào đúng thư mục: data/google_search_console, data/seo_insider, data/google_trend
  4) Chạy: python scripts/collect_[destination].py

OUTPUT:
  - File CSV trung gian: reports/[destination]-raw.csv (100 keywords đã xử lý)
  - File CSV này sẽ được format_report.py (keyword-validator) đọc để tạo Report Final.

Yêu cầu quan trọng:
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
    # TODO: Thay đổi theo destination thực tế
    name="<TÊN DESTINATION>",            # Ví dụ: "Đà Nẵng"
    slug="<SLUG>",                        # Ví dụ: "danang"

    name_variants=[
        # TODO: Liệt kê các biến thể tên destination (có dấu + không dấu + viết liền)
        # Ví dụ: "đà nẵng", "da nang", "danang"
    ],

    entities=[
        # TODO: Liệt kê entity đặc hữu — địa danh nổi tiếng chỉ thuộc destination này
        # Keyword không chứa tên destination nhưng chứa entity vẫn được coi là in-scope
        # Ví dụ: "cầu rồng", "bà nà hills", "bán đảo sơn trà", ...
    ],

    districts=[
        # TODO: Liệt kê quận/huyện của destination
        # Ví dụ: "hải châu", "thanh khê", "liên chiểu", ...
    ],

    landmark_keywords=[
        # TODO: Từ khoá normalized (không dấu) để detect Landmark/Văn hoá-Lịch sử
        # Chú ý: đây là dạng KHÔNG DẤU vì logic match đã strip accent
        # Ví dụ: "cau rong", "ba na", "ngu hanh son", "son tra", ...
    ],

    cluster_rules={
        # TODO: Định nghĩa rules mapping cluster_name theo từng cluster_type
        # Format: {cluster_type: [{"pattern": regex, "name": display}, ...]}
        # Rule đầu tiên match thắng. Không match -> fallback mặc định.
    },

    province_display_overrides={
        # TODO: Override hiển thị tên tỉnh (normalized -> có dấu đúng)
        "phu quoc": "Phú Quốc",
        "da lat": "Đà Lạt",
        "da nang": "Đà Nẵng",
        "sa pa": "Sa Pa",
        "tam dao": "Tam Đảo",
    },

    extra_travel_patterns="",
)


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PHẦN DƯỚI ĐÂY KHÔNG CẦN CHỈNH SỬA (trừ khi muốn custom logic)           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝


# =====================
# Derived config
# =====================

WORKDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

GSC_QUERIES_PATH = os.path.join(WORKDIR, "data", "google_search_console", "Queries.csv")
SEO_INSIDER_PATH = os.path.join(WORKDIR, "data", "seo_insider", "advance_search_report.csv")
TRENDS_DIR = os.path.join(WORKDIR, "data", "google_trend")
# Output CSV trung gian — format_report.py sẽ đọc file này
OUTPUT_CSV = os.path.join(WORKDIR, "reports", f"{DESTINATION.slug}-raw.csv")


# Danh sách tỉnh/thành để detect out-of-scope.
PROVINCES = [
    "an giang", "bà rịa - vũng tàu", "bạc liêu", "bắc giang", "bắc kạn", "bắc ninh", "bến tre", "bình định",
    "bình dương", "bình phước", "bình thuận", "cà mau", "cần thơ", "cao bằng", "đà nẵng", "đắk lắk",
    "đắk nông", "điện biên", "đồng nai", "đồng tháp", "gia lai", "hà giang", "hà nam", "hà nội",
    "hà tĩnh", "hải dương", "hải phòng", "hậu giang", "hòa bình", "hưng yên", "khánh hòa", "kiên giang",
    "kon tum", "lai châu", "lâm đồng", "lạng sơn", "lào cai", "long an", "nam định", "nghệ an",
    "ninh bình", "ninh thuận", "phú thọ", "phú yên", "quảng bình", "quảng nam", "quảng ngãi", "quảng ninh",
    "quảng trị", "sóc trăng", "sơn la", "tây ninh", "thái bình", "thái nguyên", "thanh hóa", "thừa thiên huế",
    "tiền giang", "tp hồ chí minh", "trà vinh", "tuyên quang", "vĩnh long", "vĩnh phúc", "yên bái",
    "phú quốc", "tam đảo", "sầm sơn", "đồng văn", "sa pa", "sapa", "đà lạt", "huế", "hue", "nha trang",
    "vũng tàu", "vung tau", "quy nhơn", "quy nhon", "hạ long", "ha long", "sài gòn", "sai gon", "saigon",
    "hồ chí minh", "ho chi minh", "tphcm", "tp hcm", "quận 1", "quan 1", "quận 3", "quan 3",
]


def strip_accents(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return unicodedata.normalize("NFC", text)


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", strip_accents(text).lower()).strip()


def kw_contains(kw_norm: str, phrase: str) -> bool:
    p = re.escape(norm(phrase))
    return re.search(rf"(^|\W){p}(\W|$)", kw_norm) is not None


def is_travelish(kw_norm: str) -> bool:
    base_pattern = (
        r"(du lich|check in|dia diem|choi gi|kinh nghiem|lich trinh"
        r"|khach san|hotel|resort|homestay|hostel|nha nghi|villa|apartment|can ho"
        r"|tour|dat |booking|thue xe|xe |limousine|taxi|san bay|bus|tau|may bay"
        r"|an|quan an|nha hang|buffet|bun |ca phe|coffee)"
    )
    extra = DESTINATION.extra_travel_patterns.strip()
    if extra:
        if not extra.startswith("|"):
            extra = "|" + extra
        pattern = base_pattern[:-1] + extra + ")"
    else:
        pattern = base_pattern
    return re.search(pattern, kw_norm) is not None


def has_destination_token(keyword: str) -> bool:
    kw_n = norm(keyword)
    for variant in DESTINATION.name_variants:
        if kw_contains(kw_n, variant): return True
    for d in DESTINATION.districts:
        if kw_contains(kw_n, d): return True
    for e in DESTINATION.entities:
        if kw_contains(kw_n, e): return True
    return False


def is_destination_related(keyword: str, geo_label: str) -> bool:
    if geo_label == f"In-scope {DESTINATION.name}":
        return True
    return has_destination_token(keyword)


def geo_scope(keyword: str):
    kw_n = norm(keyword)
    for prov in PROVINCES:
        is_dest = False
        for v in DESTINATION.name_variants:
            if norm(v) == norm(prov):
                is_dest = True; break
        if is_dest: continue
        if kw_contains(kw_n, prov):
            prov_norm = norm(prov)
            prov_display = DESTINATION.province_display_overrides.get(prov_norm) or prov.title().replace("Tp ", "TP ")
            return (f"Out-of-scope {prov_display}", f"{prov_display} Trip")
    
    if has_destination_token(keyword):
        return (f"In-scope {DESTINATION.name}", DESTINATION.name)
    return ("Geo Ambiguous", "Geo Ambiguous")


def cluster_type(keyword: str) -> str:
    kw_n = norm(keyword)
    if re.search(r"(khach san|hotel|resort|homestay|hostel|nha nghi|villa|apartment|can ho)", kw_n):
        return "Lưu trú"
    if re.search(r"(tour|taxi|xe |limousine|thue xe|bus|tau|may bay|san bay|airport|di chuyen|dua don)", kw_n):
        return "Di chuyển"
    
    raw = (keyword or "").lower().strip()
    pho_is_food = re.search(r"\bphở\b", raw) or re.search(r"\bpho\s+(bo|ga|cuon|tai|nam|dap|tron)\b", kw_n)
    if re.search(r"\bbun\b", kw_n) or pho_is_food or re.search(r"(cha |banh |buffet|quan an|nha hang|an dem|cafe|ca phe|coffee|dac san|an uong)", kw_n):
        return "Ẩm thực (F&B)"
    
    landmark_pattern = r"chua|den|bao tang|di tich"
    if DESTINATION.landmark_keywords:
        landmark_pattern += "|" + "|".join(re.escape(lk) for lk in DESTINATION.landmark_keywords)
    if re.search(rf"({landmark_pattern})", kw_n):
        return "Địa danh tham quan / Văn hóa - Lịch sử"
    return "Tổng hợp"


def cluster_name(keyword: str, ctype: str, geo_label: str, out_cluster: str) -> str:
    kw_n = norm(keyword)
    if geo_label.startswith("Out-of-scope"): return out_cluster
    if geo_label == "Geo Ambiguous": return "Geo Ambiguous"
    rules = DESTINATION.cluster_rules.get(ctype, [])
    for rule in rules:
        if re.search(rule["pattern"], kw_n): return rule["name"]
    fallback_map = {
        "Địa danh tham quan / Văn hóa - Lịch sử": f"Điểm tham quan {DESTINATION.name}",
        "Lưu trú": f"Khách sạn {DESTINATION.name}",
        "Di chuyển": f"Di chuyển {DESTINATION.name}",
        "Ẩm thực (F&B)": f"Ăn uống {DESTINATION.name}",
    }
    return fallback_map.get(ctype, f"Tổng hợp {DESTINATION.name}")


CSV_COLUMNS = ["keyword", "cluster", "cluster_type", "geo_scope", "intent", "vol", "imp", "clicks", "ctr", "kd_comp", "source", "action_plan", "group", "score", "spi"]

@dataclass
class KeywordRow:
    keyword: str; cluster: str; cluster_type: str; geo_scope: str; intent: str
    vol: str; imp: str; clicks: str; ctr: str; kd_comp: str; source: str
    action_plan: str; group: str; score: float; spi: str


def resolve_intent(keyword: str, ctype: str, seo_main_intent: str | None) -> str:
    def map_intent(mi):
        mi = (mi or "").lower()
        if "transaction" in mi: return "Transaction"
        if "commercial" in mi or "navigational" in mi: return "Commercial Investigation"
        if "information" in mi: return "Informational"
        return None
    
    seo_intent = map_intent(seo_main_intent)
    inferred = infer_intent(keyword)
    if seo_intent == "Transaction": return "Transaction"
    if inferred == "Transaction" and ctype in ("Lưu trú", "Di chuyển"): return "Transaction"
    if seo_intent == "Informational" and inferred != "Informational": return inferred
    return seo_intent or inferred


def infer_intent(keyword: str) -> str:
    kw_n = norm(keyword)
    if re.search(r"(\bgia\b|\bdat\b|booking|mua|\bthue\b|voucher|combo|deal|khuyen mai|ve may bay|ve tau|ve xe)", kw_n): return "Transaction"
    if re.search(r"(review|top|tot nhat|so sanh|kinh nghiem|nen di|list|nen o)", kw_n): return "Commercial Investigation"
    ctype = cluster_type(keyword)
    if ctype in ("Lưu trú", "Di chuyển"): return "Commercial Investigation"
    return "Informational"


def action_plan_for(row: KeywordRow) -> str:
    dest = DESTINATION.name
    if row.group == "A":
        if row.intent == "Transaction": return f"Tối ưu landing (CTA/giá/FAQ), tăng CTR; internal link từ hub '{dest}'"
        return f"Cập nhật nội dung theo intent, bổ sung FAQ, tối ưu title để đẩy Top 1-3"
    if row.intent == "Transaction": return "Tạo landing chuyển đổi, gom vào cluster page + build backlink nội bộ"
    return "Viết bài top-list/guide; map vào cluster hub; link về trang dịch vụ"


def load_gsc(path):
    rows = []
    if not os.path.exists(path): return rows
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            kw = (row.get("Top queries") or "").strip()
            if not kw: continue
            try:
                rows.append({"keyword": kw, "clicks": int(float(row.get("Clicks") or 0)), "imp": int(float(row.get("Impressions") or 0)), 
                             "ctr": float((row.get("CTR") or "0").replace("%", "")), "pos": float(row.get("Position") or 0),
                             "source": f"data/google_search_console/{os.path.basename(path)}"})
            except: continue
    return rows


def load_seo(path):
    data = {}
    if not os.path.exists(path): return data
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            kw = (row.get("keyword") or "").strip()
            if not kw: continue
            try:
                vol = int(float(row.get("search_volume") or 0)) if row.get("search_volume") not in (None, "", "--") else None
                kd = int(float(row.get("difficulty") or 0)) if row.get("difficulty") not in (None, "", "--") else None
                data[norm(kw)] = {"keyword": kw, "vol": vol, "kd": kd, "main_intent": row.get("main_intent"), "source": f"data/seo_insider/{os.path.basename(path)}"}
            except: continue
    return data


def load_trends(dir_path):
    agg = {}
    for path in glob.glob(os.path.join(dir_path, "*.csv")):
        with open(path, newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            if not r.fieldnames or "query" not in r.fieldnames: continue
            for row in r:
                q = (row.get("query") or "").strip()
                if not q: continue
                qn = norm(q)
                si = int(row.get("search interest")) if (row.get("search interest") or "").isdigit() else None
                inc = (row.get("increase percent") or "").strip()
                if qn not in agg: agg[qn] = {"keyword": q, "max_interest": si, "increase": inc, "sources": {f"data/google_trend/{os.path.basename(path)}"}}
                else:
                    agg[qn]["sources"].add(f"data/google_trend/{os.path.basename(path)}")
                    if si is not None and (agg[qn]["max_interest"] is None or si > agg[qn]["max_interest"]): agg[qn]["max_interest"] = si
                    if inc == "Breakout": agg[qn]["increase"] = "Breakout"
    return agg


def build_candidates():
    seo = load_seo(SEO_INSIDER_PATH)
    trends = load_trends(TRENDS_DIR)
    gsc = load_gsc(GSC_QUERIES_PATH)
    candidates = {}
    
    for r in gsc:
        kw = r["keyword"]; kw_n = norm(kw)
        geo, out_cluster = geo_scope(kw)
        if not is_destination_related(kw, geo): continue
        ctype = cluster_type(kw)
        if ctype == "Tổng hợp" and not is_travelish(kw_n): continue
        if kw_n == "vietgoing": continue
        
        s = seo.get(kw_n)
        vol = str(s["vol"]) if (s and s["vol"] is not None) else "N/A"
        kd = s["kd"] if s else None
        kd_t = f"{'Low' if (kd or 0)<30 else 'Medium' if (kd or 0)<60 else 'High'} ({kd or 'N/A'})"
        intent = resolve_intent(kw, ctype, s.get("main_intent") if s else None)
        spi_v = float(r["imp"]) * (float(r["ctr"]) / 100.0)
        
        row = KeywordRow(keyword=kw.lower(), cluster=cluster_name(kw, ctype, geo, out_cluster), cluster_type=ctype, geo_scope=geo, intent=intent,
                         vol=vol, imp=str(r["imp"]), clicks=str(r["clicks"]), ctr=f"{r['ctr']}%", kd_comp=kd_t, source=r["source"],
                         action_plan="", group="A", score=spi_v, spi=f"{spi_v:.1f}")
        row.action_plan = action_plan_for(row)
        candidates[kw_n] = row

    for kw_n, s in seo.items():
        if kw_n in candidates: continue
        geo, out_cluster = geo_scope(s["keyword"])
        if not is_destination_related(s["keyword"], geo): continue
        ctype = cluster_type(s["keyword"])
        if ctype == "Tổng hợp" and not is_travelish(kw_n): continue
        vol = s["vol"]; kd = s["kd"]
        if vol is None or vol < 100: continue # Giảm xuống 100 để lấy nhiều hơn
        
        kd_t = f"{'Low' if (kd or 0)<30 else 'Medium' if (kd or 0)<60 else 'High'} ({kd or 'N/A'})"
        row = KeywordRow(keyword=s["keyword"].lower(), cluster=cluster_name(s["keyword"], ctype, geo, out_cluster), cluster_type=ctype, geo_scope=geo, 
                         intent=resolve_intent(s["keyword"], ctype, s.get("main_intent")), vol=str(vol), imp="N/A", clicks="N/A", ctr="N/A", 
                         kd_comp=kd_t, source=s["source"], action_plan="", group="B", score=float(vol)*(1.0-(kd or 50)/100.0), spi="N/A")
        row.action_plan = action_plan_for(row)
        candidates[kw_n] = row
        
    return list(candidates.values())


def select_keywords(candidates, total=100):
    buckets = defaultdict(list)
    for c in candidates: buckets[c.intent].append(c)
    for arr in buckets.values(): arr.sort(key=lambda x: (0 if x.group=="A" else 1, -x.score))
    
    selected = []; used = set()
    targets = {"Informational": int(total*0.2), "Commercial Investigation": int(total*0.4), "Transaction": total - int(total*0.2) - int(total*0.4)}

    for intent in ["Informational", "Transaction", "Commercial Investigation"]:
        pool = buckets.get(intent, [])
        for row in pool:
            if sum(1 for r in selected if r.intent == intent) >= targets[intent]: break
            kn = norm(row.keyword)
            if kn not in used: selected.append(row); used.add(kn)
            
    if len(selected) < total:
        rest = sorted([c for c in candidates if norm(c.keyword) not in used], key=lambda x: (0 if x.group=="A" else 1, -x.score))
        for row in rest:
            if len(selected) >= total: break
            selected.append(row); used.add(norm(row.keyword))
            
    selected.sort(key=lambda x: (x.cluster.lower(), 0 if x.group=="A" else 1, -x.score))
    return selected[:total]


def main():
    if not DESTINATION.name or DESTINATION.name.startswith("<"):
        print("❌ ERROR: Chưa fill DestinationConfig!"); return
    cands = build_candidates()
    sel = select_keywords(cands, 100)
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        w.writeheader()
        for r in sel: w.writerow(r.__dict__)
    print(f"✅ Exported: {OUTPUT_CSV} ({len(sel)} keywords)")

if __name__ == "__main__":
    main()
