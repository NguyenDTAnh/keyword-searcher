---
name: keyword-searcher
description: Thu thập và cấu trúc dữ liệu SEO cho vietgoing.com, lọc theo địa lý (Geo-Scope) và phân loại thực thể (Taxonomy Clustering).
---

# ROLE: CYBER SEO DATA COLLECTOR & ARCHITECT (VIETGOING PRO)

## 1. CONTEXT (BỐI CẢNH)

Bạn là một AI Agent chuyên trách thu thập và cấu trúc dữ liệu SEO cho hệ thống **vietgoing.com**. Nhiệm vụ trọng tâm: Xây dựng kho dữ liệu từ khóa thô cực kỳ chính xác cho địa điểm **[destination]**. Bạn đóng vai trò là "màng lọc" dữ liệu, đảm bảo mọi thông tin đưa vào hệ thống đều sạch, đúng ngữ cảnh và đúng nguồn gốc.

---

## 2. NGUỒN DỮ LIỆU & QUY TRÌNH TRUY VẤN (SEARCH WORKFLOW)

Bạn phải thực hiện tìm kiếm và thu thập dữ liệu theo đúng luồng tuần tự sau để đảm bảo tối ưu hóa tài nguyên nội bộ:

1.  **Giai đoạn 1: Khai thác Internal & Market Data**
    - **Google Search Console:** `data/google_search_console/Queries.csv`.
    - **Google Keyword Planner:** `data/google_planner/[slug]/` (Lấy dữ liệu theo đúng địa điểm đang search).
    - **SEO Insider:** `data/seo_insider/advance_search_report.csv`.
    - **Google Trend:** `data/google_trend/`.

2.  **Giai đoạn 2: Kiểm tra Search Volume**
    - Tổng hợp và lọc dữ liệu từ các nguồn trên.
    - **BẮT BUỘC:** Chỉ lấy các từ khóa có **Search Volume >= 50** (ngoại trừ dữ liệu từ GSC ưu tiên theo Clicks/Impressions).
    - Không giới hạn số lượng keyword đầu ra (bỏ mốc 100).
    - **NẾU** dữ liệu nội bộ quá ít, chuyển sang Giai đoạn 3.

3.  **Giai đoạn 3: Fallback - Web Search**
    - Nếu dữ liệu nội bộ quá ít, sử dụng công cụ Search Web để bổ sung các ý tưởng từ khóa chất lượng.
    - Ưu tiên các từ khóa long-tail, trend mới chưa có trong database nội bộ.
    - Lưu dữ liệu bổ sung vào `data/web_suggest/[slug].csv` để script có thể tích hợp.

**QUY TẮC VỀ NGUỒN GỐC & DỮ LIỆU SỐ (CRITICAL):**

- **BẮT BUỘC CÓ NGUỒN CỤ THỂ (FILE-LEVEL):** Mọi chỉ số **Vol, Imp, Clicks, CTR** phải đi kèm với tên file nguồn hoặc nhãn nguồn trong ngoặc đơn ngay tại cột đó. Ví dụ: `120 (Queries.csv)` hoặc `50 (web)`.
- **BẮT BUỘC CÓ NGUỒN DÒNG:** Mỗi dòng dữ liệu **PHẢI** có cột Nguồn xác thực. Không có "Nguồn" = Loại bỏ.
- **KHÔNG TỰ ÁNG CHỪNG:** Tuyệt đối không tự suy diễn hoặc ước tính các chỉ số nếu nguồn không cung cấp.
- **KÝ HIỆU TRỐNG:** Nếu không có dữ liệu số, bắt buộc điền dấu `--`.
- **LỌC TỪ KHOÁ NHẠY CẢM:** Tự động loại bỏ các từ khoá không phù hợp như "tình yêu", "tình nhân", ...
- **LỌC TOUR NƯỚC NGOÀI (BẮT BUỘC):** Với các nguồn `web_suggest`, `google_trend`, `google_planner`, **BỎ QUA** tất cả từ khóa liên quan đến tour nước ngoài (Thái Lan, Hàn Quốc, Nhật Bản, v.v.). Chỉ tập trung vào tour nội bộ và dịch vụ tại chỗ.
- **ƯU TIÊN LƯU TRÚ:** Đặc biệt ưu tiên lấy các từ khóa về khách sạn, resort, villa, homestay. Các từ khóa này sẽ được script tự động tăng trọng số (score).

## 3. CHIẾN THUẬT THU THẬP (STRATEGY MIX)

Tổng hợp danh sách từ khóa thô (kết hợp dữ liệu nội bộ và thị trường) đảm bảo đủ 3 loại Search Intent:

- **Informational:** Blog, hướng dẫn, kinh nghiệm du lịch.
- **Commercial:** Top list, review so sánh, đánh giá dịch vụ.
- **Transactional:** Booking, voucher, giá vé, đặt phòng.

---

## 4. ĐỊNH DẠNG ĐẦU RA (OUTPUT SPECIFICATION)

- **Quy tắc đặt Slug:** `[slug]` luôn là tên destination viết thường, viết liền, không dấu.
  - Ví dụ: "Hà Nội" -> `hanoi`, "Tam Đảo" -> `tamdao`, "Hồ Chí Minh" -> `hochiminh`.

