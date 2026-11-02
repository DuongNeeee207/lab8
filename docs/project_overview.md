# TỔNG QUAN DỰ ÁN: FASHIONSTORE
**Website Thương Mại Điện Tử Thời Trang Bằng Python & Django**

---

## 1. THÔNG TIN CHUNG
- **Tên dự án:** FashionStore
- **Loại hình:** Ứng dụng web thương mại điện tử chuyên ngành thời trang (Clothing E-Commerce Web Application).
- **Mục tiêu dự án:**
  - Xây dựng một website bán hàng thời trang hoàn chỉnh, chuẩn mực theo kiến trúc MTV (Model - Template - View) của framework Django.
  - Cung cấp cho khách hàng trải nghiệm mua sắm mượt mà, trực quan, tinh tế lấy cảm hứng từ các thương hiệu thời trang hiện đại (Zara, H&M, Uniqlo).
  - Cung cấp cho ban quản trị (Admin) hệ thống quản lý sản phẩm, biến thể (size, màu), danh mục, đơn hàng và khách hàng dễ sử dụng, an toàn và bảo mật.
  - Phục vụ báo cáo và bảo vệ đồ án chuyên môn, đáp ứng đầy đủ nội dung kiến thức từ Cơ bản đến Nâng cao của chương trình học Django.

- **Đối tượng người dùng:**
  - **Khách hàng (Customer):** Người tiêu dùng có nhu cầu tìm kiếm, tham khảo, đặt mua các mặt hàng thời trang trực tuyến.
  - **Quản trị viên (Admin / Shop Manager):** Chủ shop hoặc nhân viên quản lý kho, sản phẩm, xử lý đơn hàng và theo dõi vận hành website.

---

## 2. NGHIỆP VỤ KINH DOANH CHÍNH (CORE BUSINESS OPERATIONS)
1. **Quản lý danh mục & dòng sản phẩm:**
   - Thời trang nam (Men's clothing), Thời trang nữ (Women's clothing).
   - Áo thun (T-shirts), Áo sơ mi (Shirts), Áo hoodie & áo nỉ (Hoodies & Sweatshirts), Áo khoác & áo măng tô (Jackets & Coats).
   - Quần jeans & quần tây (Jeans & Trousers), Váy & đầm (Dresses & Skirts), Phụ kiện thời trang (Fashion Accessories).
2. **Quản lý biến thể sản phẩm (Size & Color):**
   - Một mẫu áo/quần có thể có nhiều kích thước (S, M, L, XL, XXL) và màu sắc (Đen, Trắng, Be, Xanh Navy,...).
   - Từng biến thể có mã SKU và số lượng tồn kho riêng biệt.
3. **Quy trình mua hàng (Shopping Workflow):**
   - Khách xem danh mục -> Tìm kiếm/Lọc -> Xem chi tiết -> Chọn Size/Màu -> Thêm vào giỏ hàng (Cart).
   - Cập nhật số lượng, xóa sản phẩm trong giỏ hàng.
   - Tiến hành thanh toán (Checkout) -> Điền địa chỉ giao hàng, số điện thoại, ghi chú -> Chọn hình thức thanh toán COD (Thanh toán khi nhận hàng).
   - Tạo đơn hàng (Order) -> Hệ thống tự động trừ tồn kho của biến thể -> Chuyển sang trạng thái đơn hàng "Chờ xử lý" (Pending).
4. **Quy trình xử lý đơn hàng (Order Fulfillment):**
   - Admin tiếp nhận đơn hàng, xem chi tiết các mặt hàng -> Cập nhật trạng thái: `Chờ xử lý (Pending)` -> `Đã xác nhận (Confirmed)` -> `Đang giao hàng (Shipping)` -> `Đã giao thành công (Delivered)` hoặc `Đã hủy (Cancelled)`.
   - Nếu đơn hàng bị hủy, số lượng tồn kho sẽ được hoàn trả lại cho hệ thống.
5. **Đánh giá & Phản hồi (Reviews & Ratings):**
   - Khách hàng đã mua hoặc trải nghiệm có thể gửi đánh giá sao (1 đến 5 sao) và nhận xét cho từng sản phẩm.

---

