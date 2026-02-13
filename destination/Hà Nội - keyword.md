# REPORT KEYWORD PLANNER: HÀ NỘI

## 1. TỔNG QUAN CHIẾN LƯỢC
- **Mục tiêu**: Chiếm lĩnh thị trường du lịch Hà Nội cho vietgoing.com bằng dữ liệu thực tế (GSC) + xu hướng (Trend/SEO Insider).
- **Tổng số từ khóa**: 121
- **Nguồn dữ liệu**:
  - `data/google_search_console/Queries.csv` (79 từ khóa)
  - `Web Suggest` (27 từ khóa)
  - `data/google_trend/searched_with_top-queries_VN_20250210-1749_20260210-1749.csv` (7 từ khóa)
  - `data/google_trend/searched_with_rising-queries_VN_20250210-1752_20260210-1752.csv` (4 từ khóa)
  - `data/google_trend/searched_with_top-queries_VN_20250210-1748_20260210-1748.csv` (2 từ khóa)
  - `data/google_trend/searched_with_top-queries_VN_20250210-1750_20260210-1750.csv; data/google_search_console/Queries.csv` (1 từ khóa)
  - `data/google_trend/searched_with_rising-queries_VN_20250210-1752_20260210-1752.csv; data/google_trend/searched_with_top-queries_VN_20250210-1752_20260210-1752.csv; data/google_trend/searched_with_top-queries_VN_20250210-1750_20260210-1750.csv` (1 từ khóa)

## 2. TOP TỪ KHÓA TIỀM NĂNG (THEO SPI - GROUP A)
> **Action Plan**: Đây là các từ khóa đang perform tốt nhất, cần tối ưu để scale.

| Keyword | Cluster | CTR | Action Plan |
| :--- | :--- | :--- | :--- |
| **khách sạn 4 sao hà nội** | Khách sạn Hà Nội | 2.49 | Push Top |
| **khách sạn gần phố đi bộ hồ gươm** | Khách sạn Hà Nội | 6.46 | Push Top |
| **khách sạn 5 sao hà nội** | Khách sạn Hà Nội | 0.76 | Push Top |
| **khách sạn ở phố cổ hà nội giá rẻ** | Khách sạn Phố Cổ | 4.53 | Push Top |
| **tòa soạn báo hà nội mới** | Tổng hợp Hà Nội | 4.37 | Push Top |
| **khách sạn gần hồ gươm giá rẻ** | Khách sạn Hà Nội | 4.26 | Push Top |
| **khách sạn gần phố đi bộ hà nội** | Khách sạn Hà Nội | 5.05 | Push Top |
| **nhà nghỉ gần phố đi bộ hồ gươm** | Khách sạn Hà Nội | 7.34 | Push Top |
| **khách sạn phố cổ hà nội** | Khách sạn Phố Cổ | 0.86 | Push Top |
| **hồ hoàn kiếm** | Hồ Hoàn Kiếm & Phố đi bộ | 0.59 | Push Top |

## 3. NHÓM 1: TỪ KHÓA CŨ (TỐI ƯU HÓA TÀI SẢN HIỆN CÓ - GROUP A)
> **Tiêu chí sắp xếp**: CTR giảm dần > Impressions giảm dần. Tập trung tối ưu On-page và Internal Link để đẩy Top.

