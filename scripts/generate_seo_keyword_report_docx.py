""" 
Generate báo cáo .docx: "Xây dựng bộ từ khoá SEO"

Yêu cầu từ user:
- File .docx/.doc
- Trình bày phân cấp (Heading) + bulletpoint
- Nội dung 4 phần: Mục tiêu, Tổng quan SEO hiện tại + Trend, Phân loại nhóm từ khoá, Tiêu chí & Nguồn dữ liệu

Data input:
- reports/Bao_cao_xu_huong_tu_khoa_Vietgoing.md (tóm tắt GSC)
- data/google_trend/*.csv (Top queries + Rising queries)

Chạy:
  source .venv/bin/activate
  python scripts/generate_seo_keyword_report_docx.py
"""

from __future__ import annotations

import csv
import glob
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from docx import Document
from docx.shared import Pt


BASE_DIR = Path(__file__).resolve().parents[1]
REPORT_MD_PATH = BASE_DIR / "reports" / "Bao_cao_xu_huong_tu_khoa_Vietgoing.md"
TREND_DIR = BASE_DIR / "data" / "google_trend"
OUTPUT_DOCX_PATH = BASE_DIR / "reports" / "Xay_dung_bo_tu_khoa_SEO.docx"


# =============================
# Helpers: Google Trend parsing
# =============================


@dataclass(frozen=True)
class TrendRow:
    query: str
    search_interest: str
    increase_percent: str
    source_file: str


def _read_trend_csv(path: Path) -> list[TrendRow]:
    rows: list[TrendRow] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            q = (r.get("query") or "").strip()
            if not q:
                continue
            rows.append(
                TrendRow(
                    query=q,
                    search_interest=(r.get("search interest") or "").strip(),
                    increase_percent=(r.get("increase percent") or "").strip(),
                    source_file=path.name,
                )
            )
    return rows


def _norm_query(q: str) -> str:
    q = q.strip().lower()
    q = re.sub(r"\s+", " ", q)
    return q


def _score_increase_percent(val: str) -> int:
    v = (val or "").strip().lower()
    if v == "breakout":
        return 10_000
    v = v.replace("%", "").strip()
    try:
        return int(v)
    except Exception:
        return 0


def _to_int(val: str) -> int:
    try:
        return int(str(val).strip())
    except Exception:
        return 0


def _is_relevant_query(q: str) -> bool:
    """Filter nhẹ để giữ trend liên quan mảng Vietgoing.

    Lưu ý: Rising queries có khá nhiều query giáo dục/luật/... nhưng vẫn chứa "du lịch".
    Anh giữ lại theo keyword chính, sau đó highlight trong phần report là "từ khoá dạng info".
    """

    qn = _norm_query(q)
    keywords = [
        "khách sạn",
        "resort",
        "villa",
        "homestay",
        "du lịch",
        "tour",
        "đặt phòng",
        "đặt khách sạn",
        "đặt tour",
        "booking",
        "book phòng",
        "nghỉ dưỡng",
        "sân bay",
        "quận 1",
    ]
    return any(k in qn for k in keywords)


def load_trend_insights() -> dict:
    files = sorted(glob.glob(str(TREND_DIR / "*.csv")))
    top_rows: list[TrendRow] = []
    rising_rows: list[TrendRow] = []

    for f in files:
        p = Path(f)
        rows = _read_trend_csv(p)
        if "rising-queries" in p.name:
            rising_rows.extend(rows)
        elif "top-queries" in p.name:
            top_rows.extend(rows)

    # filter relevant
    top_rows = [r for r in top_rows if _is_relevant_query(r.query)]
    rising_rows = [r for r in rising_rows if _is_relevant_query(r.query)]

    # dedupe by normalized query (keep best score)
    def dedupe_best(rows: Iterable[TrendRow], key_fn, score_fn):
        best: dict[str, TrendRow] = {}
        best_score: dict[str, int] = {}
        for r in rows:
            k = key_fn(r)
            s = score_fn(r)
            if k not in best or s > best_score.get(k, -1):
                best[k] = r
                best_score[k] = s
        return list(best.values())

    top_rows = dedupe_best(
        top_rows,
        key_fn=lambda r: _norm_query(r.query),
        score_fn=lambda r: _to_int(r.search_interest),
    )
    rising_rows = dedupe_best(
        rising_rows,
        key_fn=lambda r: _norm_query(r.query),
        score_fn=lambda r: _score_increase_percent(r.increase_percent) * 100 + _to_int(r.search_interest),
    )

    top_rows.sort(key=lambda r: (_to_int(r.search_interest), _norm_query(r.query)), reverse=True)
    rising_rows.sort(
        key=lambda r: (
            _score_increase_percent(r.increase_percent),
            _to_int(r.search_interest),
            _norm_query(r.query),
        ),
        reverse=True,
    )

    return {
        "top": top_rows,
        "rising": rising_rows,
        "files": [Path(f).name for f in files],
    }


# =============================
# Helpers: parse GSC MD report
# =============================


