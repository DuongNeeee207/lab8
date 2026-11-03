# 🛍️ FASHIONSTORE — WEBSITE THƯƠNG MẠI ĐIỆN TỬ THỜI TRANG

> **Đồ Án Môn Học / Dự Án Chuyên Ngành Python & Django Framework**  
> Ứng dụng web bán hàng thời trang hoàn chỉnh theo kiến trúc MTV (Model - Template - View) với giao diện tối giản hiện đại (Minimalist Fashion) tương thích hoàn hảo mọi thiết bị.

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django_REST_Framework-3.14+-red.svg)](https://www.django-rest-framework.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.3-purple.svg)](https://getbootstrap.com/)
[![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)](https://www.sqlite.org/)

---

## ⚡ CÁCH CHẠY DỰ ÁN NHANH NHẤT (CHỈ CẦN 1 BƯỚC)

Dự án đã được tích hợp sẵn:
- **Cơ sở dữ liệu SQLite (`db.sqlite3`)** đầy đủ hơn 70+ sản phẩm thật, 7 danh mục, hình ảnh thời trang thực tế và tài khoản mẫu.
- **Thư mục ảnh (`media/`)** đi kèm đầy đủ, không cần seed hay tải lại.

### 👉 Dành cho Windows:
1. Tải repository về máy (Tải ZIP hoặc `git clone`).
2. Mở thư mục dự án và **nhấp đúp chuột vào file `run.bat`**.
3. **Xong!** File `run.bat` sẽ tự động:
   - Nhận diện Python trên máy tính của bạn.
   - Tự động cài đặt thư viện (`requirements.txt`) nếu máy bạn chưa có.
   - Khởi chạy server Django và **tự động mở trình duyệt web** tại: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

### 💻 Cách Chạy Thủ Công Qua Terminal / PowerShell:

```powershell
# 1. Di chuyển vào thư mục dự án
cd lab8-main

# 2. Cài đặt các thư viện cần thiết (nếu chưa cài)
pip install -r requirements.txt

# 3. Khởi chạy máy chủ Django
python manage.py runserver
```

Truy cập website tại: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔑 TÀI KHOẢN MẪU ĐĂNG NHẬP HỆ THỐNG

| Vai trò | Tên đăng nhập (`username`) | Mật khẩu (`password`) | Quyền hạn & Chức năng |
| :--- | :--- | :--- | :--- |
| **Quản trị viên (Admin)** | `admin` | `admin123` | Quản lý sản phẩm, đơn hàng, duyệt đánh giá, bảng điều khiển doanh thu (`/management/dashboard/`), Django Admin (`/admin/`) |
| **Khách hàng (Customer)** | `khachhang` | `customer123` | Mua sắm, giỏ hàng, đặt hàng COD, xem lịch sử đơn hàng (`/orders/history/`), gửi đánh giá |

---

## ✨ CÁC TÍNH NĂNG NỔI BẬT

### 1. Giao Diện Thời Trang Tối Giản (Minimalist Fashion)
- Phong cách thẩm mỹ tinh tế lấy cảm hứng từ Zara, Routine, COS và Uniqlo.
- **Tương thích 100% mọi thiết bị**: Desktop, Laptop, iPad/Tablet và Smartphone.
- **Mobile Bottom Navigation Bar**: Thanh điều hướng cố định chân màn hình điện thoại tiện lợi, hiện đại như một ứng dụng Native App.

### 2. Định Dạng Giá Chuẩn Tiền Việt (VNĐ)
- Toàn bộ giá niêm yết, khuyến mãi, thành tiền và tổng đơn được định dạng có dấu chấm phân cách hàng nghìn rõ ràng: **`189.000₫`**, **`1.290.000₫`**.

### 3. Trải Nghiệm Người Dùng Mượt Mà (Smart Auth Popup)
- Nút tài khoản trên thanh Navbar được tinh gọn thành 1 icon sang trọng.
- Khi người dùng chưa đăng nhập bấm vào bất kỳ tính năng nào cần tài khoản (**Giỏ hàng**, **Thêm vào giỏ**, **Đánh giá**, **Đặt hàng**), hệ thống sẽ **tự động bật Popup Modal** để chọn nhanh **Đăng Nhập** hoặc **Đăng Ký** mà không làm gián đoạn trải nghiệm duyệt web.

### 4. Quản Lý Sản Phẩm & Biến Thể Đa Dạng
- Hơn 70+ sản phẩm thuộc 7 danh mục: Áo Thun & Polo, Áo Sơ Mi, Áo Khoác & Blazer, Quần Jeans & Tây, Váy & Đầm, Áo Hoodie & Nỉ, Phụ Kiện.
- Hỗ trợ đa dạng biến thể: Kích cỡ (S, M, L, XL, XXL, Freesize), màu sắc, SKU riêng biệt và kiểm soát tồn kho realtime.

### 5. Giỏ Hàng & Quy Trình Đặt Hàng COD Nguyên Tử (Atomic Checkout)
- Thêm, sửa số lượng, xóa sản phẩm trong giỏ hàng tức thì.
- Đặt hàng thanh toán khi nhận hàng (COD) với `transaction.atomic()` đảm bảo an toàn dữ liệu: trừ kho chính xác khi đặt hàng và tự động hoàn trả số lượng vào kho nếu đơn hàng bị hủy.

### 6. Bảng Điều Khiển Quản Trị & REST API
- Bảng điều khiển riêng (`/management/dashboard/`) thống kê tổng doanh thu, số đơn chờ xử lý, đang giao, hoàn thành.
- Tích hợp Django REST Framework (DRF) cung cấp API cho sản phẩm và danh mục tại `/api/products/` và `/api/categories/`.

---

## 📁 CẤU TRÚC THƯ MỤC DỰ ÁN

```text
lab8-main/
├── accounts/               # Ứng dụng tài khoản, hồ sơ khách hàng, phân quyền
├── cart/                   # Ứng dụng giỏ hàng & tính toán tạm tính
├── core/                   # Trang chủ, giới thiệu, liên hệ, dashboard & template tags
│   └── templatetags/       # Bộ lọc tiền tệ VND chuẩn (vnd, vnd_text)
├── docs/                   # Toàn bộ tài liệu báo cáo, ERD, kịch bản bảo vệ
├── fashionstore/           # Cấu hình dự án Django chính (settings, urls, wsgi)
├── media/                  # Thư mục lưu trữ hình ảnh sản phẩm & danh mục
├── orders/                 # Quản lý đặt hàng, thanh toán COD, lịch sử giao dịch
├── products/               # Quản lý sản phẩm, danh mục, biến thể size/màu & API
├── reviews/                # Đánh giá & bình luận sản phẩm
├── static/                 # Tài nguyên tĩnh CSS, JavaScript, Fonts, Images
│   ├── css/style.css       # CSS tùy biến phong cách thời trang tối giản
│   └── js/main.js          # JavaScript xử lý tương tác, tìm kiếm & auth popup
├── templates/              # Giao diện HTML (Jinja/Django Templates)
├── db.sqlite3              # Cơ sở dữ liệu SQLite đã nạp sẵn dữ liệu thực tế
├── manage.py               # Lệnh quản trị Django
├── requirements.txt        # Danh sách thư viện Python phụ thuộc
└── run.bat                 # File khởi chạy nhanh 1-click cho Windows
```

---

## 📚 TÀI LIỆU DỰ ÁN CHI TIẾT

Trong thư mục `docs/` có đầy đủ các tài liệu phục vụ báo cáo và thuyết trình:
- [docs/project_overview.md](docs/project_overview.md): Tổng quan dự án & chuẩn hóa kiến trúc MTV.
- [docs/requirements.md](docs/requirements.md): Đặc tả yêu cầu chức năng & phi chức năng.
- [docs/erd.md](docs/erd.md): Sơ đồ thực thể liên kết (Mermaid ERD) chi tiết các bảng.
- [docs/page_list.md](docs/page_list.md): Danh mục toàn bộ URL, Views và Templates.
- [docs/test_report.md](docs/test_report.md): Báo cáo kết quả kiểm thử tự động.
- [docs/presentation_guide.md](docs/presentation_guide.md): 10 câu hỏi cốt lõi và kịch bản thuyết trình bảo vệ đồ án.

---

## 🛡️ BẢN QUYỀN & GIẤY PHÉP

Dự án được xây dựng phục vụ mục đích học tập và nghiên cứu. Phát hành theo giấy phép [MIT License](LICENSE).