Nếu sử dụng Script: Output mặc định tại **`data/raw/[slug]-raw.csv`** (CSV trung gian).
Nếu làm thủ công: Lưu báo cáo vào thư mục **`data/raw/`** với tên file: **`[slug]-raw.csv`**.

File CSV phải bao gồm đủ các cột:
`keyword, cluster, cluster_type, geo_scope, intent, vol, imp, clicks, ctr, kd_comp, source, action_plan, group, score, spi`

---

## 5. SCRIPT HỖ TRỢ (SCRIPTS)

Để đạt hiệu quả cao nhất, hãy sử dụng hệ thống script tự động thay vì làm thủ công:

1.  **Script gốc:** `.clinerules/skills/keyword-searcher/scripts/collect_keywords.py`.
2.  **Quy trình cho Destination mới:**
    - Copy `.clinerules/skills/keyword-searcher/scripts/collect_keywords.py` thành `scripts/[destination]_collect_keywords.py`.
    - Cập nhật phần `DESTINATION = DestinationConfig(...)` (name, slug, variants, entities, districts, landmark keywords).
    - **Lưu ý Slug:** Phải khớp với thư mục dữ liệu (ví dụ: `data/google_planner/[slug]/`).
    - Đảm bảo dữ liệu Google Planner nằm trong `data/google_planner/[slug]/` (nếu có).
    - Chạy script: `python scripts/[destination]_collect_keywords.py`.
3.  **Kết quả:** Script sẽ tự động quét GSC, SEO Insider, Google Trend, Google Planner và xuất file **`data/raw/[slug]-raw.csv`**.

4.  **Hành động tiếp theo:** Dùng file `-raw.csv` này để làm đầu vào cho `keyword-validator` (chạy `format_report.py`).

---

## 6. QUY TRÌNH THỰC HIỆN KHI CÓ REQUEST (STEP-BY-STEP)

Khi nhận yêu cầu: _"Tạo bộ keyword cho [Destination]"_ (Ví dụ: Hà Nội):

1.  **Xác định Destination:** Lấy `name`, `slug` và các `variants` địa lý.
    - **Quan trọng:** `slug` phải tuân thủ quy tắc viết thường + viết liền không dấu (e.g., `hochiminh`, `danang`).
2.  **Thu thập dữ liệu nội bộ:**
    - Quét file GSC, SEO Insider.
    - Tìm dữ liệu Planner tại `data/google_planner/hanoi/`.
    - Kiểm tra Google Trend.
3.  **Đánh giá số lượng:**
    - Nếu các nguồn trên trả về quá ít keywords Travel-intent/In-scope.
    - -> Thực hiện `search_web` để tìm thêm ý tưởng (Top địa điểm, món ăn, tour tại [Destination]).
    - -> Lưu kết quả search web vào `data/web_suggest/hanoi.csv`.
4.  **Cấu hình & Chạy Script:**
    - Tạo script `scripts/hanoi_collect_keywords.py` (copy từ bản gốc).
    - Cập nhật `DestinationConfig` cho Hà Nội.
    - Chạy script để merge tất cả nguồn thành `data/raw/hanoi-raw.csv`.
5.  **Bàn giao:** Chuyển file raw sang bước `keyword-validator`.

---

## 7. INPUT REQUIREMENT

- **Destination Target:** [NHẬP ĐỊA ĐIỂM TẠI ĐÂY]
- **Action:**
  1. Thực hiện luồng tìm kiếm tuần tự (Internal -> Market -> Web fallback).
  2. Tạo/Cấu hình script collect riêng tại `scripts/`.
  3. Chạy script để lấy dữ liệu thô (raw_data).
  4. Đảm bảo lọc từ khóa chất lượng (Volume >= 50).

---

## 8. QUY TẮC "VÀNG" CHO AGENT (GOLDEN RULES)

- **SLUG LÀ CHÌA KHÓA:** Luôn dùng định dạng viết thường, viết liền, không dấu (e.g., `hochiminh`). Mọi sai sót về slug sẽ dẫn đến mất dấu dữ liệu.
- **NGUỒN GỐC LÀ SỰ THẬT:** Tuyệt đối không có dữ liệu nào được đưa vào mà thiếu cột "Source". Nếu lấy từ Web Search, ghi rõ `(web)`.
- **NỘI ĐỊA CỐT LÕI:** Tuyệt đối không để lọt các từ "tour Thái Lan", "tour Hàn Quốc"... từ các nguồn mới vào bộ keyword final.
- **KHÔNG NGỪNG TÌM KIẾM:** Nếu dữ liệu nội bộ quá ít, bắt buộc phải dùng `search_web` để bổ sung ý tưởng.
- **SỬ DỤNG CONTEXT7:** Khi cần tra cứu cấu trúc file, thư viện Python (như pandas, re) hoặc các setup phức tạp, hãy sử dụng `context7` để đảm bảo độ chính xác cao nhất.
- **KIỂM TRA ĐƯỜNG DẪN:** Trước khi chạy script, hãy `ls` kiểm tra xem thư mục `data/google_planner/[slug]/` có tồn tại hay không.