def _extract_section(md: str, start_heading: str, end_heading: str | None = None) -> str:
    """Cắt nội dung giữa 2 heading markdown dạng '## X.'"""
    start_idx = md.find(start_heading)
    if start_idx == -1:
        return ""
    md2 = md[start_idx + len(start_heading) :]
    if end_heading:
        end_idx = md2.find(end_heading)
        if end_idx != -1:
            md2 = md2[:end_idx]
    return md2.strip()


def _extract_bullets(text: str) -> list[str]:
    bullets = []
    for line in text.splitlines():
        l = line.strip()
        if l.startswith("-"):
            bullets.append(re.sub(r"^\-\s+", "", l))
    return bullets


def _clean_md_inline(text: str) -> str:
    # remove markdown bold/italic/backticks
    t = text
    t = t.replace("**", "")
    t = re.sub(r"`([^`]*)`", r"\1", t)
    t = re.sub(r"_([^_]*)_", r"\1", t)
    return t.strip()


def load_gsc_summary(md_path: Path) -> dict:
    md = md_path.read_text(encoding="utf-8")
    overview = _extract_section(md, "## 1. Tổng Quan (Executive Summary)", "## 2.")
    overview_bullets = [_clean_md_inline(b) for b in _extract_bullets(overview)]

    top_clicks = [
        "vietgoing (2,348 clicks)",
        "khách sạn long thành 3 sầm sơn (727 clicks)",
        "khách sạn gần sân bay tân sơn nhất (690 clicks, 45,700 impressions, CTR 1.51%, vị trí 8.4)",
        "suối ở huế (669 clicks, CTR 25.51%)",
    ]
    destination_trends = [
        "Hạ Long - Quảng Ninh: 3,154 clicks | 63,997 impressions",
        "Hà Nội: 2,406 clicks | 101,051 impressions",
        "TP.HCM: 2,394 clicks | 140,801 impressions",
        "Tam Đảo - Vĩnh Phúc: 1,791 clicks | 71,296 impressions",
        "Huế: 1,581 clicks | 39,407 impressions",
        "Thanh Hóa: 1,515 clicks | 16,779 impressions",
    ]
    golden_opportunities = [
        "khách sạn gần sân bay tân sơn nhất: 45,700 impressions | CTR 1.51% | Avg Pos 8.4",
        "bảo tàng dân tộc học việt nam: 36,615 impressions | CTR 0.05%",
        "suối tiên: 30,165 impressions | CTR 0.12%",
        "khách sạn quận 1: 19,575 impressions | CTR 0.41%",
    ]

    action_plan = _extract_section(md, "## 5. Đề Xuất Chiến Lược (Action Plan)")
    action_plan_lines = []
    for line in action_plan.splitlines():
        l = _clean_md_inline(line.strip())
        if re.match(r"^\d+\.\s+", l):
            action_plan_lines.append(re.sub(r"^\d+\.\s+", "", l))

    return {
        "date": "12/02/2026",
        "overview_bullets": overview_bullets,
        "top_clicks": top_clicks,
        "destination_trends": destination_trends,
        "golden_opportunities": golden_opportunities,
        "action_plan": action_plan_lines,
    }


# =============================
# DOCX writer
# =============================


def _set_doc_defaults(doc: Document) -> None:
    """Set font mặc định để Word mở lên không bị 'font lạ'."""
    style = doc.styles["Normal"]
    font = style.font
    font.name = "Arial"
    font.size = Pt(11)


def _add_bullet(doc: Document, text: str, level: int = 0) -> None:
    p = doc.add_paragraph(style="List Bullet")
    if level > 0:
        # indent bằng cách tăng left indent qua paragraph_format
        p.paragraph_format.left_indent = Pt(18 * level)
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(11)


def _add_heading(doc: Document, text: str, level: int) -> None:
    # python-docx: level=0 là Title, 1 là Heading 1, ...
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = "Arial"


