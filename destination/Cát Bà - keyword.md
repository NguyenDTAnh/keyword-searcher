# REPORT KEYWORD PLANNER: CÁT BÀ

## 1. TỔNG QUAN CHIẾN LƯỢC
- **Mục tiêu**: Chiếm lĩnh thị trường du lịch Cát Bà cho vietgoing.com bằng dữ liệu thực tế (GSC) + xu hướng (Trend/SEO Insider).
- **Tổng số từ khóa**: 100
- **Nguồn dữ liệu**:
  - `web (cat-ba.csv)` (92 từ khóa)
  - `data/google_search_console/Queries.csv` (5 từ khóa)
  - `data/seo_insider/advance_search_report.csv` (2 từ khóa)
  - `data/google_trend/searched_with_top-queries_VN_20250210-1748_20260210-1748.csv` (1 từ khóa)

## 2. TOP TỪ KHÓA TIỀM NĂNG (THEO SPI - GROUP A)
> **Action Plan**: Đây là các từ khóa đang perform tốt nhất, cần tối ưu để scale.

| Keyword | Cluster | CTR | Action Plan |
| :--- | :--- | :--- | :--- |
| **khách sạn giang hà cát bà** | Khách sạn Cát Bà | 32.26% | Push Top |
| **giang hà hotel cát bà** | Khách sạn Cát Bà | 15.28% | Push Top |
| **hà my hotel cát bà** | Khách sạn Cát Bà | 7.92% | Push Top |
| **khách sạn 3 sao cát bà** | Khách sạn Cát Bà | 2.26% | Push Top |
| **eden hotel cát bà** | Khách sạn Cát Bà | 0.64% | Push Top |

## 3. NHÓM 1: TỪ KHÓA CŨ (TỐI ƯU HÓA TÀI SẢN HIỆN CÓ - GROUP A)
> **Tiêu chí sắp xếp**: CTR giảm dần > Impressions giảm dần. Tập trung tối ưu On-page và Internal Link để đẩy Top.

| STT | Cluster | Cluster Type | Keyword | Intent | Imp | Clicks | CTR | Source | Action Plan |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Khách sạn Cát Bà | Lưu trú | **khách sạn giang hà cát bà** | Transaction | 186 | 60 | 32.26% | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Cát Bà' |
| 2 | Khách sạn Cát Bà | Lưu trú | **giang hà hotel cát bà** | Transaction | 216 | 33 | 15.28% | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Cát Bà' |
| 3 | Khách sạn Cát Bà | Lưu trú | **hà my hotel cát bà** | Transaction | 265 | 21 | 7.92% | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Cát Bà' |
| 4 | Khách sạn Cát Bà | Lưu trú | **khách sạn 3 sao cát bà** | Commercial Investigation | 576 | 13 | 2.26% | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 5 | Khách sạn Cát Bà | Lưu trú | **eden hotel cát bà** | Commercial Investigation | 1730 | 11 | 0.64% | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |

## 4. NHÓM 2: TỪ KHÓA MỚI (KHAI PHÁ THỊ TRƯỜNG - GROUP B)
> **Tiêu chí sắp xếp**: Score tổng hợp (Volume cao + Cạnh tranh thấp/trung bình -> YoY tăng + Bid cao).

