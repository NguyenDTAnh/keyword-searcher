# REPORT KEYWORD PLANNER: HÒA BÌNH

## 1. TỔNG QUAN CHIẾN LƯỢC
- **Mục tiêu**: Chiếm lĩnh thị trường du lịch Hòa Bình cho vietgoing.com bằng dữ liệu thực tế (GSC) + xu hướng (Trend/SEO Insider).
- **Tổng số từ khóa**: 124
- **Nguồn dữ liệu**:
  - `web (hoa-binh.csv)` (112 từ khóa)
  - `data/google_search_console/Queries.csv` (6 từ khóa)
  - `data/seo_insider/advance_search_report.csv` (5 từ khóa)
  - `data/google_trend/searched_with_rising-queries_VN_20250210-1752_20260210-1752.csv; data/google_trend/searched_with_top-queries_VN_20250210-1752_20260210-1752.csv` (1 từ khóa)

## 2. TOP TỪ KHÓA TIỀM NĂNG (THEO SPI - GROUP A)
> **Action Plan**: Đây là các từ khóa đang perform tốt nhất, cần tối ưu để scale.

| Keyword | Cluster | CTR | Action Plan |
| :--- | :--- | :--- | :--- |
| **villa hồ đồng chanh hòa bình** | Khách sạn Hòa Bình | 13.15% | Push Top |
| **melody retreat hoà bình** | Khách sạn Hòa Bình | 5.07% | Push Top |
| **khách sạn hoa viên kim bôi** | Khách sạn Hòa Bình | 2.45% | Push Top |
| **resort melody hoà bình** | Resort Hòa Bình | 12.66% | Push Top |
| **halo retreat hòa bình** | Khách sạn Hòa Bình | 2.81% | Push Top |
| **melody retreat hòa bình review** | Khách sạn Hòa Bình | 7.63% | Push Top |

## 3. NHÓM 1: TỪ KHÓA CŨ (TỐI ƯU HÓA TÀI SẢN HIỆN CÓ - GROUP A)
> **Tiêu chí sắp xếp**: CTR giảm dần > Impressions giảm dần. Tập trung tối ưu On-page và Internal Link để đẩy Top.

| STT | Cluster | Cluster Type | Keyword | Intent | Imp | Clicks | CTR | Source | Action Plan |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Khách sạn Hòa Bình | Lưu trú | **villa hồ đồng chanh hòa bình** | Transaction | 213 | 28 | 13.15% | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hòa Bình' |
| 2 | Resort Hòa Bình | Lưu trú | **resort melody hoà bình** | Transaction | 158 | 20 | 12.66% | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hòa Bình' |
| 3 | Khách sạn Hòa Bình | Lưu trú | **melody retreat hòa bình review** | Commercial Investigation | 131 | 10 | 7.63% | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 4 | Khách sạn Hòa Bình | Lưu trú | **melody retreat hoà bình** | Transaction | 434 | 22 | 5.07% | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hòa Bình' |
| 5 | Khách sạn Hòa Bình | Lưu trú | **halo retreat hòa bình** | Transaction | 356 | 10 | 2.81% | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hòa Bình' |
| 6 | Khách sạn Hòa Bình | Lưu trú | **khách sạn hoa viên kim bôi** | Transaction | 857 | 21 | 2.45% | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hòa Bình' |

## 4. NHÓM 2: TỪ KHÓA MỚI (KHAI PHÁ THỊ TRƯỜNG - GROUP B)
> **Tiêu chí sắp xếp**: Score tổng hợp (Volume cao + Cạnh tranh thấp/trung bình -> YoY tăng + Bid cao).