## 3. CÔNG NGHỆ & CÔNG CỤ SỬ DỤNG
- **Ngôn ngữ lập trình:** Python (>= 3.10)
- **Web Framework chính:** Django (Phiên bản 5.x LTS / 4.2 LTS)
  - Kiến trúc: MTV (Model - Template - View)
  - ORM: Django Object-Relational Mapping (xử lý dữ liệu không cần viết SQL thô)
  - Authentication: Django Auth System (Quản lý User, Session, Password Hashing PBKDF2/Argon2)
  - Forms: Django Form & ModelForm (Xác thực dữ liệu chặt chẽ ở backend)
- **API (Phần mở rộng):** Django REST Framework (DRF) cho Product API.
- **Frontend & Giao diện:**
  - HTML5, CSS3, JavaScript nguyên bản (Vanilla JS)
  - Framework CSS: Bootstrap 5 (Responsive grid, components)
  - Icons: Bootstrap Icons
  - Django Template Engine: Kế thừa giao diện (`{% extends %}`, `{% block %}`, `{% include %}`)
- **Cơ sở dữ liệu:** SQLite3 (phù hợp tối đa cho môi trường học tập, đồ án, dễ triển khai sao lưu).
- **Môi trường & Công cụ phát triển:** Visual Studio Code / PyCharm, Python Virtual Environment (`venv`), Git.

---

## 4. CẤU TRÚC DỰ ÁN DJANGO DỰ KIẾN (PROPOSED PROJECT STRUCTURE)

Dự án được phân tách thành các Django App chuyên biệt, độc lập và dễ hiểu:

```text
fashionstore_project/
│
├── manage.py                     # Script điều khiển dòng lệnh của Django
├── db.sqlite3                    # Cơ sở dữ liệu SQLite
├── requirements.txt              # Danh sách thư viện phụ thuộc (Django, djangorestframework, pillow, ...)
│
├── fashionstore/                 # Thư mục cấu hình trung tâm (Project root configuration)
│   ├── __init__.py
│   ├── settings.py               # Cấu hình dự án (INSTALLED_APPS, DATABASE, STATIC, MEDIA, TEMPLATES)
│   ├── urls.py                   # Bộ định tuyến URL gốc của toàn bộ website
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/                     # App: Quản lý người dùng, đăng ký, đăng nhập, hồ sơ
│   ├── migrations/
│   ├── models.py                 # Profile (mở rộng thông tin số điện thoại, địa chỉ)
│   ├── forms.py                  # UserRegisterForm, UserLoginForm, ProfileUpdateForm
│   ├── views.py                  # login_view, register_view, logout_view, profile_view
│   ├── urls.py
│   └── admin.py
│
├── products/                     # App: Quản lý danh mục, sản phẩm, biến thể (size, màu)
│   ├── migrations/
│   ├── models.py                 # Category, Product, ProductVariant
│   ├── forms.py                  # ProductForm, ProductVariantForm, CategoryForm
│   ├── views.py                  # product_list, product_detail, category_products, search_products
│   ├── serializers.py            # DRF ModelSerializers
│   ├── api_views.py              # DRF API generic views
│   ├── api_urls.py               # DRF API routing
│   ├── urls.py
│   └── admin.py
│
├── cart/                         # App: Giỏ hàng & các thao tác thêm, bớt, xóa sản phẩm
│   ├── migrations/
│   ├── models.py                 # Cart, CartItem
│   ├── views.py                  # cart_detail, cart_add, cart_update, cart_remove
│   ├── urls.py
│   └── admin.py
│
├── orders/                       # App: Đặt hàng, thanh toán COD, quản lý đơn hàng
│   ├── migrations/
│   ├── models.py                 # Order, OrderItem
│   ├── forms.py                  # CheckoutForm
│   ├── views.py                  # checkout_view, order_confirmation, order_history, order_detail
│   ├── urls.py
│   └── admin.py
│
├── reviews/                      # App: Đánh giá và nhận xét sản phẩm
│   ├── migrations/
│   ├── models.py                 # Review
│   ├── forms.py                  # ReviewForm
│   ├── views.py                  # add_review
│   ├── urls.py
│   └── admin.py
│
├── core/                         # App: Trang chủ, giới thiệu, liên hệ, bảng điều khiển quản trị tùy chỉnh
│   ├── views.py                  # home_view, about_view, contact_view, admin_dashboard
│   ├── urls.py
│   └── forms.py                  # ContactForm
│
├── static/                       # Chứa static files chung
│   ├── css/
│   │   └── style.css             # CSS tùy chỉnh với phong cách thời trang tối giản, cao cấp
│   ├── js/
│   │   └── main.js               # JavaScript tương tác client-side
│   └── images/                   # Logo, banner, placeholder mặc định
│
├── media/                        # Chứa file upload động của người dùng (ảnh sản phẩm, danh mục)
│   ├── products/
│   ├── categories/
│   └── avatars/
│
├── templates/                    # Giao diện HTML (Django Templates)
│   ├── base.html                 # Layout dùng chung: Navbar, Header, Footer, Toast Messages
│   ├── core/
│   │   ├── home.html
│   │   ├── about.html
│   │   ├── contact.html
│   │   └── admin_dashboard.html  # Giao diện thống kê và quản trị riêng cho Admin
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   ├── products/
│   │   ├── product_list.html
│   │   ├── product_detail.html
│   │   ├── product_form.html     # Tạo/sửa sản phẩm
│   │   └── category_list.html
│   ├── cart/
│   │   └── cart_detail.html
│   ├── orders/
│   │   ├── checkout.html
│   │   ├── order_confirmation.html
│   │   ├── order_history.html
│   │   ├── order_detail.html
│   │   └── admin_orders.html     # Danh sách quản lý đơn hàng cho Admin
│   └── includes/
│       ├── navbar.html
│       ├── footer.html
│       └── messages.html
│
└── docs/                         # Thư mục tài liệu đồ án (Planning, ERD, Specs)
```

