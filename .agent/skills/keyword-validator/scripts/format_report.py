
"""Script sắp xếp & format keyword report cho một destination.

CÁCH DÙNG:
  1) Chạy collect_keywords.py (keyword-searcher) trước để có file CSV trung gian.
  2) Chạy script này: python .clinerules/skills/keyword-validator/scripts/format_report.py
  3) Hoặc truyền tên destination: python format_report.py --name "Hà Nội" --slug hanoi

INPUT:
  - File CSV trung gian: reports/[slug]-raw.csv (do collect_keywords.py tạo ra)

OUTPUT:
  - File Markdown final: destination/[Destination] - keyword.md
  - Bao gồm 2 bảng: TỪ KHÓA CŨ (Group A) & TỪ KHÓA MỚI (Group B)
  - Quality Gate check tự động

Yêu cầu:
  - Bảng 1 (Group A): Sắp xếp theo CTR > Impressions > Clicks
  - Bảng 2 (Group B): Sắp xếp theo Volume > KD/Comp (Low trước)
  - Quality Gate: Taxonomy, Geo, Source, Intent ratio 20/40/40
"""

import argparse
import csv
import os
from collections import Counter
from dataclasses import dataclass


# =====================
# Config
# =====================

WORKDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))


# =====================
# Data model — đồng bộ với collect_keywords.py
# =====================

