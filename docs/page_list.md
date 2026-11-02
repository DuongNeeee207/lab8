# DANH SÁCH CÁC TRANG VÀ TÍNH NĂNG CHI TIẾT (PAGE & FUNCTIONALITY LIST)

---

## 1. PHÂN HỆ KHÁCH HÀNG (CUSTOMER PAGES)

| STT | Tên trang | Đường dẫn URL | Tên URL (`name`) | View phụ trách | Template sử dụng | Quyền truy cập | Mô tả tính năng chính |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Trang chủ** | `/` | `core:home` | `home_view` | `core/home.html` | Công khai | Banner thời trang nổi bật, bộ sưu tập mới (New Arrivals), sản phẩm bán chạy (Best Sellers), danh mục nổi bật (Categories Grid), chính sách vận chuyển & đổi trả. |
| 2 | **Danh sách sản phẩm** | `/products/` | `products:product_list` | `product_list` | `products/product_list.html` | Công khai | Hiển thị tất cả sản phẩm thời trang có phân trang (Pagination), bộ lọc theo danh mục, lọc theo mức giá, sắp xếp (Mới nhất, Giá tăng/giảm). |
| 3 | **Sản phẩm theo danh mục** | `/products/category/<slug:category_slug>/` | `products:category_products` | `category_products` | `products/product_list.html` | Công khai | Lọc danh sách sản phẩm theo danh mục tương ứng (ví dụ: Áo sơ mi, Váy đầm), hiển thị tiêu đề và banner của danh mục. |
| 4 | **Tìm kiếm sản phẩm** | `/products/search/` | `products:search` | `product_search` | `products/product_list.html` | Công khai | Tìm kiếm theo từ khóa tên hoặc mô tả sản phẩm (nhận từ `request.GET['q']`), thông báo số lượng kết quả tìm thấy. |
| 5 | **Chi tiết sản phẩm** | `/products/<slug:product_slug>/` | `products:product_detail` | `product_detail` | `products/product_detail.html` | Công khai | Ảnh lớn sản phẩm, mô tả chi tiết, giá bán, chọn Size, chọn Màu, chọn số lượng, nút "Thêm vào giỏ hàng", danh sách đánh giá của khách hàng, form gửi đánh giá (nếu đã đăng nhập). |
| 6 | **Giỏ hàng** | `/cart/` | `cart:detail` | `cart_detail` | `cart/cart_detail.html` | Yêu cầu đăng nhập | Xem danh sách món hàng trong giỏ, hình ảnh, phân loại Size/Màu, thay đổi số lượng, xóa từng món, tính tạm tính và nút chuyển sang Thanh toán. |
| 7 | **Thêm vào giỏ hàng** | `/cart/add/<int:variant_id>/` | `cart:add` | `cart_add` | *(Xử lý POST & Redirect)* | Yêu cầu đăng nhập | Nhận biến thể `variant_id` và số lượng từ form chi tiết, kiểm tra số lượng tồn kho và cộng dồn vào giỏ hàng. |
| 8 | **Cập nhật giỏ hàng** | `/cart/update/<int:item_id>/` | `cart:update` | `cart_update` | *(Xử lý POST & Redirect)* | Yêu cầu đăng nhập | Cập nhật lại số lượng của món hàng trong giỏ, tự động xóa nếu số lượng về 0. |
| 9 | **Xóa món khỏi giỏ** | `/cart/remove/<int:item_id>/` | `cart:remove` | `cart_remove` | *(Xử lý POST & Redirect)* | Yêu cầu đăng nhập | Xóa hẳn một dòng món hàng ra khỏi giỏ của người dùng. |
| 10 | **Thanh toán (Checkout)** | `/orders/checkout/` | `orders:checkout` | `checkout_view` | `orders/checkout.html` | Yêu cầu đăng nhập | Hiển thị tóm tắt đơn hàng (tổng tiền, các món mua), form điền thông tin người nhận hàng (Họ tên, SĐT, Địa chỉ, Ghi chú), chọn phương thức COD, nút "Xác nhận đặt hàng". |
| 11 | **Xác nhận đặt hàng** | `/orders/success/<str:order_number>/` | `orders:success` | `order_success` | `orders/order_success.html` | Yêu cầu đăng nhập | Thông báo đặt hàng thành công, hiển thị mã đơn hàng, tổng tiền cần thanh toán khi nhận hàng, hướng dẫn liên hệ hỗ trợ. |
| 12 | **Đăng ký tài khoản** | `/accounts/register/` | `accounts:register` | `register_view` | `accounts/register.html` | Khách vãng lai | Form đăng ký: Tên tài khoản, Email, Mật khẩu, Xác nhận mật khẩu, Họ và tên. Kiểm tra trùng lặp và đăng nhập tự động sau khi đăng ký. |
| 13 | **Đăng nhập** | `/accounts/login/` | `accounts:login` | `login_view` | `accounts/login.html` | Khách vãng lai | Form đăng nhập: Username, Password. Chuyển hướng về trang trước đó hoặc trang chủ sau khi đăng nhập thành công. |
| 14 | **Đăng xuất** | `/accounts/logout/` | `accounts:logout` | `logout_view` | *(Xử lý POST & Redirect)* | Yêu cầu đăng nhập | Hủy phiên làm việc và trở về trang chủ kèm thông báo tạm biệt. |
| 15 | **Hồ sơ cá nhân** | `/accounts/profile/` | `accounts:profile` | `profile_view` | `accounts/profile.html` | Yêu cầu đăng nhập | Xem và cập nhật họ tên, số điện thoại, địa chỉ nhận hàng mặc định, đổi mật khẩu. |
| 16 | **Lịch sử đơn hàng** | `/orders/history/` | `orders:history` | `order_history` | `orders/order_history.html` | Yêu cầu đăng nhập | Hiển thị danh sách các đơn hàng của riêng tài khoản đang đăng nhập, trạng thái đơn hàng (Chờ xử lý, Đang giao, Đã giao, Đã hủy) và ngày đặt. |
| 17 | **Chi tiết đơn hàng** | `/orders/detail/<str:order_number>/` | `orders:detail` | `order_detail` | `orders/order_detail.html` | Yêu cầu đăng nhập (Chính chủ) | Xem đầy đủ chi tiết một đơn hàng: Tên từng món, Size, Màu, đơn giá tại thời điểm mua, địa chỉ nhận hàng, hành trình trạng thái. |
| 18 | **Giới thiệu (About Us)**| `/about/` | `core:about` | `about_view` | `core/about.html` | Công khai | Câu chuyện thương hiệu FashionStore, sứ mệnh thời trang bền vững, phong cách thiết kế tối giản. |
| 19 | **Liên hệ (Contact)** | `/contact/` | `core:contact` | `contact_view` | `core/contact.html` | Công khai | Bản đồ cửa hàng, thông tin liên hệ (hotline, email), form gửi tin nhắn thắc mắc. |