| STT | Cluster | Cluster Type | Keyword | Intent | Imp | Clicks | CTR | Source | Action Plan |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Tổng hợp Hà Nội | Tổng hợp | **19c hoàng diệu hà nội** | Informational | 76 | 11 | 14.47 | data/google_search_console/Queries.csv | Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3 |
| 2 | Khách sạn Hà Nội | Lưu trú | **khách sạn lê văn lương hà nội** | Commercial Investigation | 94 | 11 | 11.7 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 3 | Khách sạn/Homestay Hồ Tây | Lưu trú | **khách sạn tình yêu hồ tây** | Commercial Investigation | 357 | 41 | 11.48 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 4 | Khách sạn Phố Cổ | Lưu trú | **khách sạn 5 sao phố cổ** | Commercial Investigation | 342 | 36 | 10.53 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 5 | Điểm tham quan Hà Nội | Địa danh tham quan / Văn hóa - Lịch sử | **19c phố hoàng diệu hoàng thành thăng long hà nội** | Informational | 143 | 15 | 10.49 | data/google_search_console/Queries.csv | Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3 |
| 6 | Khách sạn Hà Nội | Lưu trú | **resort long biên** | Commercial Investigation | 99 | 10 | 10.1 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 7 | Tổng hợp Hà Nội | Tổng hợp | **19c phố hoàng diệu hà nội** | Informational | 174 | 17 | 9.77 | data/google_search_console/Queries.csv | Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3 |
| 8 | Khách sạn Hà Nội | Lưu trú | **nhà nghỉ giá rẻ gần phố đi bộ hà nội** | Transaction | 306 | 28 | 9.15 | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hà Nội' |
| 9 | Khách sạn Phố Cổ | Lưu trú | **khách sạn 4 sao phố cổ** | Commercial Investigation | 430 | 39 | 9.07 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 10 | Tổng hợp Hà Nội | Tổng hợp | **địa chỉ làng lụa vạn phúc hà đông** | Informational | 113 | 10 | 8.85 | data/google_search_console/Queries.csv | Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3 |
| 11 | Tổng hợp Hà Nội | Tổng hợp | **toà soạn báo hà nội mới** | Informational | 427 | 36 | 8.43 | data/google_search_console/Queries.csv | Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3 |
| 12 | Khách sạn Hà Nội | Lưu trú | **khách sạn 4 sao gần hồ hoàn kiếm, hà nội** | Commercial Investigation | 710 | 59 | 8.31 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 13 | Khách sạn Hà Nội | Lưu trú | **khách sạn cát linh hà nội** | Commercial Investigation | 183 | 15 | 8.2 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 14 | Khách sạn Hà Nội | Lưu trú | **khách sạn 5 sao hoàn kiếm** | Commercial Investigation | 189 | 15 | 7.94 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 15 | Khách sạn Hà Nội | Lưu trú | **khách sạn 5 sao hà nội, gần hồ hoàn kiếm** | Commercial Investigation | 274 | 21 | 7.66 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 16 | Khách sạn Hà Nội | Lưu trú | **khách sạn lò sũ hà nội** | Commercial Investigation | 171 | 13 | 7.6 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 17 | Khách sạn Hà Nội | Lưu trú | **nhà nghỉ gần phố đi bộ hồ gươm** | Commercial Investigation | 954 | 70 | 7.34 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 18 | Khách sạn Hà Nội | Lưu trú | **nhà nghỉ gần phố đi bộ hà nội** | Commercial Investigation | 590 | 43 | 7.29 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 19 | Khách sạn Phố Cổ | Lưu trú | **khách sạn 4 sao phố cổ hà nội** | Commercial Investigation | 857 | 60 | 7.0 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 20 | Hải Phòng Trip | Di chuyển | **tour hà nội hải phòng 1 ngày** | Transaction | 264 | 18 | 6.82 | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hà Nội' |
| 21 | Khách sạn Hà Nội | Lưu trú | **khách sạn gần phố đi bộ hồ gươm** | Commercial Investigation | 1749 | 113 | 6.46 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 22 | Khách sạn Phố Cổ | Lưu trú | **khách sạn phố cổ hà nội 4 sao** | Commercial Investigation | 718 | 44 | 6.13 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 23 | Khách sạn Phố Cổ | Lưu trú | **khách sạn 5 sao phố cổ hà nội** | Commercial Investigation | 663 | 39 | 5.88 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 24 | Tổng hợp Hà Nội | Tổng hợp | **hồ bán nguyệt hà nội** | Informational | 262 | 14 | 5.34 | data/google_search_console/Queries.csv | Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3 |
| 25 | Khách sạn Hà Nội | Lưu trú | **khách sạn 5 sao gần hồ gươm** | Commercial Investigation | 245 | 13 | 5.31 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 26 | Khách sạn Hà Nội | Lưu trú | **khách sạn gần phố đi bộ hà nội** | Commercial Investigation | 1385 | 70 | 5.05 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 27 | Khách sạn Phố Cổ | Lưu trú | **khách sạn ở phố cổ hà nội giá rẻ** | Transaction | 1942 | 88 | 4.53 | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hà Nội' |
| 28 | Tổng hợp Hà Nội | Tổng hợp | **tòa soạn báo hà nội mới** | Informational | 1739 | 76 | 4.37 | data/google_search_console/Queries.csv | Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3 |
| 29 | Di chuyển Hà Nội | Di chuyển | **tour hà nội 1 ngày giá cực rẻ** | Transaction | 951 | 41 | 4.31 | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hà Nội' |
| 30 | Khách sạn Hà Nội | Lưu trú | **khách sạn 4 sao gần hồ hoàn kiếm hà nội** | Commercial Investigation | 255 | 11 | 4.31 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 31 | Khách sạn Hà Nội | Lưu trú | **khách sạn gần hồ gươm giá rẻ** | Transaction | 1668 | 71 | 4.26 | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hà Nội' |
| 32 | Khách sạn Phố Cổ | Lưu trú | **khách sạn giá rẻ ở phố cổ hà nội** | Transaction | 358 | 15 | 4.19 | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hà Nội' |
| 33 | Tổng hợp Hà Nội | Tổng hợp | **19c hoàng diệu ba đình hà nội** | Informational | 335 | 14 | 4.18 | data/google_search_console/Queries.csv | Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3 |
| 34 | Khách sạn Hà Nội | Lưu trú | **khách sạn 4 sao trung tâm hà nội** | Commercial Investigation | 249 | 10 | 4.02 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 35 | Khách sạn Hà Nội | Lưu trú | **khách sạn gần hồ hoàn kiếm giá rẻ** | Transaction | 476 | 19 | 3.99 | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hà Nội' |
| 36 | Hải Phòng Trip | Di chuyển | **tour hà nội - hải phòng 1 ngày** | Transaction | 453 | 17 | 3.75 | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hà Nội' |
| 37 | Khách sạn Phố Cổ | Lưu trú | **khách sạn gần phố cổ hà nội giá rẻ** | Transaction | 593 | 22 | 3.71 | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hà Nội' |
| 38 | Khách sạn Phố Cổ | Lưu trú | **khách sạn phố cổ giá rẻ** | Transaction | 394 | 14 | 3.55 | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hà Nội' |
| 39 | Tổng hợp Hà Nội | Tổng hợp | **chuồn chuồn nghĩa lộ cách hà nội bao nhiều km** | Informational | 1413 | 50 | 3.54 | data/google_search_console/Queries.csv | Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3 |
| 40 | Tổng hợp Hà Nội | Tổng hợp | **toà soạn báo hà nội** | Informational | 795 | 28 | 3.52 | data/google_search_console/Queries.csv | Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3 |
| 41 | Khách sạn Hà Nội | Lưu trú | **khách sạn 5 sao gần hồ hoàn kiếm** | Commercial Investigation | 532 | 18 | 3.38 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 42 | Tổng hợp Hà Nội | Tổng hợp | **báo hà nội mới ở đâu** | Informational | 1072 | 36 | 3.36 | data/google_search_console/Queries.csv | Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3 |
| 43 | Khách sạn Hà Nội | Lưu trú | **khách sạn 5 sao hà nội gần hồ hoàn kiếm** | Commercial Investigation | 539 | 18 | 3.34 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 44 | Khách sạn Phố Cổ | Lưu trú | **khách sạn phố cổ hà nội giá rẻ** | Transaction | 1725 | 55 | 3.19 | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hà Nội' |
| 45 | Khách sạn Hà Nội | Lưu trú | **khách sạn phố cầu gỗ hà nội** | Commercial Investigation | 362 | 11 | 3.04 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 46 | Khách sạn/Homestay Hồ Tây | Lưu trú | **khách sạn view hồ tây** | Commercial Investigation | 1076 | 32 | 2.97 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 47 | Khách sạn Hà Nội | Lưu trú | **khách sạn 4 sao hà nội** | Commercial Investigation | 7743 | 193 | 2.49 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 48 | Khách sạn Phố Cổ | Lưu trú | **khách sạn hà nội gần phố cổ** | Commercial Investigation | 820 | 20 | 2.44 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 49 | Điểm tham quan Hà Nội | Địa danh tham quan / Văn hóa - Lịch sử | **19c phố hoàng diệu hoàng thành thăng long là ở đầu** | Informational | 829 | 20 | 2.41 | data/google_search_console/Queries.csv | Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3 |
| 50 | Văn Miếu Quốc Tử Giám | Địa danh tham quan / Văn hóa - Lịch sử | **thông tin về văn miếu quốc tử giám** | Commercial Investigation | 482 | 10 | 2.07 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 51 | Tam Đảo Trip | Di chuyển | **xe limousine hà nội tam đảo** | Transaction | 1042 | 21 | 2.02 | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hà Nội' |
| 52 | Khách sạn Hà Nội | Lưu trú | **khách sạn 4 sao tại hà nội** | Commercial Investigation | 890 | 18 | 2.02 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 53 | Khách sạn Hà Nội | Lưu trú | **khách sạn 4 sao ở hà nội** | Commercial Investigation | 1400 | 27 | 1.93 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 54 | Khách sạn Phố Cổ | Lưu trú | **khách sạn phố cổ hà nội 3 sao** | Commercial Investigation | 535 | 10 | 1.87 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 55 | Tổng hợp Hà Nội | Tổng hợp | **trụ sở báo hà nội mới** | Informational | 1245 | 23 | 1.85 | data/google_search_console/Queries.csv | Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3 |
| 56 | Tổng hợp Hà Nội | Tổng hợp | **địa chỉ báo hà nội mới** | Informational | 636 | 11 | 1.73 | data/google_search_console/Queries.csv | Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3 |
| 57 | Di chuyển Hà Nội | Di chuyển | **tour hà nội** | Commercial Investigation | 1518 | 26 | 1.71 | data/google_trend/searched_with_top-queries_VN_20250210-1750_20260210-1750.csv; data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 58 | Khách sạn Phố Cổ | Lưu trú | **khách sạn giá rẻ phố cổ hà nội** | Transaction | 649 | 11 | 1.69 | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hà Nội' |
| 59 | Khách sạn Hà Nội | Lưu trú | **khách sạn giá rẻ hà nội gần hồ hoàn kiếm** | Transaction | 615 | 10 | 1.63 | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hà Nội' |
| 60 | Khách sạn Phố Cổ | Lưu trú | **khách sạn gần phố cổ hà nội** | Commercial Investigation | 1993 | 31 | 1.56 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 61 | Khách sạn Hà Nội | Lưu trú | **khách sạn hà nội 4 sao** | Commercial Investigation | 1424 | 22 | 1.54 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 62 | Điểm tham quan Hà Nội | Địa danh tham quan / Văn hóa - Lịch sử | **19c hoàng diệu hoàng thành thăng long** | Informational | 879 | 12 | 1.37 | data/google_search_console/Queries.csv | Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3 |
| 63 | Khách sạn Phố Cổ | Lưu trú | **khách sạn khu phố cổ hà nội** | Commercial Investigation | 1151 | 15 | 1.3 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 64 | Tổng hợp Hà Nội | Tổng hợp | **tòa soạn báo hà nội mới ở đâu** | Informational | 768 | 10 | 1.3 | data/google_search_console/Queries.csv | Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3 |
| 65 | Khách sạn Hà Nội | Lưu trú | **khách sạn ở hà nội gần hồ gươm** | Commercial Investigation | 1630 | 19 | 1.17 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 66 | Điểm tham quan Hà Nội | Địa danh tham quan / Văn hóa - Lịch sử | **19c phố hoàng diệu hoàng thành thăng long** | Informational | 3566 | 39 | 1.09 | data/google_search_console/Queries.csv | Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3 |
| 67 | Khách sạn Hà Nội | Lưu trú | **nhà nghỉ gần lăng bác** | Commercial Investigation | 945 | 10 | 1.06 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 68 | Khách sạn Hà Nội | Lưu trú | **khách sạn gần hồ gươm hà nội** | Commercial Investigation | 1252 | 13 | 1.04 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 69 | Khách sạn Hà Nội | Lưu trú | **nhà nghỉ gần hồ hoàn kiếm giá rẻ** | Transaction | 1112 | 11 | 0.99 | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hà Nội' |
| 70 | Khách sạn Hà Nội | Lưu trú | **khách sạn 5 sao ở hà nội** | Commercial Investigation | 1681 | 15 | 0.89 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 71 | Khách sạn Phố Cổ | Lưu trú | **khách sạn phố cổ hà nội** | Commercial Investigation | 7707 | 66 | 0.86 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 72 | Khách sạn Hà Nội | Lưu trú | **khách sạn 5 sao hà nội** | Commercial Investigation | 13613 | 104 | 0.76 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 73 | Khách sạn/Homestay Hồ Tây | Lưu trú | **khách sạn hồ tây** | Commercial Investigation | 2283 | 17 | 0.74 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 74 | Khách sạn Hà Nội | Lưu trú | **khách sạn hà nội giá rẻ** | Transaction | 1471 | 10 | 0.68 | data/google_search_console/Queries.csv | Tối ưu landing (CTA/giá/FAQ), cải thiện snippet để tăng CTR; internal link từ hub 'Hà Nội' |
| 75 | Điểm tham quan Hà Nội | Địa danh tham quan / Văn hóa - Lịch sử | **hoàng thành thăng long ở đâu** | Informational | 6302 | 39 | 0.62 | data/google_search_console/Queries.csv | Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3 |
| 76 | Khách sạn Hà Nội | Lưu trú | **khách sạn gần hồ gươm** | Commercial Investigation | 3571 | 22 | 0.62 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 77 | Hồ Hoàn Kiếm & Phố đi bộ | Địa danh tham quan / Văn hóa - Lịch sử | **hồ hoàn kiếm** | Informational | 10468 | 62 | 0.59 | data/google_search_console/Queries.csv | Cập nhật nội dung theo intent, bổ sung FAQ + schema, tối ưu title/meta để đẩy Top 1-3 |
| 78 | Khách sạn Phố Cổ | Lưu trú | **khách sạn phố cổ** | Commercial Investigation | 3576 | 21 | 0.59 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 79 | Khách sạn Hà Nội | Lưu trú | **khách sạn gần hồ hoàn kiếm hà nội** | Commercial Investigation | 1867 | 11 | 0.59 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |
| 80 | Khách sạn Hà Nội | Lưu trú | **khách sạn gần hồ hoàn kiếm** | Commercial Investigation | 6911 | 33 | 0.48 | data/google_search_console/Queries.csv | Refresh bài top-list, thêm bảng so sánh + schema FAQ/Review; tối ưu title để tăng CTR |