def build_report_docx() -> Path:
    gsc = load_gsc_summary(REPORT_MD_PATH)
    trend = load_trend_insights()

    doc = Document()
    _set_doc_defaults(doc)

    # Title
    _add_heading(doc, "Xây dựng bộ từ khoá SEO", level=0)

    # ============ Phần 1
    _add_heading(doc, "Phần 1: Mục tiêu", level=1)
    _add_bullet(
        doc,
        "Xây dựng bộ từ khoá cho 20 điểm đến/khu du lịch ở header tại Vietgoing.com nhằm đẩy SEO cho website, tăng tính bao phủ của website.",
    )

    # ============ Phần 2
    _add_heading(doc, "Phần 2: Tổng quan SEO hiện tại & xu hướng từ khoá", level=1)

    # 2.1 Tổng quan GSC
    _add_heading(doc, "2.1. Tổng quan tình hình SEO từ khoá hiện tại (Google Search Console)", level=2)
    _add_bullet(doc, f"Nguồn tham khảo: {REPORT_MD_PATH.as_posix()}")
    _add_bullet(doc, f"Ngày báo cáo tham chiếu: {gsc['date']}")

    _add_heading(doc, "Các điểm nổi bật", level=3)
    for b in gsc["overview_bullets"]:
        _add_bullet(doc, b)

    _add_heading(doc, "Từ khoá/nhóm từ khoá đang kéo traffic tốt", level=3)
    for x in gsc["top_clicks"]:
        _add_bullet(doc, x)

    _add_heading(doc, "Xu hướng theo điểm đến (tổng hợp clicks/impressions)", level=3)
    for x in gsc["destination_trends"]:
        _add_bullet(doc, x)

    _add_heading(doc, "Cơ hội vàng (Impressions cao - CTR thấp)", level=3)
    for x in gsc["golden_opportunities"]:
        _add_bullet(doc, x)

    if gsc["action_plan"]:
        _add_heading(doc, "Đề xuất chiến lược (từ báo cáo hiện tại)", level=3)
        for x in gsc["action_plan"]:
            _add_bullet(doc, x)

    # 2.2 Trend
    _add_heading(doc, "2.2. Phân tích xu hướng từ khoá (Google Trend - phạm vi 2025)", level=2)
    _add_bullet(doc, f"Nguồn dữ liệu: {TREND_DIR.as_posix()} (tổng {len(trend['files'])} file CSV)")
    _add_bullet(doc, "Khung thời gian dữ liệu: 2025-02-10 đến 2026-02-10 (bao gồm toàn bộ năm 2025)")

    top = trend["top"][:20]
    rising = trend["rising"][:20]

    _add_heading(doc, "Top queries (nhu cầu lớn, mức quan tâm cao)", level=3)
    for r in top:
        _add_bullet(
            doc,
            f"{r.query} (Interest: {r.search_interest}, YoY: {r.increase_percent})",
        )

    _add_heading(doc, "Rising queries (tăng trưởng nhanh)", level=3)
    for r in rising:
        _add_bullet(
            doc,
            f"{r.query} (Interest: {r.search_interest}, Tăng: {r.increase_percent})",
        )

    _add_heading(doc, "Nhận định từ Trend (gợi ý hướng mở rộng)", level=3)
    for s in [
        "Nhóm 'khách sạn + điểm đến' luôn nằm top: Đà Nẵng, Hà Nội, Đà Lạt, Nha Trang, Vũng Tàu, Hạ Long... => nên ưu tiên landing page theo điểm đến.",
        "Nhóm 'tour du lịch' có mức quan tâm cao và có xu hướng tăng ở nhiều điểm đến (Đà Nẵng, Phú Quốc, Ninh Bình...) => mở rộng content theo tour/ lịch trình.",
        "Xu hướng tăng xuất hiện nhiều query dạng thông tin (thuộc tỉnh nào, đi mấy ngày, review điểm đến...) => làm content informational để kéo top-of-funnel rồi dẫn về trang booking.",
        "Các query liên quan 'booking/đặt tour/đặt phòng' tăng => nên tối ưu CTA/Title/Meta nhấn mạnh ưu đãi, giá, đặt nhanh.",
    ]:
        _add_bullet(doc, s)

    # ============ Phần 3
    _add_heading(doc, "Phần 3: Phân loại nhóm từ khoá", level=1)
    _add_heading(doc, "Nhóm A", level=2)
    _add_bullet(doc, "Các từ khoá đã có sẵn trên website, đang SEO tốt hoặc có thể cải thiện")
    _add_heading(doc, "Nhóm B", level=2)
    _add_bullet(doc, "Nhóm từ khoá mới, mở rộng để tăng tính bao phủ của website")

    # ============ Phần 4
    _add_heading(doc, "Phần 4: Tiêu chí chọn lọc từ khoá và nguồn dữ liệu", level=1)
    _add_heading(doc, "4.1. Tiêu chí chọn lọc", level=2)

    _add_heading(doc, "Nhóm A", level=3)
    for x in [
        "Các từ khoá có lượng Impression cao hoặc có tỷ lệ CTR tốt",
        "Các từ khoá tiềm năng (Impressions cao nhưng CTR thấp / vị trí 6-10)",
    ]:
        _add_bullet(doc, x)

    _add_heading(doc, "Nhóm B", level=3)
    for x in [
        "Search Volume > 50 lượt tìm kiếm (trung bình) / tháng",
        "Tập trung vào các từ khoá như: Khách sạn, Resort, Villa, Du lịch, Tour du lịch, Đặt phòng, Book phòng",
        "Các từ khoá thuộc chủ đề du lịch, đặt phòng khách sạn, đặt tour",
        "Tập trung vào các ý định tìm kiếm: đặt phòng, tham khảo giá, tìm kiếm thông tin địa điểm, tour, khách sạn...",
        "Lấy các từ khoá trong toàn bộ năm 2025",
    ]:
        _add_bullet(doc, x)

    _add_heading(doc, "4.2. Nguồn dữ liệu", level=2)
    for x in [
        "Google Search Console",
        "Google trend",
        "Google Ads Planner",
        "SEO Insider",
    ]:
        _add_bullet(doc, x)

    OUTPUT_DOCX_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUTPUT_DOCX_PATH))
    return OUTPUT_DOCX_PATH


def main() -> None:
    out = build_report_docx()
    print(f"DONE: {out}")


if __name__ == "__main__":
    main()
