from django.db import models
from django.contrib.auth.models import User
from products.models import ProductVariant
import uuid

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Thanh toán khi nhận hàng (COD)'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Unpaid', 'Chưa thanh toán'),
        ('Paid', 'Đã thanh toán'),
    ]

    ORDER_STATUS_CHOICES = [
        ('Pending', 'Chờ xử lý'),
        ('Confirmed', 'Đã xác nhận'),
        ('Shipping', 'Đang giao hàng'),
        ('Delivered', 'Đã giao thành công'),
        ('Cancelled', 'Đã hủy'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name='Khách hàng')
    order_number = models.CharField(max_length=50, unique=True, verbose_name='Mã đơn hàng')
    full_name = models.CharField(max_length=100, verbose_name='Họ và tên người nhận')
    phone_number = models.CharField(max_length=15, verbose_name='Số điện thoại nhận hàng')
    shipping_address = models.TextField(verbose_name='Địa chỉ nhận hàng chi tiết')
    note = models.TextField(blank=True, verbose_name='Ghi chú đơn hàng')
    total_amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Tổng tiền đơn hàng (VNĐ)')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='COD', verbose_name='Phương thức thanh toán')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Unpaid', verbose_name='Trạng thái thanh toán')
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending', verbose_name='Trạng thái đơn hàng')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày đặt hàng')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Cập nhật lần cuối')

    class Meta:
        verbose_name = 'Đơn hàng'
        verbose_name_plural = 'Đơn hàng'
        ordering = ['-created_at']

    def __str__(self):
        return f"Đơn hàng #{self.order_number} - {self.full_name}"

    @classmethod
    def generate_order_number(cls):
        """Tạo mã đơn hàng duy nhất ngẫu nhiên, ví dụ: FS-A1B2C3D4"""
        return f"FS-{uuid.uuid4().hex[:8].upper()}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Đơn hàng')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Biến thể')
    product_name = models.CharField(max_length=200, verbose_name='Tên sản phẩm tại thời điểm mua')
    variant_info = models.CharField(max_length=100, verbose_name='Phân loại (Size & Màu)')
    unit_price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Đơn giá lúc mua (VNĐ)')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Số lượng')
    subtotal = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Thành tiền (VNĐ)')

    class Meta:
        verbose_name = 'Chi tiết đơn hàng'
        verbose_name_plural = 'Chi tiết đơn hàng'

    def __str__(self):
        return f"{self.quantity} x {self.product_name} ({self.variant_info})"
