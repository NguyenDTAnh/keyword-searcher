# WORKFLOW: KEYWORD PLANNER & STRATEGY

Workflow này kết hợp sức mạnh của 2 skills chuyên biệt để tạo ra báo cáo từ khóa chất lượng cao cho `vietgoing.com`.

## Inputs

- **Destination Target**: Tên địa điểm cần làm SEO (VD: "Hà Nội", "Đà Nẵng", "Sapa").
- **Dữ liệu nguồn**: Các file từ google_search_console, google_trend, seo_insider đặt tại `data/`.

---

## BƯỚC 1: THU THẬP & PHÂN LOẠI (keyword-searcher)

**Mục tiêu:** Thu thập từ khóa từ data nội bộ, lọc geo, gán cluster/intent, chọn 100 keyword chuẩn.

1.  **Ưu tiên 1 (Script):** Nếu folder `data/` có đầy đủ file CSV:
    - **Lệnh:** `python3 .clinerules/skills/keyword-searcher/scripts/collect_keywords.py`
    - **Lưu ý:** Fill `DestinationConfig` trong script trước khi chạy.
    - **Output:** File CSV trung gian: `reports/[slug]-raw.csv`

2.  **Ưu tiên 2 (Manual/Add-on):** Nếu thiếu dữ liệu hoặc cần thêm keyword:
    - Sử dụng skill `keyword-searcher` để research bổ sung.
    - Đảm bảo output có cột `Group` (A: Cũ, B: Mới).

3.  **Output Mong Đợi:** File `reports/[slug]-raw.csv` có 100 keywords đã phân loại.

---

## BƯỚC 2: SẮP XẾP & FORMAT REPORT (keyword-validator)

**Mục tiêu:** Đọc CSV trung gian, sắp xếp chiến lược, xuất báo cáo 2 bảng Markdown.

1.  **Chạy Script:**
    - **Lệnh:** `python3 .clinerules/skills/keyword-validator/scripts/format_report.py --name "[Destination]" --slug [slug]`
    - **Input:** File `reports/[slug]-raw.csv` (từ Bước 1).
    - **Nhiệm vụ tự động:**
      - **Split Tables:** Chia thành 2 bảng riêng biệt:
        - **BẢNG 1: TỪ KHÓA CŨ (Group A):** Sắp xếp theo **CTR > Impressions > Clicks**.
        - **BẢNG 2: TỪ KHÓA MỚI (Group B):** Sắp xếp theo **Volume > KD/Comp (Low trước)**.
      - **Quality Gate:** Kiểm tra Taxonomy, Geo, Source, Intent 20/40/40.
    - **Output:** File Final: `destination/[Destination] - keyword.md`

2.  **Audit (Manual):** Sau khi chạy script, reviewer kiểm tra lại và bổ sung nếu cần.

---

## BƯỚC 3: REVIEW & FINAL REPORT

1.  **Review báo cáo:**
    - Kiểm tra logic xếp hạng trong file `destination/[Destination] - keyword.md`.
    - Đảm bảo các `Action Plan` (Ghi chú) là khả thi.

2.  **Quality Checklist (Bắt buộc):**
    Chỉ khi tất cả các mục dưới đây được đánh dấu tick `[x]`, báo cáo mới được coi là hoàn thành:
    - [ ] **Tối thiểu 100 từ khóa:** Tổng cộng cả từ khóa Cũ và Mới phải đạt số lượng từ 100 trở lên.
    - [ ] **100% Có Nguồn Gốc:** Tất cả các từ khóa và thông số đi kèm phải có nhãn nguồn (`Source`) rõ ràng. Không chấp nhận dữ liệu thiếu nguồn.
    - [ ] **Đúng địa lý (Geo-Scope):** Toàn bộ từ khóa phải thuộc đúng khu vực `[Destination]`.
    - [ ] **Phân loại chính xác:** Các từ khóa phải nằm đúng Cluster và Search Intent.

3.  **Kết thúc:**
    - File cuối cùng: **`destination/[Destination] - keyword.md`** (do `format_report.py` tạo).
    - Dữ liệu trung gian: **`reports/[slug]-raw.csv`** (do `collect_keywords.py` tạo).
