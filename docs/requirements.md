# YÊU CẦU DỰ ÁN VÀ PHÂN QUYỀN NGƯỜI DÙNG (REQUIREMENTS & USER ROLES)

---

## 1. PHÂN QUYỀN VÀ VAI TRÒ NGƯỜI DÙNG (USER ROLES & PERMISSIONS)

Hệ thống được thiết kế dựa trên hệ thống xác thực và phân quyền chuẩn của Django (`django.contrib.auth`), chia thành 2 vai trò chính:

### 1.1. KHÁCH HÀNG (CUSTOMER)
- **Mô tả:** Người dùng đã đăng ký tài khoản và đăng nhập vào hệ thống để mua sắm.
- **Quyền hạn chi tiết:**
  - Được xem công khai trang chủ, danh sách sản phẩm, chi tiết sản phẩm, chính sách, giới thiệu, liên hệ.
  - Được đăng ký tài khoản mới và đăng nhập/đăng xuất an toàn.
  - Được quản lý thông tin hồ sơ cá nhân (Họ tên, số điện thoại, địa chỉ nhận hàng).
  - Được thêm sản phẩm theo biến thể (kích cỡ, màu sắc) vào giỏ hàng cá nhân.
  - Được cập nhật số lượng hoặc xóa sản phẩm khỏi giỏ hàng.
  - Được tiến hành đặt hàng với phương thức COD (Cash on Delivery).
  - Được xem lại danh sách đơn hàng đã mua (Lịch sử đơn hàng) và chi tiết từng đơn hàng của chính mình.
  - Được gửi đánh giá và nhận xét kèm số sao (1-5 sao) cho các sản phẩm.
- **Giới hạn an ninh (Security Constraints):**
  - **Không** được phép truy cập vào các đường dẫn quản trị (Admin Dashboard, Django Admin).
  - **Không** được xem, sửa hoặc hủy đơn hàng của khách hàng khác (buộc phải kiểm tra điều kiện `order.user == request.user` ở cấp View).
  - **Không** được phép can thiệp vào giá tiền hay số lượng tồn kho của sản phẩm.

### 1.2. QUẢN TRỊ VIÊN (ADMIN / STAFF)
- **Mô tả:** Ban quản lý cửa hàng, nhân sự phụ trách kho và xử lý đơn hàng (`is_staff=True` hoặc `is_superuser=True`).
- **Quyền hạn chi tiết:**
  - Truy cập bảng điều khiển quản trị (Admin Dashboard) tổng quan số liệu kinh doanh: tổng số đơn hàng, tổng doanh thu, số sản phẩm sắp hết hàng, khách hàng mới.
  - Quản lý danh mục sản phẩm (Thêm mới, sửa thông tin, xóa danh mục không có ràng buộc).
  - Quản lý sản phẩm và biến thể sản phẩm (Thêm sản phẩm, tải ảnh lên, thiết lập giá bán, giá khuyến mãi, tạo các biến thể Size / Color / SKU / Tồn kho).
  - Quản lý kho hàng (Inventory Management): Theo dõi lượng tồn theo từng biến thể, cập nhật nhập kho khi cần.
  - Quản lý đơn hàng (Order Management): Xem danh sách tất cả các đơn hàng, lọc theo trạng thái (`Pending`, `Confirmed`, `Shipping`, `Delivered`, `Cancelled`), cập nhật trạng thái đơn hàng.
  - Quản lý khách hàng: Xem danh sách tài khoản khách hàng, khóa/mở khóa tài khoản khi cần.
  - Thao tác toàn diện qua giao diện quản trị tùy chỉnh (Custom Admin Panel) và hệ thống Django Admin gốc (`/admin/`).
  - Toàn quyền gọi API quản trị qua Django REST Framework (`POST`, `PUT`, `PATCH`, `DELETE`).

---

## 2. YÊU CẦU CHỨC NĂNG (FUNCTIONAL REQUIREMENTS)

### 2.1. Phân hệ Xác thực & Tài khoản (Accounts Module)
- **FR-ACC-01 (Đăng ký):** Người dùng có thể đăng ký tài khoản bằng `username`, `email`, `password`, `confirm_password`, họ và tên. Hệ thống kiểm tra trùng lặp và độ mạnh mật khẩu.
- **FR-ACC-02 (Đăng nhập):** Xác thực người dùng bằng username và password. Báo lỗi rõ ràng nếu nhập sai thông tin.
- **FR-ACC-03 (Đăng xuất):** Hủy phiên làm việc (Session) an toàn và chuyển hướng về trang chủ kèm thông báo thành công.
- **FR-ACC-04 (Hồ sơ người dùng):** Cho phép xem và cập nhật thông tin cá nhân: Số điện thoại, địa chỉ giao hàng mặc định.

