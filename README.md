# FASHIONSTORE — WEBSITE THƯƠNG MẠI ĐIỆN TỬ THỜI TRANG BẰNG DJANGO

> **Đồ án môn học / Dự án chuyên ngành Python & Django Framework**  
> Ứng dụng web bán hàng thời trang hoàn chỉnh, hiện đại theo chuẩn kiến trúc MTV (Model - Template - View).

---

## 1. TÀI KHOẢN MẪU DÙNG THỬ (DEMO CREDENTIALS)

Hệ thống đã được nạp sẵn dữ liệu mẫu thực tế (Sản phẩm, danh mục, biến thể size/màu, kho hàng):

| Vai trò | Tên đăng nhập (`username`) | Mật khẩu (`password`) | Chức năng truy cập |
| :--- | :--- | :--- | :--- |
| **Quản trị viên (Admin)** | `admin` | `admin123` | Bảng điều khiển quản trị (`/management/dashboard/`), Quản lý sản phẩm, tồn kho, đơn hàng, Django Admin (`/admin/`) |
| **Khách hàng (Customer)** | `khachhang` | `customer123` | Xem sản phẩm, giỏ hàng, đặt hàng COD, theo dõi lịch sử đơn hàng (`/orders/history/`), đánh giá |

---

## 2. HƯỚNG DẪN KHỞI CHẠY DỰ ÁN (QUICK START)

### Bước 1: Mở Terminal (PowerShell hoặc Command Prompt)
Di chuyển đến thư mục dự án:
```powershell
cd e:\lab8
```

### Bước 2: Kích hoạt môi trường ảo (Virtual Environment)
```powershell
# Trên Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Hoặc Command Prompt:
.\venv\Scripts\activate.bat
```

### Bước 3: Khởi chạy máy chủ phát triển (Development Server)
```powershell
python manage.py runserver 127.0.0.1:8000
```

### Bước 4: Mở trình duyệt và trải nghiệm
- **Trang chủ cửa hàng:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Danh sách sản phẩm:** [http://127.0.0.1:8000/products/](http://127.0.0.1:8000/products/)
- **Bảng điều khiển quản trị (Admin Dashboard):** [http://127.0.0.1:8000/management/dashboard/](http://127.0.0.1:8000/management/dashboard/)
- **Hệ thống Django Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **REST API (DRF):** [http://127.0.0.1:8000/api/products/](http://127.0.0.1:8000/api/products/)

---

## 3. CHẠY BỘ KIỂM THỬ TỰ ĐỘNG (AUTOMATED TEST SUITE)

Hệ thống đi kèm bộ kiểm thử tự động 9 kịch bản trọng yếu (Auth, Catalog, Cart, Atomic Checkout, Stock Decrement & Cancellation Stock Recovery, REST API):

```powershell
python test_suite.py
```

---

## 4. TÀI LIỆU DỰ ÁN CHI TIẾT (DOCUMENTATION DIRECTORY)

Tất cả tài liệu phân tích, thiết kế, báo cáo kiểm thử và kịch bản bảo vệ đồ án nằm trong thư mục `docs/`:

1. [docs/project_overview.md](docs/project_overview.md): Tổng quan dự án, nghiệp vụ kinh doanh, công nghệ sử dụng và ánh xạ với 8 chương của giáo trình.
2. [docs/requirements.md](docs/requirements.md): Đặc tả yêu cầu chức năng, phi chức năng và quy tắc nghiệp vụ cốt lõi.
3. [docs/erd.md](docs/erd.md): Sơ đồ thực thể liên kết (Mermaid ERD) và chi tiết các bảng dữ liệu.
4. [docs/page_list.md](docs/page_list.md): Danh mục toàn bộ URL, Views và Templates trong hệ thống.
5. [docs/wireframes.md](docs/wireframes.md): Thiết kế bố cục giao diện thời trang tối giản chuẩn phong cách Zara/H&M/Uniqlo.
6. [docs/test_report.md](docs/test_report.md): Báo cáo kết quả kiểm thử 19 trường hợp kiểm thử (100% PASS).
7. [docs/presentation_guide.md](docs/presentation_guide.md): 10 câu hỏi cốt lõi và kịch bản thuyết trình bảo vệ đồ án trước hội đồng.

---

## 5. CÔNG NGHỆ ÁP DỤNG
- **Ngôn ngữ:** Python 3.10
- **Framework:** Django 5.2 (Kiến trúc MTV, ORM, Forms, ModelForms, Authentication, Signals)
- **API:** Django REST Framework (DRF)
- **Frontend:** HTML5, CSS3 (Custom Minimalist Fashion Theme), Bootstrap 5, Bootstrap Icons, JavaScript
- **Cơ sở dữ liệu:** SQLite3
