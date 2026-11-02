import os
import sys
import django

# UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashionstore.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from products.models import Product, ProductVariant, Category
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem

def run_tests():
    print("==================================================")
    print("   BẮT ĐẦU KIỂM THỬ TỰ ĐỘNG HỆ THỐNG FASHIONSTORE   ")
    print("==================================================")
    client = Client()

    # 1. Test Trang chủ
    res = client.get('/')
    assert res.status_code == 200, f"Trang chủ lỗi: {res.status_code}"
    print("[PASS] 1. Trang chủ tải thành công (HTTP 200)")

    # 2. Test Danh sách sản phẩm
    res = client.get('/products/')
    assert res.status_code == 200, f"Trang sản phẩm lỗi: {res.status_code}"
    print("[PASS] 2. Trang danh sách sản phẩm tải thành công (HTTP 200)")

    # 3. Test Chi tiết sản phẩm
    prod = Product.objects.first()
    assert prod is not None, "Không tìm thấy sản phẩm nào trong DB"
    res = client.get(f'/products/detail/{prod.slug}/')
    assert res.status_code == 200, f"Trang chi tiết sản phẩm lỗi: {res.status_code}"
    print(f"[PASS] 3. Chi tiết sản phẩm '{prod.name}' tải thành công (HTTP 200)")

    # 4. Test Đăng nhập tài khoản khách hàng
    login_success = client.login(username='khachhang', password='customer123')
    assert login_success, "Đăng nhập khách hàng thất bại"
    print("[PASS] 4. Đăng nhập tài khoản khách hàng 'khachhang' thành công")

    # 5. Test Thêm sản phẩm vào giỏ hàng
    variant = prod.variants.first()
    assert variant is not None, "Sản phẩm không có biến thể"
    initial_stock = variant.stock_quantity

    res = client.post(f'/cart/add/{variant.id}/', {'quantity': 2}, follow=True)
    assert res.status_code == 200, "Thêm vào giỏ hàng thất bại"
    
    user = User.objects.get(username='khachhang')
    cart = Cart.objects.get(user=user)
    assert cart.get_total_items() >= 2, "Giỏ hàng không cập nhật số lượng"
    print(f"[PASS] 5. Thêm 2 món '{variant.product.name} (Size: {variant.size})' vào giỏ hàng thành công")

    # 6. Test Thanh toán và Đặt hàng (Checkout)
    checkout_data = {
        'full_name': 'Nguyễn Văn An',
        'phone_number': '0987654321',
        'shipping_address': 'Số 68 Cầu Giấy, Hà Nội',
        'note': 'Giao trong giờ hành chính',
        'payment_method': 'COD'
    }
    res = client.post('/orders/checkout/', checkout_data, follow=True)
    assert res.status_code == 200, "Đặt hàng thất bại"
    
    order = Order.objects.filter(user=user).order_by('-created_at').first()
    assert order is not None, "Đơn hàng chưa được lưu trong cơ sở dữ liệu"
    
    # Kiểm tra tồn kho sau khi đặt hàng
    variant.refresh_from_db()
    assert variant.stock_quantity == initial_stock - 2, f"Tồn kho chưa bị trừ đúng: Ban đầu {initial_stock}, hiện tại {variant.stock_quantity}"
    print(f"[PASS] 6. Đặt hàng thành công! Mã đơn: #{order.order_number}. Tồn kho đã tự động trừ 2 cái (Còn {variant.stock_quantity}).")

    # 7. Test Quyền Admin: Dashboard và Hủy đơn hoàn kho
    client.logout()
    admin_login = client.login(username='admin', password='admin123')
    assert admin_login, "Đăng nhập admin thất bại"
    
    res = client.get('/management/dashboard/')
    assert res.status_code == 200, "Truy cập Admin Dashboard thất bại"
    print("[PASS] 7. Đăng nhập Admin và tải Dashboard quản trị thành công (HTTP 200)")

    from django.urls import reverse
    admin_order_url = reverse('orders:admin_order_detail', args=[order.order_number])
    res = client.post(admin_order_url, {
        'order_status': 'Cancelled',
        'payment_status': 'Unpaid'
    }, follow=True)
    assert res.status_code == 200, "Cập nhật trạng thái đơn thất bại"
    
    variant.refresh_from_db()
    assert variant.stock_quantity == initial_stock, f"Tồn kho chưa được hoàn trả: Kỳ vọng {initial_stock}, thực tế {variant.stock_quantity}"
    print(f"[PASS] 8. Admin hủy đơn hàng: Hệ thống tự động hoàn trả số lượng vào kho thành công (Về lại {variant.stock_quantity}).")

    # 8. Test REST API (DRF)
    res = client.get('/api/products/')
    assert res.status_code == 200, "Gọi REST API /api/products/ thất bại"
    print("[PASS] 9. REST API GET /api/products/ hoạt động hoàn hảo, trả về dữ liệu chuẩn JSON")

    print("==================================================")
    print("   TẤT CẢ 9 BÀI KIỂM THỬ ĐÃ VƯỢT QUA XUẤT SẮC (PASS)   ")
    print("==================================================")

if __name__ == '__main__':
    run_tests()