### 2.2. Phân hệ Sản phẩm & Danh mục (Products Module)
- **FR-PROD-01 (Hiển thị sản phẩm):** Danh sách sản phẩm được phân trang, hiển thị hình ảnh đại diện, tên, danh mục, giá gốc và giá khuyến mãi (nếu có).
- **FR-PROD-02 (Phân loại theo danh mục):** Cho phép người dùng lọc sản phẩm theo danh mục cụ thể (Áo thun, Sơ mi, Váy đầm, Quần jeans,...).
- **FR-PROD-03 (Tìm kiếm & Bộ lọc):** Tìm kiếm sản phẩm theo tên hoặc từ khóa mô tả; sắp xếp sản phẩm theo giá tăng/giảm hoặc mới nhất.
- **FR-PROD-04 (Chi tiết sản phẩm):** Hiển thị đầy đủ mô tả, hình ảnh lớn, danh sách kích cỡ (Size), màu sắc (Color) khả dụng và trạng thái còn hàng/hết hàng.
- **FR-PROD-05 (Quản lý CRUD):** Admin có thể tạo, chỉnh sửa, ẩn/hiện hoặc xóa sản phẩm và các biến thể.

### 2.3. Phân hệ Giỏ hàng (Shopping Cart Module)
- **FR-CART-01 (Thêm vào giỏ):** Khách hàng chọn một biến thể cụ thể (Size + Màu) và số lượng để thêm vào giỏ.
- **FR-CART-02 (Kiểm tra tồn kho khi thêm):** Không cho phép thêm số lượng vượt quá số lượng tồn kho thực tế của biến thể đó.
- **FR-CART-03 (Xem giỏ hàng):** Hiển thị danh sách các món đồ đã chọn kèm hình ảnh, tên, biến thể, đơn giá, số lượng và tổng tiền tạm tính.
- **FR-CART-04 (Cập nhật & Xóa):** Cho phép thay đổi số lượng từng món trong giỏ hàng hoặc xóa món đồ khỏi giỏ hàng ngay lập tức.
- **FR-CART-05 (Đồng bộ người dùng):** Giỏ hàng được lưu trong cơ sở dữ liệu liên kết với tài khoản người dùng đã đăng nhập.

### 2.4. Phân hệ Đặt hàng & Thanh toán (Orders Module)
- **FR-ORD-01 (Khởi tạo thanh toán):** Kiểm tra giỏ hàng có sản phẩm hợp lệ trước khi cho phép vào trang thanh toán.
- **FR-ORD-02 (Nhập thông tin giao nhận):** Khách hàng điền họ tên người nhận, số điện thoại, địa chỉ chi tiết và ghi chú đơn hàng. Form tự động điền thông tin từ hồ sơ khách hàng nếu có.
- **FR-ORD-03 (Xác nhận đặt hàng):** Thực hiện giao dịch an toàn (Database Transaction):
  - Kiểm tra lại tồn kho tức thời.
  - Tạo bản ghi `Order` với mã đơn hàng duy nhất (`order_number`).
  - Sao lưu đơn giá tại thời điểm mua vào bản ghi `OrderItem`.
  - Trừ số lượng tồn kho tương ứng của `ProductVariant`.
  - Làm trống giỏ hàng sau khi đặt thành công.
- **FR-ORD-04 (Trang cảm ơn / Xác nhận):** Hiển thị thông báo đặt hàng thành công kèm tóm tắt đơn hàng và hướng dẫn nhận hàng COD.
- **FR-ORD-05 (Lịch sử đơn hàng):** Khách hàng xem lại danh sách đơn hàng đã mua, ngày mua, tổng tiền và trạng thái hiện tại.
- **FR-ORD-06 (Chi tiết đơn hàng):** Khách hàng xem chi tiết từng món đồ trong đơn hàng đã đặt.

### 2.5. Phân hệ Quản trị (Admin Management Module)
- **FR-ADM-01 (Thống kê tổng hợp):** Thống kê tổng doanh thu từ các đơn hàng thành công, số lượng đơn hàng mới, số sản phẩm đang kinh doanh.
- **FR-ADM-02 (Xử lý đơn hàng):** Chuyển đổi trạng thái đơn hàng (`Pending` -> `Confirmed` -> `Shipping` -> `Delivered` / `Cancelled`). Nếu chuyển sang `Cancelled`, tự động hoàn trả số lượng vào kho.
- **FR-ADM-03 (Quản trị sản phẩm & kho):** Thêm nhanh sản phẩm, upload ảnh, tạo biến thể kích cỡ / màu sắc / số lượng tồn kho.