| STT | Cluster | Cluster Type | Keyword | Intent | Vol | YoY | KD/Comp | Bid (High) | Source | Action Plan |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Khách sạn Hòa Bình | Lưu trú | **mandala retreats kim bôi** | Transaction | 18100 | N/A | Low (0) | N/A | data/seo_insider/advance_search_report.csv | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 2 | Resort Hòa Bình | Lưu trú | **serena resort kim bôi** | Transaction | 14800 | N/A | Low (5) | N/A | data/seo_insider/advance_search_report.csv | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 3 | Tổng hợp Hòa Bình | Tổng hợp | **tân lạc** | Informational | 12100 | N/A | Low (0) | N/A | data/seo_insider/advance_search_report.csv | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 4 | Mai Châu | Địa danh tham quan / Văn hóa - Lịch sử | **bản lác** | Commercial Investigation | 9900 | N/A | Low (1) | N/A | data/seo_insider/advance_search_report.csv | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 5 | Tổng hợp Hòa Bình | Tổng hợp | **somerset hoa binh hanoi** | Commercial Investigation | 6600 | N/A | Low (0) | N/A | data/seo_insider/advance_search_report.csv | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 6 | Homestay Hòa Bình | Lưu trú | **homestay mai châu** | Transaction | 1500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 7 | Homestay Hòa Bình | Lưu trú | **homestay thung nai** | Transaction | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 8 | Homestay Hòa Bình | Lưu trú | **homestay kim bôi** | Commercial Investigation | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 9 | Khách sạn Hòa Bình | Lưu trú | **khách sạn hoà bình** | Transaction | 3000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 10 | Khách sạn Hòa Bình | Lưu trú | **khách sạn mai châu** | Transaction | 2000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 11 | Khách sạn Hòa Bình | Lưu trú | **khách sạn kim bôi** | Transaction | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 12 | Khách sạn Hòa Bình | Lưu trú | **mai chau ecolodge** | Transaction | 1500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 13 | Khách sạn Hòa Bình | Lưu trú | **mandala retreat kim bôi** | Transaction | 800 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 14 | Khách sạn Hòa Bình | Lưu trú | **hoa viên hotel kim bôi** | Transaction | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 15 | Khách sạn Hòa Bình | Lưu trú | **sol bungalow mai châu** | Transaction | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 16 | Khách sạn Hòa Bình | Lưu trú | **mai chau lodge** | Transaction | 800 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 17 | Khách sạn Hòa Bình | Lưu trú | **đặt phòng khách sạn hoà bình** | Transaction | 300 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 18 | Khách sạn Hòa Bình | Lưu trú | **hasu village hoà bình** | Commercial Investigation | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 19 | Khách sạn Hòa Bình | Lưu trú | **đặt phòng mai châu ecolodge** | Commercial Investigation | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 20 | Resort Hòa Bình | Lưu trú | **giá phòng serena resort kim bôi** | Transaction | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 21 | Resort Hòa Bình | Lưu trú | **resort hoà bình** | Transaction | 2500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 22 | Resort Hòa Bình | Lưu trú | **resort mai châu** | Transaction | 2000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 23 | Resort Hòa Bình | Lưu trú | **resort kim bôi** | Transaction | 2500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 24 | Resort Hòa Bình | Lưu trú | **mai chau hideaway** | Transaction | 2000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 25 | Resort Hòa Bình | Lưu trú | **avana retreat mai châu** | Transaction | 1500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 26 | Resort Hòa Bình | Lưu trú | **an lạc resort kim bôi** | Transaction | 800 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 27 | Resort Hòa Bình | Lưu trú | **venus resort kim bôi** | Transaction | 800 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 28 | Resort Hòa Bình | Lưu trú | **mai chau mountain view resort** | Transaction | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 29 | Resort Hòa Bình | Lưu trú | **v_resort kim bôi** | Transaction | 1500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 30 | Resort Hòa Bình | Lưu trú | **ivory villas & resort hoà bình** | Transaction | 1500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 31 | Resort Hòa Bình | Lưu trú | **sakana resort hoà bình** | Transaction | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 32 | Resort Hòa Bình | Lưu trú | **la saveur de hoa binh resort** | Transaction | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 33 | Resort Hòa Bình | Lưu trú | **review serena resort kim bôi** | Commercial Investigation | 800 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 34 | Resort Hòa Bình | Lưu trú | **review mai chau hideaway** | Commercial Investigation | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 35 | Resort Hòa Bình | Lưu trú | **cullinan resort hoà bình** | Commercial Investigation | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 36 | Resort Hòa Bình | Lưu trú | **resort thung nai** | Commercial Investigation | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 37 | Sài Gòn Trip | Lưu trú | **khách sạn sài gòn hoà bình** | Commercial Investigation | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 38 | Thanh Hóa Trip | Lưu trú | **khách sạn mường thanh hoà bình** | Commercial Investigation | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 39 | Các điểm tham quan khác Hòa Bình | Địa danh tham quan / Văn hóa - Lịch sử | **thác mu hoà bình** | Informational | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 40 | Di chuyển Hòa Bình | Di chuyển | **taxi hoà bình** | Transaction | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 41 | Di chuyển Hòa Bình | Di chuyển | **tour hoà bình 1 ngày** | Transaction | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 42 | Di chuyển Hòa Bình | Di chuyển | **tour hoà bình 2 ngày 1 đêm** | Transaction | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 43 | Di chuyển Hòa Bình | Di chuyển | **tour mai châu 2 ngày 1 đêm** | Transaction | 1500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 44 | Di chuyển Hòa Bình | Di chuyển | **tour kim bôi 1 ngày** | Transaction | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 45 | Di chuyển Hòa Bình | Di chuyển | **tour kim bôi 2 ngày 1 đêm** | Transaction | 800 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 46 | Di chuyển Hòa Bình | Di chuyển | **tour thung nai 1 ngày** | Transaction | 800 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 47 | Di chuyển Hòa Bình | Di chuyển | **tour thung nai 2 ngày 1 đêm** | Transaction | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 48 | Di chuyển Hòa Bình | Di chuyển | **ve tàu thung nai** | Transaction | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 49 | Di chuyển Hòa Bình | Di chuyển | **nhà xe đi hoà bình** | Commercial Investigation | 800 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 50 | Di chuyển Hòa Bình | Di chuyển | **xe máy đi hoà bình** | Commercial Investigation | 300 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 51 | Di chuyển Hòa Bình | Di chuyển | **tour trekking mai châu** | Commercial Investigation | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 52 | Di chuyển Hòa Bình | Di chuyển | **di chuyển từ hoà bình đến mai châu** | Commercial Investigation | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 53 | Di chuyển Hòa Bình | Di chuyển | **tàu tham quan hồ hoà bình** | Commercial Investigation | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 54 | Di chuyển Hòa Bình | Di chuyển | **xe đi kim bôi** | Commercial Investigation | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 55 | Hà Nội Trip | Di chuyển | **xe ghép hoà bình hà nội** | Commercial Investigation | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 56 | Hà Nội Trip | Di chuyển | **xe bus hoà bình hà nội** | Commercial Investigation | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 57 | Hà Nội Trip | Tổng hợp | **khoảng cách hà nội hoà bình** | Informational | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 58 | Mai Châu | Địa danh tham quan / Văn hóa - Lịch sử | **du lịch mai châu** | Informational | 3000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 59 | Mai Châu | Địa danh tham quan / Văn hóa - Lịch sử | **bản lác mai châu** | Informational | 2000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 60 | Mai Châu | Địa danh tham quan / Văn hóa - Lịch sử | **du lịch bản lác** | Informational | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 61 | Mai Châu | Địa danh tham quan / Văn hóa - Lịch sử | **thung lũng mai châu** | Informational | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 62 | Mai Châu | Địa danh tham quan / Văn hóa - Lịch sử | **thời tiết mai châu hoà bình** | Informational | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 63 | Mai Châu | Địa danh tham quan / Văn hóa - Lịch sử | **lịch trình đi mai châu** | Informational | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 64 | Mai Châu | Địa danh tham quan / Văn hóa - Lịch sử | **hang chiều mai châu** | Informational | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 65 | Mai Châu | Địa danh tham quan / Văn hóa - Lịch sử | **combo mai châu** | Transaction | 800 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 66 | Mai Châu | Địa danh tham quan / Văn hóa - Lịch sử | **đi mai châu mùa nào đẹp** | Transaction | 300 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 67 | Mai Châu | Địa danh tham quan / Văn hóa - Lịch sử | **mùa vàng mai châu** | Transaction | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 68 | Mai Châu | Địa danh tham quan / Văn hóa - Lịch sử | **kinh nghiệm du lịch mai châu** | Commercial Investigation | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 69 | Mai Châu | Địa danh tham quan / Văn hóa - Lịch sử | **mai châu có gì chơi** | Commercial Investigation | 800 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 70 | Mai Châu | Địa danh tham quan / Văn hóa - Lịch sử | **trecking mai châu** | Informational | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 71 | Mai Châu | Địa danh tham quan / Văn hóa - Lịch sử | **thác gò lào mai châu** | Informational | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 72 | Mai Châu | Địa danh tham quan / Văn hóa - Lịch sử | **cột cờ mai châu** | Informational | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 73 | Mai Châu | Địa danh tham quan / Văn hóa - Lịch sử | **bản bước mai châu** | Informational | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 74 | Mai Châu | Địa danh tham quan / Văn hóa - Lịch sử | **nhà sàn mai châu** | Informational | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 75 | Suối khoáng Kim Bôi | Địa danh tham quan / Văn hóa - Lịch sử | **suối khoáng kim bôi** | Informational | 3000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 76 | Suối khoáng Kim Bôi | Địa danh tham quan / Văn hóa - Lịch sử | **tắm khoáng kim bôi** | Informational | 1500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 77 | Suối khoáng Kim Bôi | Địa danh tham quan / Văn hóa - Lịch sử | **khu du lịch suối khoáng kim bôi** | Informational | 1500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 78 | Suối khoáng Kim Bôi | Địa danh tham quan / Văn hóa - Lịch sử | **du lịch kim bôi** | Informational | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 79 | Suối khoáng Kim Bôi | Địa danh tham quan / Văn hóa - Lịch sử | **voucher serena kim bôi** | Transaction | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 80 | Suối khoáng Kim Bôi | Địa danh tham quan / Văn hóa - Lịch sử | **kinh nghiệm du lịch kim bôi** | Commercial Investigation | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 81 | Suối khoáng Kim Bôi | Địa danh tham quan / Văn hóa - Lịch sử | **suối nước nóng kim bôi** | Informational | 3000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 82 | Suối khoáng Kim Bôi | Địa danh tham quan / Văn hóa - Lịch sử | **nghỉ dưỡng kim bôi** | Informational | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 83 | Thung Nai & Thác Bờ | Địa danh tham quan / Văn hóa - Lịch sử | **thung nai hoà bình** | Informational | 2500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 84 | Thung Nai & Thác Bờ | Địa danh tham quan / Văn hóa - Lịch sử | **du lịch thung nai** | Informational | 1500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 85 | Thung Nai & Thác Bờ | Địa danh tham quan / Văn hóa - Lịch sử | **động thác bờ** | Informational | 800 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 86 | Thung Nai & Thác Bờ | Địa danh tham quan / Văn hóa - Lịch sử | **đền chúa thác bờ** | Informational | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 87 | Thung Nai & Thác Bờ | Địa danh tham quan / Văn hóa - Lịch sử | **thuê thuyền thung nai** | Transaction | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 88 | Thung Nai & Thác Bờ | Địa danh tham quan / Văn hóa - Lịch sử | **kinh nghiệm du lịch thung nai** | Commercial Investigation | 800 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 89 | Thung Nai & Thác Bờ | Địa danh tham quan / Văn hóa - Lịch sử | **đảo dừa thung nai** | Informational | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 90 | Thung Nai & Thác Bờ | Địa danh tham quan / Văn hóa - Lịch sử | **cắm trại thung nai** | Informational | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 91 | Thung Nai & Thác Bờ | Địa danh tham quan / Văn hóa - Lịch sử | **đền mẫu thác bờ** | Informational | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 92 | Thung Nai & Thác Bờ | Địa danh tham quan / Văn hóa - Lịch sử | **hang trần thung nai** | Informational | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 93 | Thung Nai & Thác Bờ | Địa danh tham quan / Văn hóa - Lịch sử | **kdl sinh thái thung nai** | Informational | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 94 | Tổng hợp Hòa Bình | Tổng hợp | **các điểm du lịch hoà bình** | Informational | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 95 | Tổng hợp Hòa Bình | Tổng hợp | **địa điểm du lịch hoà bình** | Informational | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 96 | Tổng hợp Hòa Bình | Tổng hợp | **du lịch đèo thung khe** | Informational | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 97 | Tổng hợp Hòa Bình | Tổng hợp | **đặc sản hoà bình** | Informational | 800 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 98 | Tổng hợp Hòa Bình | Tổng hợp | **lợn mán hoà bình** | Informational | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 99 | Tổng hợp Hòa Bình | Tổng hợp | **giá vé tham quan thuỷ điện hoà bình** | Transaction | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 100 | Tổng hợp Hòa Bình | Tổng hợp | **combo du lịch hoà bình** | Transaction | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 101 | Tổng hợp Hòa Bình | Tổng hợp | **bảng giá vé tham quan hoà bình** | Transaction | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 102 | Tổng hợp Hòa Bình | Tổng hợp | **kinh nghiệm du lịch hoà bình** | Commercial Investigation | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 103 | Tổng hợp Hòa Bình | Tổng hợp | **review du lịch hoà bình** | Commercial Investigation | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 104 | Tổng hợp Hòa Bình | Tổng hợp | **kinh nghiệm đi đèo đá trắng** | Commercial Investigation | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 105 | Tổng hợp Hòa Bình | Tổng hợp | **văn hoá đồng bào hoà bình** | Informational | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 106 | Tổng hợp Hòa Bình | Tổng hợp | **bản ngòi núi hoà bình** | Informational | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 107 | Tổng hợp Hòa Bình | Tổng hợp | **đèo đá trắng hoà bình** | Informational | 2000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 108 | Tổng hợp Hòa Bình | Tổng hợp | **check in đèo đá trắng** | Informational | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 109 | Tổng hợp Hòa Bình | Tổng hợp | **hang xăm hoà bình** | Informational | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 110 | Xe khách/Limousine đi Hòa Bình | Di chuyển | **xe limousine đi hoà bình** | Transaction | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 111 | Xe khách/Limousine đi Hòa Bình | Di chuyển | **xe limousine đi mai châu** | Transaction | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 112 | Xe khách/Limousine đi Hòa Bình | Di chuyển | **thuê xe limousine đi hoà bình** | Transaction | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 113 | Xe khách/Limousine đi Hòa Bình | Di chuyển | **xe khách đi hoà bình** | Commercial Investigation | 800 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 114 | Xe khách/Limousine đi Hòa Bình | Di chuyển | **xe khách đi mai châu** | Commercial Investigation | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 115 | Ăn uống Hòa Bình | Ẩm thực (F&B) | **nhà hàng ngon ở hoà bình** | Informational | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 116 | Ăn uống Hòa Bình | Ẩm thực (F&B) | **quán ăn ngon ở hoà bình** | Informational | 500 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 117 | Điểm tham quan Hòa Bình | Địa danh tham quan / Văn hóa - Lịch sử | **cửu thác tú sơn** | Informational | 1000 | N/A | N/A (web) | N/A | web (hoa-binh.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 118 | Tổng hợp Hòa Bình | Tổng hợp | **du lịch hòa bình** | Informational | N/A | 20% | Trend SI:4 20% | N/A | data/google_trend/searched_with_rising-queries_VN_20250210-1752_20260210-1752.csv; data/google_trend/searched_with_top-queries_VN_20250210-1752_20260210-1752.csv | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |

## 5. QUALITY GATE (AUTO-CHECK)
- **Intent distribution**: Informational=44, Commercial Investigation=29, Transaction=51
- [x] PASS: Taxonomy (landmark không được nằm trong F&B)
- [x] PASS: Geo-scope (out-of-scope phải tách cluster '* Trip')
- [x] PASS: Source (mỗi keyword phải có source folder/file)
- [x] PASS: Intent ratio (check 20/40/40 nếu đủ 100 keywords)
