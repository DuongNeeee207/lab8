# BÁO CÁO KIỂM THỬ HỆ THỐNG (TESTING & DEBUGGING REPORT)
**Dự án: FashionStore — E-Commerce Website using Django**

---

## 1. MỤC TIÊU VÀ PHẠM VI KIỂM THỬ
Kiểm thử toàn diện chức năng của hệ thống FashionStore nhằm đảm bảo:
- Xác thực và phân quyền (Authentication & Authorization) chính xác giữa Khách hàng và Admin.
- Tìm kiếm, lọc sản phẩm theo danh mục và khoảng giá hoạt động chính xác.
- Thao tác giỏ hàng (thêm món, chọn size/màu, thay đổi số lượng, xóa) trơn tru.
- Quy trình Đặt hàng (Checkout) bảo toàn đơn giá và tự động trừ/hoàn trả tồn kho chính xác trong cơ sở dữ liệu.
- Phân hệ quản trị (Admin Panel) và REST API (DRF) hoạt động ổn định, bảo mật.

---

## 2. BẢNG KẾT QUẢ KIỂM THỬ CHỨC NĂNG (FUNCTIONAL TEST CASES)

| Mã kiểm thử | Phân hệ | Trường hợp kiểm thử (Test Case) | Dữ liệu đầu vào / Thao tác | Kết quả kỳ vọng (Expected Result) | Kết quả thực tế (Actual Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-AUTH-01** | Xác thực | Đăng ký tài khoản khách hàng mới | `username='an_nguyen'`, `email='an@gmail.com'`, mật khẩu hợp lệ | Tạo User và Profile thành công, tự động đăng nhập và chuyển hướng về trang chủ kèm thông báo chào mừng | Tạo tài khoản thành công, đăng nhập ngay, hiển thị thông báo | **PASS** |
| **TC-AUTH-02** | Xác thực | Đăng ký với username đã tồn tại | `username='admin'` | Báo lỗi trùng lặp `Tên đăng nhập này đã có người sử dụng` và yêu cầu chọn tên khác | Hiển thị thông báo lỗi trường form chính xác | **PASS** |
| **TC-AUTH-03** | Xác thực | Đăng nhập với mật khẩu sai | `username='khachhang'`, `password='sai123'` | Báo lỗi `Tên đăng nhập hoặc mật khẩu không chính xác`, không cho đăng nhập | Báo lỗi và giữ nguyên form | **PASS** |
| **TC-AUTH-04** | Phân quyền | Khách hàng cố truy cập URL Admin | Truy cập `/management/dashboard/` bằng tài khoản thường | Chuyển hướng hoặc chặn truy cập (HTTP 302/403) | Hệ thống chuyển hướng về trang đăng nhập hoặc chặn theo `user_passes_test` | **PASS** |
| **TC-PROD-01** | Sản phẩm | Hiển thị danh sách sản phẩm | Truy cập `/products/` | Hiển thị danh sách sản phẩm phân trang, ảnh đại diện, giá gốc, giá sale | Tải đủ sản phẩm, ảnh và phân loại size | **PASS** |
| **TC-PROD-02** | Sản phẩm | Lọc sản phẩm theo danh mục | Chọn danh mục `Áo Sơ Mi (ao-so-mi)` | Chỉ hiển thị các sản phẩm thuộc danh mục áo sơ mi | Lọc đúng 100% sản phẩm tương ứng | **PASS** |
| **TC-PROD-03** | Sản phẩm | Tìm kiếm sản phẩm | Nhập từ khóa `Blazer` | Hiển thị sản phẩm `Áo Khoác Blazer Nam Cổ Điển 2 Lớp` | Tìm kiếm chính xác theo tên và mô tả | **PASS** |
| **TC-PROD-04** | Sản phẩm | Xem chi tiết sản phẩm | Truy cập `/products/detail/<slug>/` | Hiển thị chi tiết mô tả, các biến thể Size (S, M, L) và Màu khả dụng, kiểm tra trạng thái tồn kho | Hiển thị đầy đủ thông tin, form chọn biến thể phản hồi linh hoạt | **PASS** |
| **TC-CART-01** | Giỏ hàng | Thêm biến thể sản phẩm vào giỏ | Chọn Size M, Màu Đen, số lượng 2 | Thêm thành công vào giỏ, cập nhật badge số lượng trên thanh menu điều hướng | Giỏ hàng tăng 2 món, badge navbar nhảy số tức thì | **PASS** |
| **TC-CART-02** | Giỏ hàng | Thêm số lượng vượt tồn kho | Chọn biến thể còn 10 cái, nhập số lượng mua 99 | Báo cảnh báo `Sản phẩm chỉ còn 10 cái trong kho`, không cho vượt tồn | Hiển thị thông báo cảnh báo và chặn thêm | **PASS** |
| **TC-CART-03** | Giỏ hàng | Thay đổi số lượng & xóa | Bấm nút (+) tăng, (-) giảm, (xóa) | Cập nhật số lượng và tổng tiền tạm tính tương ứng, xóa món khi số lượng = 0 | Tính toán chuẩn xác ở server | **PASS** |
| **TC-ORD-01** | Đặt hàng | Thanh toán khi giỏ trống | Truy cập `/orders/checkout/` khi giỏ trống | Chuyển hướng về trang sản phẩm kèm thông báo giỏ hàng trống | Chuyển hướng chuẩn | **PASS** |
| **TC-ORD-02** | Đặt hàng | Đặt hàng COD thành công | Điền họ tên, số điện thoại hợp lệ (10 số), địa chỉ nhận hàng, chọn COD | Tạo đơn hàng mới, tạo OrderItem, trừ số lượng tồn kho của biến thể, làm sạch giỏ hàng | Đơn hàng tạo thành công, mã đơn dạng `FS-XXXXXX`, tồn kho bị trừ đúng số lượng đặt | **PASS** |
| **TC-ORD-03** | Đặt hàng | Bảo toàn đơn giá lúc mua | Sản phẩm gốc giảm giá hoặc thay đổi giá trong tương lai | `OrderItem.unit_price` giữ nguyên mức giá tại thời điểm khách bấm đặt hàng | Đơn giá được lưu cố định vào bản ghi chi tiết đơn | **PASS** |
| **TC-ORD-04** | Đặt hàng | Khách xem lịch sử đơn hàng | Truy cập `/orders/history/` | Hiển thị danh sách các đơn hàng của riêng khách hàng đó | Hiển thị đúng các đơn hàng của chính tài khoản đang đăng nhập | **PASS** |
| **TC-ADM-01** | Quản trị | Admin Dashboard | Đăng nhập tài khoản Admin truy cập `/management/dashboard/` | Hiển thị thống kê tổng doanh thu, số đơn chờ duyệt, tổng sản phẩm, khách hàng | Hiển thị số liệu trực quan, thẻ KPI và đơn mới | **PASS** |
| **TC-ADM-02** | Quản trị | Admin hủy đơn & hoàn kho | Đổi trạng thái đơn từ `Pending` sang `Cancelled` | Trạng thái cập nhật `Đã hủy`, số lượng sản phẩm trong đơn được tự động cộng hoàn lại kho | Tồn kho được hoàn trả chính xác về ban đầu | **PASS** |
| **TC-API-01** | REST API | Lấy danh sách sản phẩm qua API | `GET /api/products/` | Trả về mã HTTP 200 và chuỗi JSON chứa danh sách sản phẩm cùng các biến thể | JSON trả về đầy đủ các trường, hỗ trợ phân trang | **PASS** |
| **TC-API-02** | REST API | Xem chi tiết sản phẩm qua API | `GET /api/products/1/` | Trả về mã HTTP 200 và chi tiết một sản phẩm | Trả về JSON chi tiết đúng sản phẩm yêu cầu | **PASS** |

---

## 3. KẾT LUẬN KIỂM THỬ
- **Tổng số trường hợp kiểm thử thực hiện:** 19 trường hợp (gồm 9 bài test tự động qua script `test_suite.py` và 10 bài test nghiệp vụ chi tiết).
- **Số ca đạt (PASS):** 19/19 (100%).
- **Số ca lỗi (FAIL):** 0/19 (0%).
- **Đánh giá tổng thể:** Hệ thống vận hành trơn tru, logic trừ tồn kho và hoàn kho khi hủy đơn hoạt động chính xác tuyệt đối; giao diện thân thiện, chuẩn responsive và tuân thủ chặt chẽ kiến trúc MTV của Django.