### 2.6. Phân hệ Đánh giá & Nhận xét (Reviews Module)
- **FR-REV-01 (Gửi đánh giá):** Khách hàng có thể viết nhận xét và chọn số sao từ 1 đến 5 sao cho sản phẩm.
- **FR-REV-02 (Hiển thị đánh giá):** Danh sách đánh giá hiển thị công khai ở trang chi tiết sản phẩm kèm thời gian gửi và tên khách hàng.

### 2.7. Phân hệ REST API (DRF Product API)
- **FR-API-01:** `GET /api/products/` - Danh sách sản phẩm dạng JSON.
- **FR-API-02:** `GET /api/products/<int:pk>/` - Chi tiết sản phẩm dạng JSON.
- **FR-API-03:** `POST /api/products/` - Thêm mới sản phẩm (Chỉ dành cho Admin, yêu cầu xác thực).
- **FR-API-04:** `PUT / PATCH /api/products/<int:pk>/` - Cập nhật sản phẩm (Chỉ dành cho Admin).
- **FR-API-05:** `DELETE /api/products/<int:pk>/` - Xóa sản phẩm (Chỉ dành cho Admin).

---

## 3. YÊU CẦU PHI CHỨC NĂNG (NON-FUNCTIONAL REQUIREMENTS)

### 3.1. An toàn & Bảo mật (Security)
- **Mật khẩu an toàn:** Sử dụng thuật toán PBKDF2 của Django để băm (hash) mật khẩu. Tuyệt đối không lưu mật khẩu dạng bản rõ (plaintext).
- **Chống tấn công CSRF:** Bắt buộc sử dụng thẻ `{% csrf_token %}` trên tất cả các form gửi dữ liệu bằng phương thức `POST`.
- **Chống SQL Injection:** Sử dụng 100% Django ORM với parameterized queries, không nối chuỗi SQL thô.
- **Chống truy cập trái phép (Access Control):** Bảo vệ các trang nhạy cảm bằng `@login_required` và kiểm tra quyền admin (`request.user.is_staff`). Kiểm tra nghiêm ngặt quyền sở hữu dữ liệu đơn hàng trên Server.

### 3.2. Hiệu năng & Tính ổn định (Performance & Reliability)
- Tối ưu hóa truy vấn bằng `select_related` và `prefetch_related` khi hiển thị danh sách sản phẩm và đơn hàng để tránh lỗi truy vấn lặp `N+1`.
- Sử dụng giao dịch cơ sở dữ liệu (`transaction.atomic()`) trong quá trình tạo đơn hàng để bảo toàn tính toàn vẹn dữ liệu kho và đơn hàng khi có lỗi xảy ra.

### 3.3. Tính khả dụng & Thẩm mỹ (Usability & Aesthetics)
- Thiết kế giao diện hiện đại, tối giản theo xu hướng thời trang quốc tế (Minimalist fashion design, tông màu trung tính đen/trắng/ghi/beige).
- Giao diện tương thích đa thiết bị (Responsive Design) với Bootstrap 5, hiển thị tốt trên Desktop, Tablet và Điện thoại di động.
- Thông báo trực quan (Django Messages framework) khi thực hiện các hành động: Thêm vào giỏ thành công, Đặt hàng thành công, Báo lỗi tồn kho,...

---

## 4. QUY TẮC NGHIỆP VỤ CỐT LÕI (CORE BUSINESS RULES)
1. **Bảo toàn giá (Price Preservation):** Giá sản phẩm có thể thay đổi trong tương lai, nhưng đơn hàng đã đặt phải luôn giữ nguyên mức giá tại thời điểm khách hàng bấm nút đặt hàng. Do đó, bảng `OrderItem` bắt buộc phải có trường `unit_price`.
2. **Tính toán tổng tiền ở Server (Server-side Calculation):** Toàn bộ tổng tiền giỏ hàng, tổng tiền đơn hàng phải được tính toán lại hoàn toàn ở phía Backend (Python), tuyệt đối không nhận tổng tiền gửi lên từ phía Client/JavaScript để chống gian lận giá.
3. **Kiểm tra tồn kho thời gian thực:** Trước khi tạo đơn hàng, hệ thống phải kiểm tra xem số lượng tồn kho của từng biến thể có đủ đáp ứng hay không. Nếu không đủ, giao dịch lập tức bị hủy bỏ và thông báo cho người dùng.
4. **Phương thức thanh toán ban đầu:** Áp dụng phương thức Thanh toán khi nhận hàng (COD - Cash On Delivery), đảm bảo tính thực tiễn cao và phù hợp với đồ án học tập.