---

## 2. PHÂN HỆ QUẢN TRỊ (ADMIN PAGES)

| STT | Tên trang | Đường dẫn URL | Tên URL (`name`) | View phụ trách | Template sử dụng | Quyền truy cập | Mô tả tính năng chính |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Bảng điều khiển (Dashboard)** | `/management/` | `core:admin_dashboard` | `admin_dashboard` | `core/admin_dashboard.html` | Staff/Superuser | Thống kê tổng quan doanh thu, số đơn hàng đang chờ xử lý, số lượng sản phẩm đang hoạt động, danh sách 5 đơn hàng mới nhất cần xác nhận. |
| 2 | **Quản lý danh mục** | `/management/categories/` | `products:admin_category_list` | `admin_category_list` | `products/admin_category_list.html` | Staff/Superuser | Xem bảng danh mục, thêm mới danh mục, sửa thông tin hoặc xóa danh mục. |
| 3 | **Danh sách sản phẩm** | `/management/products/` | `products:admin_product_list` | `admin_product_list` | `products/admin_product_list.html` | Staff/Superuser | Bảng quản lý tất cả sản phẩm thời trang, hiển thị ảnh nhỏ, giá, danh mục, trạng thái bật/tắt, nút sửa, nút xóa. |
| 4 | **Thêm sản phẩm mới** | `/management/products/add/` | `products:admin_product_add` | `admin_product_add` | `products/admin_product_form.html` | Staff/Superuser | Form nhập thông tin sản phẩm: Tên, danh mục, mô tả, giá gốc, giá khuyến mãi, tải ảnh đại diện lên, kích hoạt hiển thị. |
| 5 | **Chỉnh sửa sản phẩm** | `/management/products/<int:pk>/edit/` | `products:admin_product_edit` | `admin_product_edit` | `products/admin_product_form.html` | Staff/Superuser | Cập nhật thông tin chi tiết của sản phẩm đã có. |
| 6 | **Quản lý biến thể & kho** | `/management/products/<int:pk>/variants/` | `products:admin_variants` | `admin_variants` | `products/admin_variants.html` | Staff/Superuser | Thêm các kích cỡ (S, M, L, XL) và màu sắc cho sản phẩm, quản lý số lượng tồn kho từng biến thể, cập nhật mã SKU. |
| 7 | **Quản lý đơn hàng** | `/management/orders/` | `orders:admin_order_list` | `admin_order_list` | `orders/admin_orders.html` | Staff/Superuser | Bảng danh sách tất cả các đơn hàng trong toàn bộ hệ thống, lọc đơn theo trạng thái (`Pending`, `Confirmed`, `Shipping`, `Delivered`, `Cancelled`). |
| 8 | **Chi tiết & Xử lý đơn** | `/management/orders/<str:order_number>/` | `orders:admin_order_detail` | `admin_order_detail` | `orders/admin_order_detail.html` | Staff/Superuser | Xem đầy đủ thông tin khách hàng, địa chỉ, các mặt hàng đã mua; form cập nhật trạng thái đơn hàng (ví dụ: chuyển từ Chờ xử lý sang Đã xác nhận/Đang giao). |
| 9 | **Quản lý khách hàng** | `/management/customers/` | `accounts:admin_customer_list` | `admin_customer_list` | `accounts/admin_customers.html` | Staff/Superuser | Danh sách khách hàng đã đăng ký tài khoản, ngày tham gia, số lượng đơn hàng đã đặt. |
| 10 | **Hệ thống Django Admin** | `/admin/` | `admin:index` | Django Built-in | Django Built-in Admin Templates | Staff/Superuser | Quản lý toàn diện dữ liệu hệ thống (User, Group, Permissions, Categories, Products, Variants, Orders, Reviews) thông qua giao diện Django Admin gốc. |

---

## 3. PHÂN HỆ REST API (DRF ENDPOINTS)

| STT | Phương thức | Endpoint URL | Tên URL (`name`) | View phụ trách | Quyền truy cập | Chức năng |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `GET` | `/api/products/` | `api:product_list` | `ProductListCreateAPIView` | Cho phép đọc công khai | Lấy danh sách toàn bộ sản phẩm dạng JSON |
| 2 | `POST` | `/api/products/` | `api:product_create` | `ProductListCreateAPIView` | Chỉ Admin (`IsAdminUser`) | Thêm mới sản phẩm qua API |
| 3 | `GET` | `/api/products/<int:pk>/` | `api:product_detail` | `ProductDetailAPIView` | Cho phép đọc công khai | Lấy chi tiết thông tin và các biến thể của một sản phẩm |
| 4 | `PUT / PATCH`| `/api/products/<int:pk>/` | `api:product_update` | `ProductDetailAPIView` | Chỉ Admin (`IsAdminUser`) | Cập nhật thông tin sản phẩm qua API |
| 5 | `DELETE` | `/api/products/<int:pk>/` | `api:product_delete` | `ProductDetailAPIView` | Chỉ Admin (`IsAdminUser`) | Xóa sản phẩm qua API |