| STT | Cluster | Cluster Type | Keyword | Intent | Vol | YoY | KD/Comp | Bid (High) | Source | Action Plan |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Vịnh Lan Hạ | Địa danh tham quan / Văn hóa - Lịch sử | **vịnh lan hạ** | Commercial Investigation | 18100 | N/A | Low (8) | N/A | data/seo_insider/advance_search_report.csv | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 2 | Resort Cát Bà | Lưu trú | **flamingo cát bà beach resort** | Commercial Investigation | 9900 | N/A | Low (6) | N/A | data/seo_insider/advance_search_report.csv | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 3 | Khách sạn Cát Bà | Lưu trú | **khách sạn cát bà** | Commercial Investigation | N/A | -10% | Trend SI:8 -10% | N/A | data/google_trend/searched_with_top-queries_VN_20250210-1748_20260210-1748.csv | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 4 | Homestay Cát Bà | Lưu trú | **đặt homestay giá rẻ cát bà** | Transaction | 400 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 5 | Homestay Cát Bà | Lưu trú | **homestay cát bà** | Commercial Investigation | 2000 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 6 | Homestay Cát Bà | Lưu trú | **list homestay cát bà đẹp** | Commercial Investigation | 400 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 7 | Khách sạn Cát Bà | Lưu trú | **giá phòng khách sạn cát bà** | Transaction | 500 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 8 | Khách sạn Cát Bà | Lưu trú | **đặt phòng khách sạn tại cát bà giá rẻ** | Transaction | 450 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 9 | Khách sạn Cát Bà | Lưu trú | **đặt phòng khách sạn cát bà** | Commercial Investigation | 800 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 10 | Khách sạn Cát Bà | Lưu trú | **top khách sạn cát bà** | Commercial Investigation | 500 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 11 | Khách sạn Cát Bà | Lưu trú | **so sánh các khách sạn cát bà** | Commercial Investigation | 300 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 12 | Khách sạn Cát Bà | Lưu trú | **khách sạn 5 sao tốt nhất cát bà** | Commercial Investigation | 350 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 13 | Resort Cát Bà | Lưu trú | **booking resort cát bà** | Transaction | 600 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 14 | Resort Cát Bà | Lưu trú | **resort cát bà** | Commercial Investigation | 3500 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 15 | Resort Cát Bà | Lưu trú | **top resort cát bà** | Commercial Investigation | 400 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 16 | Di chuyển Cát Bà | Di chuyển | **tour cát bà 2 ngày 1 đêm** | Transaction | 1500 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 17 | Di chuyển Cát Bà | Di chuyển | **tour cát bà 3 ngày 2 đêm** | Transaction | 1200 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 18 | Di chuyển Cát Bà | Di chuyển | **tour vịnh lan hạ 1 ngày** | Transaction | 800 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 19 | Di chuyển Cát Bà | Di chuyển | **giá tour vịnh lan hạ** | Transaction | 500 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 20 | Di chuyển Cát Bà | Di chuyển | **vé tour vịnh lan hạ 2 ngày 1 đêm** | Transaction | 350 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 21 | Di chuyển Cát Bà | Di chuyển | **voucher tour cát bà** | Transaction | 300 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 22 | Di chuyển Cát Bà | Di chuyển | **tour cát bà** | Commercial Investigation | 2500 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 23 | Di chuyển Cát Bà | Di chuyển | **tour vịnh lan hạ** | Commercial Investigation | 2000 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 24 | Di chuyển Cát Bà | Di chuyển | **đặt tour vịnh lan hạ** | Commercial Investigation | 450 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 25 | Hà Nội Trip | Di chuyển | **limousine hà nội cát bà** | Transaction | 800 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 26 | Hà Nội Trip | Di chuyển | **thuê xe du lịch hà nội cát bà** | Transaction | 200 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 27 | Hà Nội Trip | Di chuyển | **xe ghép cát bà hà nội giá rẻ** | Transaction | 350 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 28 | Hà Nội Trip | Di chuyển | **xe từ hà nội đi cát bà** | Commercial Investigation | 1800 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 29 | Hà Nội Trip | Di chuyển | **xe 16 chỗ hà nội cát bà** | Commercial Investigation | 250 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 30 | Hải Phòng Trip | Di chuyển | **xe limousine đi cát bà từ hải phòng** | Transaction | 350 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 31 | Hải sản & Ăn uống Cát Bà | Ẩm thực (F&B) | **nhà hàng cát bà** | Informational | 700 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 32 | Hải sản & Ăn uống Cát Bà | Ẩm thực (F&B) | **quán ăn ngon cát bà** | Informational | 800 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 33 | Hải sản & Ăn uống Cát Bà | Ẩm thực (F&B) | **các quán ăn ngon ở cát bà** | Informational | 450 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 34 | Hải sản & Ăn uống Cát Bà | Ẩm thực (F&B) | **review nhà hàng ngon ở cát bà** | Commercial Investigation | 250 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 35 | Hải sản & Ăn uống Cát Bà | Ẩm thực (F&B) | **top nhà hàng tại cát bà** | Commercial Investigation | 300 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 36 | Sài Gòn Trip | Di chuyển | **tour sài gòn cát bà** | Commercial Investigation | 300 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 37 | Tàu phà đi Cát Bà | Di chuyển | **vé tàu đi cát bà** | Transaction | 1500 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 38 | Tàu phà đi Cát Bà | Di chuyển | **thuê tàu thăm vịnh lan hạ** | Transaction | 450 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 39 | Tàu phà đi Cát Bà | Di chuyển | **thuê tàu cao tốc ra đào cát bà** | Transaction | 400 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 40 | Tàu phà đi Cát Bà | Di chuyển | **tàu cao tốc đi cát bà** | Commercial Investigation | 1000 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 41 | Tàu phà đi Cát Bà | Di chuyển | **giờ tàu chạy bến gót** | Commercial Investigation | 600 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 42 | Tổng hợp Cát Bà | Tổng hợp | **du lịch cát bà** | Informational | 5000 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 43 | Tổng hợp Cát Bà | Tổng hợp | **chơi gì ở cát bà** | Informational | 800 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 44 | Tổng hợp Cát Bà | Tổng hợp | **nên đi cát bà tháng mấy** | Informational | 500 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 45 | Tổng hợp Cát Bà | Tổng hợp | **địa điểm du lịch cát bà** | Informational | 900 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 46 | Tổng hợp Cát Bà | Tổng hợp | **hải sản cát bà** | Informational | 1000 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 47 | Tổng hợp Cát Bà | Tổng hợp | **cẩm nang du lịch cát bà** | Informational | 200 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 48 | Tổng hợp Cát Bà | Tổng hợp | **du thuyền mường thanh cát bà** | Informational | 300 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 49 | Tổng hợp Cát Bà | Tổng hợp | **khu check in mới ở cát bà** | Informational | 250 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 50 | Tổng hợp Cát Bà | Tổng hợp | **nên ăn gì ở chợ đêm cát bà** | Informational | 400 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 51 | Tổng hợp Cát Bà | Tổng hợp | **combo du lịch cát bà** | Transaction | 600 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 52 | Tổng hợp Cát Bà | Tổng hợp | **booking flamingo cát bà** | Transaction | 400 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 53 | Tổng hợp Cát Bà | Tổng hợp | **địa chỉ mua sỉ hải sản cát bà** | Transaction | 200 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 54 | Tổng hợp Cát Bà | Tổng hợp | **giá hải sản cát bà** | Transaction | 400 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 55 | Tổng hợp Cát Bà | Tổng hợp | **bảng giá dịch vụ cát bà** | Transaction | 250 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 56 | Tổng hợp Cát Bà | Tổng hợp | **đánh giá flamingo cát bà** | Transaction | 300 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 57 | Tổng hợp Cát Bà | Tổng hợp | **đánh giá mgallery cát bà** | Transaction | 300 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 58 | Tổng hợp Cát Bà | Tổng hợp | **kinh nghiệm du lịch cát bà** | Commercial Investigation | 3000 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 59 | Tổng hợp Cát Bà | Tổng hợp | **review hải sản cát bà** | Commercial Investigation | 300 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 60 | Tổng hợp Cát Bà | Tổng hợp | **kinh nghiệm ở mgalery cát bà** | Commercial Investigation | 200 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 61 | Vườn quốc gia Cát Bà | Địa danh tham quan / Văn hóa - Lịch sử | **vườn quốc gia cát bà** | Transaction | 2000 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 62 | Vườn quốc gia Cát Bà | Địa danh tham quan / Văn hóa - Lịch sử | **chi phí tham quan vườn quốc gia cát bà** | Transaction | 250 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 63 | Vịnh Lan Hạ | Địa danh tham quan / Văn hóa - Lịch sử | **du thuyền lan hạ** | Informational | 1500 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 64 | Vịnh Lan Hạ | Địa danh tham quan / Văn hóa - Lịch sử | **lịch sử vịnh lan hạ cát bà** | Informational | 150 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 65 | Vịnh Lan Hạ | Địa danh tham quan / Văn hóa - Lịch sử | **hình ảnh du thuyền lan hạ** | Informational | 250 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 66 | Vịnh Lan Hạ | Địa danh tham quan / Văn hóa - Lịch sử | **đặt thuyền tham quan vịnh lan hạ** | Informational | 300 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 67 | Vịnh Lan Hạ | Địa danh tham quan / Văn hóa - Lịch sử | **voucher du thuyền lan hạ** | Transaction | 400 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 68 | Vịnh Lan Hạ | Địa danh tham quan / Văn hóa - Lịch sử | **giá vé du thuyền lan hạ** | Transaction | 500 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 69 | Vịnh Lan Hạ | Địa danh tham quan / Văn hóa - Lịch sử | **giá thuê cano đi vịnh lan hạ** | Transaction | 400 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 70 | Vịnh Lan Hạ | Địa danh tham quan / Văn hóa - Lịch sử | **kinh nghiệm đi vịnh lan hạ** | Commercial Investigation | 500 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 71 | Vịnh Lan Hạ | Địa danh tham quan / Văn hóa - Lịch sử | **vé thăm quan vịnh lan hạ** | Commercial Investigation | 250 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 72 | Vịnh Lan Hạ | Địa danh tham quan / Văn hóa - Lịch sử | **review du thuyền lan hạ** | Commercial Investigation | 400 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 73 | Vịnh Lan Hạ | Địa danh tham quan / Văn hóa - Lịch sử | **đặt vé du thuyền lan hạ** | Commercial Investigation | 600 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 74 | Xe đi Cát Bà | Di chuyển | **kinh nghiệm thuê xe máy cát bà** | Transaction | 200 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 75 | Xe đi Cát Bà | Di chuyển | **giá thuê xe 16 chỗ đi cát bà** | Transaction | 250 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 76 | Xe đi Cát Bà | Di chuyển | **xe đi cát bà** | Commercial Investigation | 3000 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 77 | Xe đi Cát Bà | Di chuyển | **xe khách đi cát bà** | Commercial Investigation | 1200 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 78 | Xe đi Cát Bà | Di chuyển | **nhà xe hoàng long đi cát bà** | Commercial Investigation | 200 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 79 | Xe đi Cát Bà | Di chuyển | **nhà xe daiichi cát bà** | Commercial Investigation | 300 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 80 | Xe đi Cát Bà | Di chuyển | **nhà xe good morning cát bà** | Commercial Investigation | 200 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 81 | Xe đi Cát Bà | Di chuyển | **xe hà nội cát hải** | Commercial Investigation | 400 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 82 | Ăn uống Cát Bà | Ẩm thực (F&B) | **giá ăn uống ở cát bà** | Transaction | 300 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 83 | Điểm tham quan Cát Bà | Địa danh tham quan / Văn hóa - Lịch sử | **phà gót** | Informational | 3000 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 84 | Điểm tham quan Cát Bà | Địa danh tham quan / Văn hóa - Lịch sử | **cáp treo cát bà** | Informational | 2500 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 85 | Điểm tham quan Cát Bà | Địa danh tham quan / Văn hóa - Lịch sử | **tuyến phà gót cái viềng** | Informational | 350 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 86 | Điểm tham quan Cát Bà | Địa danh tham quan / Văn hóa - Lịch sử | **khoảng cách phà gót và cáp treo** | Informational | 250 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 87 | Điểm tham quan Cát Bà | Địa danh tham quan / Văn hóa - Lịch sử | **giá vé cáp treo cát bà** | Transaction | 1000 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 88 | Điểm tham quan Cát Bà | Địa danh tham quan / Văn hóa - Lịch sử | **giá phà gót** | Transaction | 800 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 89 | Điểm tham quan Cát Bà | Địa danh tham quan / Văn hóa - Lịch sử | **giá vé phà gót** | Transaction | 800 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 90 | Điểm tham quan Cát Bà | Địa danh tham quan / Văn hóa - Lịch sử | **mã giảm giá vé cáp treo cát bà** | Transaction | 200 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 91 | Điểm tham quan Cát Bà | Địa danh tham quan / Văn hóa - Lịch sử | **vé phà gót** | Commercial Investigation | 500 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 92 | Điểm tham quan Cát Bà | Địa danh tham quan / Văn hóa - Lịch sử | **đặt vé phà gót online** | Commercial Investigation | 400 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 93 | Điểm tham quan Cát Bà | Địa danh tham quan / Văn hóa - Lịch sử | **vé cáp treo sunworld cát bà** | Commercial Investigation | 600 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 94 | Điểm tham quan Cát Bà | Địa danh tham quan / Văn hóa - Lịch sử | **đặt vé cáp treo cát bà** | Commercial Investigation | 300 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 95 | Đà Nẵng Trip | Di chuyển | **tour cát bà từ đà nẵng giá rẻ** | Transaction | 100 | N/A | N/A (web) | N/A | web (cat-ba.csv) | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |

## 5. QUALITY GATE (AUTO-CHECK)
- **Intent distribution**: Informational=20, Commercial Investigation=40, Transaction=40
- [x] PASS: Taxonomy (landmark không được nằm trong F&B)
- [x] PASS: Geo-scope (out-of-scope phải tách cluster '* Trip')
- [x] PASS: Source (mỗi keyword phải có source folder/file)
- [x] PASS: Intent ratio (100 keywords phải đạt 20/40/40)