## 4. NHÓM 2: TỪ KHÓA MỚI (KHAI PHÁ THỊ TRƯỜNG - GROUP B)
> **Tiêu chí sắp xếp**: Score tổng hợp (Volume cao + Cạnh tranh thấp/trung bình -> YoY tăng + Bid cao).

| STT | Cluster | Cluster Type | Keyword | Intent | Vol | YoY | KD/Comp | Bid (High) | Source | Action Plan |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Tổng hợp Hà Nội | Tổng hợp | **du lịch hà nội** | Informational | 0 | N/A | N/A | N/A | data/google_trend/searched_with_rising-queries_VN_20250210-1752_20260210-1752.csv; data/google_trend/searched_with_top-queries_VN_20250210-1752_20260210-1752.csv; data/google_trend/searched_with_top-queries_VN_20250210-1750_20260210-1750.csv | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 2 | Khách sạn Hà Nội | Lưu trú | **khách sạn hà nội** | Commercial Investigation | 0 | N/A | N/A | N/A | data/google_trend/searched_with_top-queries_VN_20250210-1748_20260210-1748.csv | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 3 | Khách sạn Hà Nội | Lưu trú | **khách sạn ở hà nội** | Commercial Investigation | 0 | N/A | N/A | N/A | data/google_trend/searched_with_top-queries_VN_20250210-1748_20260210-1748.csv | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 4 | Di chuyển Hà Nội | Di chuyển | **vé máy bay hà nội** | Transaction | 0 | N/A | N/A | N/A | data/google_trend/searched_with_top-queries_VN_20250210-1749_20260210-1749.csv | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 5 | Sài Gòn Trip | Di chuyển | **vé máy bay sài gòn hà nội** | Transaction | 0 | N/A | N/A | N/A | data/google_trend/searched_with_top-queries_VN_20250210-1749_20260210-1749.csv | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 6 | Sài Gòn Trip | Di chuyển | **vé máy bay hà nội sài gòn** | Transaction | 0 | N/A | N/A | N/A | data/google_trend/searched_with_top-queries_VN_20250210-1749_20260210-1749.csv | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 7 | Di chuyển Hà Nội | Di chuyển | **vé máy bay đi hà nội** | Transaction | 0 | N/A | N/A | N/A | data/google_trend/searched_with_top-queries_VN_20250210-1749_20260210-1749.csv | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 8 | Đà Nẵng Trip | Di chuyển | **vé máy bay hà nội đà nẵng** | Transaction | 0 | N/A | N/A | N/A | data/google_trend/searched_with_top-queries_VN_20250210-1749_20260210-1749.csv | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 9 | Đà Nẵng Trip | Di chuyển | **vé máy bay đà nẵng hà nội** | Transaction | 0 | N/A | N/A | N/A | data/google_trend/searched_with_top-queries_VN_20250210-1749_20260210-1749.csv | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 10 | Nha Trang Trip | Di chuyển | **vé máy bay nha trang hà nội** | Transaction | 0 | N/A | N/A | N/A | data/google_trend/searched_with_top-queries_VN_20250210-1749_20260210-1749.csv | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 11 | Tổng hợp Hà Nội | Tổng hợp | **cao đẳng du lịch hà nội** | Informational | 0 | N/A | N/A | N/A | data/google_trend/searched_with_rising-queries_VN_20250210-1752_20260210-1752.csv | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 12 | Tổng hợp Hà Nội | Tổng hợp | **trường cao đẳng du lịch hà nội** | Informational | 0 | N/A | N/A | N/A | data/google_trend/searched_with_rising-queries_VN_20250210-1752_20260210-1752.csv | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 13 | Tổng hợp Hà Nội | Tổng hợp | **cao đẳng thương mại và du lịch hà nội** | Informational | 0 | N/A | N/A | N/A | data/google_trend/searched_with_rising-queries_VN_20250210-1752_20260210-1752.csv | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 14 | Tổng hợp Hà Nội | Tổng hợp | **sở du lịch hà nội** | Informational | 0 | N/A | N/A | N/A | data/google_trend/searched_with_rising-queries_VN_20250210-1752_20260210-1752.csv | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 15 | Tổng hợp Hà Nội | Tổng hợp | **du lịch hà nội 1 ngày** | Informational | 0 | N/A | N/A | N/A | Web Suggest | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 16 | Tổng hợp Hà Nội | Tổng hợp | **du lịch hà nội 2 ngày 1 đêm** | Informational | 0 | N/A | N/A | N/A | Web Suggest | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 17 | Tổng hợp Hà Nội | Tổng hợp | **ăn gì ở hà nội** | Informational | 0 | N/A | N/A | N/A | Web Suggest | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 18 | Cafe Hà Nội | Ẩm thực (F&B) | **quán cafe view đẹp hồ tây** | Informational | 0 | N/A | N/A | N/A | Web Suggest | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 19 | Tổng hợp Hà Nội | Tổng hợp | **lịch trình du lịch hà nội** | Informational | 0 | N/A | N/A | N/A | Web Suggest | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 20 | Xe buýt & Tàu điện Hà Nội | Di chuyển | **xe buýt 2 tầng hà nội** | Commercial Investigation | 0 | N/A | N/A | N/A | Web Suggest | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 21 | Tổng hợp Hà Nội | Tổng hợp | **đặc sản hà nội làm quà** | Informational | 0 | N/A | N/A | N/A | Web Suggest | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 22 | Điểm tham quan Hà Nội | Địa danh tham quan / Văn hóa - Lịch sử | **kem tràng tiền** | Informational | 0 | N/A | N/A | N/A | Web Suggest | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 23 | Tổng hợp Hà Nội | Tổng hợp | **kinh nghiệm du lịch hà nội** | Commercial Investigation | 0 | N/A | N/A | N/A | Web Suggest | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 24 | Khách sạn Hà Nội | Lưu trú | **khách sạn 3 sao hà nội** | Commercial Investigation | 0 | N/A | N/A | N/A | Web Suggest | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 25 | Khách sạn Hà Nội | Lưu trú | **homestay giá rẻ hà nội** | Transaction | 0 | N/A | N/A | N/A | Web Suggest | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 26 | Khách sạn Hà Nội | Lưu trú | **khách sạn có bồn tắm hà nội** | Commercial Investigation | 0 | N/A | N/A | N/A | Web Suggest | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 27 | Di chuyển Hà Nội | Di chuyển | **thuê xe máy hà nội** | Transaction | 0 | N/A | N/A | N/A | Web Suggest | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 28 | Di chuyển Hà Nội | Di chuyển | **thuê xe tự lái hà nội** | Transaction | 0 | N/A | N/A | N/A | Web Suggest | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 29 | Sapa Trip | Di chuyển | **vé tàu hà nội sapa** | Transaction | 0 | N/A | N/A | N/A | Web Suggest | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 30 | Hạ Long Trip | Di chuyển | **xe limousine hà nội hạ long** | Transaction | 0 | N/A | N/A | N/A | Web Suggest | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 31 | Sapa Trip | Di chuyển | **xe limousine hà nội sapa** | Transaction | 0 | N/A | N/A | N/A | Web Suggest | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 32 | Ninh Bình Trip | Di chuyển | **xe limousine hà nội ninh bình** | Transaction | 0 | N/A | N/A | N/A | Web Suggest | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 33 | Lăng Bác & Ba Đình | Địa danh tham quan / Văn hóa - Lịch sử | **lăng bác mở cửa ngày nào** | Informational | 0 | N/A | N/A | N/A | Web Suggest | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 34 | Điểm tham quan Hà Nội | Địa danh tham quan / Văn hóa - Lịch sử | **giá vé hoàng thành thăng long** | Transaction | 0 | N/A | N/A | N/A | Web Suggest | Tạo landing chuyển đổi (giá/vé/đặt chỗ), gom vào cluster page + build backlink nội bộ |
| 35 | Văn Miếu Quốc Tử Giám | Địa danh tham quan / Văn hóa - Lịch sử | **văn miếu quốc tử giám thờ ai** | Informational | 0 | N/A | N/A | N/A | Web Suggest | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 36 | Hồ Tây & Phủ Tây Hồ | Địa danh tham quan / Văn hóa - Lịch sử | **chùa trấn quốc hồ tây** | Informational | 0 | N/A | N/A | N/A | Web Suggest | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 37 | Tổng hợp Hà Nội | Tổng hợp | **bún đậu mắm tôm hà nội** | Informational | 0 | N/A | N/A | N/A | Web Suggest | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 38 | Cafe Hà Nội | Ẩm thực (F&B) | **cà phê trứng hà nội** | Informational | 0 | N/A | N/A | N/A | Web Suggest | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 39 | Ăn uống Hà Nội | Ẩm thực (F&B) | **bánh tôm hồ tây** | Informational | 0 | N/A | N/A | N/A | Web Suggest | Viết guide/review; ưu tiên long-tail; tạo topic hub và internal link về trang dịch vụ |
| 40 | Xe buýt & Tàu điện Hà Nội | Di chuyển | **xe bus 86 hà nội** | Commercial Investigation | 0 | N/A | N/A | N/A | Web Suggest | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |
| 41 | Di chuyển Hà Nội | Di chuyển | **tàu điện cát linh hà đông** | Commercial Investigation | 0 | N/A | N/A | N/A | Web Suggest | Viết bài top-list/so sánh; map vào cluster hub; bổ sung schema + ảnh/UGC |

## 5. QUALITY GATE (AUTO-CHECK)
- **Intent distribution**: Informational=37, Commercial Investigation=53, Transaction=31
- [x] PASS: Taxonomy (landmark không được nằm trong F&B)
- [x] PASS: Geo-scope (out-of-scope phải tách cluster '* Trip')
- [x] PASS: Source (mỗi keyword phải có source folder/file)
- [x] PASS: Intent ratio (100 keywords phải đạt 20/40/40)