CSV_COLUMNS = [
    "keyword", "cluster", "cluster_type", "geo_scope", "intent",
    "vol", "imp", "clicks", "ctr", "kd_comp",
    "source", "action_plan", "group", "score", "spi",
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
    spi: str


# =====================
# Helpers
# =====================

def _parse_val(v: str) -> float:
    """Trích xuất giá trị số từ string có thể chứa label nguồn.
    Ví dụ: "36615 (Queries.csv)" -> 36615.0
            "2.49%" -> 2.49
            "N/A" -> 0.0
    """
    if not v or v == "N/A" or v == "--":
        return 0.0
    # Lấy phần số trước dấu ngoặc đơn (nếu có)
    clean = v.split("(")[0].strip().replace(",", "").replace("%", "")
    try:
        return float(clean)
    except (ValueError, TypeError):
        return 0.0


# =====================
# CSV Loader
# =====================


def load_csv(csv_path: str) -> list[KeywordRow]:
    """Đọc file CSV trung gian và convert thành list KeywordRow."""
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(KeywordRow(
                keyword=row.get("keyword", ""),
                cluster=row.get("cluster", ""),
                cluster_type=row.get("cluster_type", ""),
                geo_scope=row.get("geo_scope", ""),
                intent=row.get("intent", ""),
                vol=row.get("vol", "N/A"),
                imp=row.get("imp", "N/A"),
                clicks=row.get("clicks", "N/A"),
                ctr=row.get("ctr", "N/A"),
                kd_comp=row.get("kd_comp", "N/A"),
                source=row.get("source", ""),
                action_plan=row.get("action_plan", ""),
                group=row.get("group", ""),
                score=float(row.get("score", 0)),
                spi=row.get("spi", "N/A"),
            ))
    return rows


# =====================
# Quality Gate
# =====================


def run_quality_gate(rows: list[KeywordRow], dest_name: str) -> dict[str, list[str]]:
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
    generic_landmarks = ["chùa", "đền", "bảo tàng", "di tích"]
    for r in rows:
        if r.cluster_type != "Ẩm thực (F&B)":
            continue
        kw_lower = r.keyword.lower()
        if any(t in kw_lower for t in generic_landmarks):
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
# Markdown Export — 2 bảng chuẩn chiến lược
# =====================


def export_markdown(rows: list[KeywordRow], dest_name: str, output_path: str):
    """Tạo file markdown final với 2 bảng: Group A (Cũ) và Group B (Mới)."""

    # --- Section 1: Tổng quan ---
    header_intro = f"""# REPORT KEYWORD PLANNER: {dest_name.upper()}

## 1. TỔNG QUAN CHIẾN LƯỢC
- **Mục tiêu**: Chiếm lĩnh thị trường du lịch {dest_name} cho vietgoing.com bằng dữ liệu thực tế (GSC) + xu hướng (Trend/SEO Insider).
- **Tổng số từ khóa**: {len(rows)}
- **Nguồn dữ liệu**:
  - `data/google_search_console/Queries.csv`
  - `data/seo_insider/advance_search_report.csv`
  - `data/google_trend/*.csv`
"""

    # --- Section 2: Top SPI summary ---
    top_spi = [r for r in rows if r.group == "A"]
    top_spi.sort(key=lambda x: float(x.score), reverse=True)
    top_spi = top_spi[:10]

    header_summary = "\n## 2. TOP TỪ KHÓA TIỀM NĂNG (THEO SPI - GROUP A)\n"
    header_summary += "> **SPI (SEO Potential Index)** = Impressions x CTR (tương đương Clicks thực tế). Đây là các từ khóa đang perform tốt nhất, cần tối ưu để scale.\n\n"
    header_summary += "| Keyword | Cluster | SPI | CTR | Action Plan |\n| :--- | :--- | :--- | :--- | :--- |\n"
    for r in top_spi:
        header_summary += f"| **{r.keyword}** | {r.cluster} | {r.spi} | {r.ctr} | Push Top |\n"

    # --- Section 3: BẢNG 1 — GROUP A (TỪ KHÓA CŨ) ---
    header_group_a = """
## 3. NHÓM 1: TỪ KHÓA CŨ (TỐI ƯU HÓA TÀI SẢN HIỆN CÓ - GROUP A)
> **Tiêu chí sắp xếp**: CTR giảm dần > Impressions giảm dần. Tập trung tối ưu On-page và Internal Link để đẩy Top.

| STT | Cluster | Cluster Type | Keyword | Intent | SPI | Imp | Clicks | CTR | KD/Comp | Source | Action Plan |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    group_a_rows = [r for r in rows if r.group == "A"]
    # Sắp xếp Group A: CTR giảm dần > Imp giảm dần > Clicks giảm dần
    group_a_rows.sort(
        key=lambda x: (_parse_val(x.ctr), _parse_val(x.imp), _parse_val(x.clicks)),
        reverse=True,
    )

    # --- Section 4: BẢNG 2 — GROUP B (TỪ KHÓA MỚI) ---
    header_group_b = """
## 4. NHÓM 2: TỪ KHÓA MỚI (KHAI PHÁ THỊ TRƯỜNG - GROUP B)
> **Tiêu chí sắp xếp**: Volume giảm dần > KD Low. Tập trung viết nội dung mới và xây dựng Topic Hub.

| STT | Cluster | Cluster Type | Keyword | Intent | Vol | KD/Comp | Source | Action Plan |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    group_b_rows = [r for r in rows if r.group == "B"]
    # Sắp xếp Group B: Volume giảm dần > KD (ưu tiên Low trước)
    group_b_rows.sort(
        key=lambda x: (_parse_val(x.vol), -1 if "Low" in x.kd_comp else 0),
        reverse=True,
    )

    # --- Ghép nối tất cả ---
    lines = [header_intro, header_summary, header_group_a]
    idx_a = 1
    for r in group_a_rows:
        lines.append(
            f"| {idx_a} | {r.cluster} | {r.cluster_type} | **{r.keyword}** | {r.intent} "
            f"| {r.spi} | {r.imp} | {r.clicks} | {r.ctr} | {r.kd_comp} "
            f"| {r.source} | {r.action_plan} |\n"
        )
        idx_a += 1

    lines.append(header_group_b)
    idx_b = 1
    for r in group_b_rows:
        lines.append(
            f"| {idx_b} | {r.cluster} | {r.cluster_type} | **{r.keyword}** | {r.intent} "
            f"| {r.vol} | {r.kd_comp} | {r.source} | {r.action_plan} |\n"
        )
        idx_b += 1

    # --- Section 5: Quality Gate ---
    gates = run_quality_gate(rows, dest_name)
    lines.append("\n## 5. QUALITY GATE (AUTO-CHECK)\n")

    # Tóm tắt intent distribution
    cnt = Counter([r.intent for r in rows])
    lines.append(
        f"- **Intent distribution**: Informational={cnt.get('Informational', 0)}, "
        f"Commercial Investigation={cnt.get('Commercial Investigation', 0)}, "
        f"Transaction={cnt.get('Transaction', 0)}\n"
    )

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

    # --- Ghi file ---
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("".join(lines))

    return gates


# =====================
# Main
# =====================


def main():
    parser = argparse.ArgumentParser(
        description="Format keyword report từ CSV trung gian thành Markdown 2 bảng."
    )
    parser.add_argument(
        "--name", required=True,
        help="Tên destination hiển thị. Ví dụ: 'Hà Nội'"
    )
    parser.add_argument(
        "--slug", required=True,
        help="Slug của destination. Ví dụ: 'hanoi'"
    )
    args = parser.parse_args()

    dest_name = args.name
    slug = args.slug

    csv_path = os.path.join(WORKDIR, "reports", f"{slug}-raw.csv")
    output_path = os.path.join(WORKDIR, "destination", f"{dest_name} - keyword.md")

    if not os.path.exists(csv_path):
        print(f"❌ ERROR: Không tìm thấy file CSV: {csv_path}")
        print(f"   Hãy chạy collect_keywords.py trước!")
        return

    rows = load_csv(csv_path)
    if not rows:
        print(f"❌ ERROR: File CSV rỗng: {csv_path}")
        return

    gates = export_markdown(rows, dest_name, output_path)

    total_issues = sum(len(v) for v in gates.values())
    group_a_count = sum(1 for r in rows if r.group == "A")
    group_b_count = sum(1 for r in rows if r.group == "B")

    print(f"✅ Generated: {output_path}")
    print(f"   Total: {len(rows)} keywords (Group A: {group_a_count} | Group B: {group_b_count})")
    print(f"   Quality gate issues: {total_issues}")
    if total_issues:
        for k, arr in gates.items():
            for i in arr[:10]:
                print(f"   - {i}")


if __name__ == "__main__":
    main()