---

## 5. MỐI LIÊN HỆ VỚI CHƯƠNG TRÌNH HỌC DJANGO (CHAPTERS 1 - 8)

| Chương trong khóa học | Nội dung cốt lõi | Cách thức ứng dụng trong dự án FashionStore |
| :--- | :--- | :--- |
| **Chương 1: Khởi tạo dự án & Kiến trúc MTV** | Cài đặt Python, venv, Django, `startproject`, `startapp`, cấu hình `settings.py`. | Thiết lập dự án `fashionstore`, chia tách 6 ứng dụng chuyên biệt (`accounts`, `products`, `cart`, `orders`, `reviews`, `core`). |
| **Chương 2: URL Routing & Views** | `path()`, `include()`, Function-Based Views (FBV), `request.GET`, `request.POST`, `redirect()`, `render()`. | Viết toàn bộ luồng nghiệp vụ xem sản phẩm, thêm vào giỏ, lọc danh mục, thanh toán bằng FBV dễ hiểu, tuân thủ mô hình Post/Redirect/Get. |
| **Chương 3: Templates & Static Files** | Kế thừa Template `{% extends %}`, `{% block %}`, `{% include %}`, bộ lọc, quản lý CSS/JS. | Tạo `base.html`, phân tách component navbar/footer/messages, thiết kế giao diện thời trang chuẩn Bootstrap 5, tinh tế, sang trọng. |
| **Chương 4: Models, ORM & Migrations** | Định nghĩa thực thể, kiểu dữ liệu, khóa ngoại `ForeignKey`, `OneToOneField`, `makemigrations`, `migrate`, ORM Queries. | Xây dựng ERD hoàn chỉnh với `Category`, `Product`, `ProductVariant`, `Cart`, `Order`, `Review`, xử lý quan hệ 1-N, 1-1, truy vấn dữ liệu an toàn. |
| **Chương 5: Forms & Validation** | `forms.Form`, `forms.ModelForm`, `is_valid()`, `clean()`, CSRF token. | Xây dựng form đăng ký, form đặt hàng (CheckoutForm), form nhập sản phẩm, kiểm tra tồn kho, kiểm tra giá > 0, validate số điện thoại. |
| **Chương 6: Authentication & Authorization** | `User`, `authenticate()`, `login()`, `logout()`, `@login_required`, phân quyền Admin/Customer. | Bảo vệ trang quản trị, bảo vệ trang lịch sử đơn hàng, chỉ cho phép khách hàng xem đơn của chính họ, ngăn chặn người ngoài sửa sản phẩm. |
| **Chương 7: Django REST Framework (DRF)** | `ModelSerializer`, Generic Views (`ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`), Permissions. | Cung cấp RESTful API cho danh mục và sản phẩm (`/api/products/`), hỗ trợ xem và thao tác dữ liệu chuẩn JSON. |
| **Chương 8: Testing, Debugging & Deployment Readiness** | Kiểm thử chức năng, xử lý lỗi 404, 500, tối ưu câu truy vấn ORM, tài liệu bàn giao. | Viết báo cáo kiểm thử toàn diện (Auth, Cart, Order, Admin, API), chuẩn bị kịch bản thuyết trình bảo vệ đồ án. |
