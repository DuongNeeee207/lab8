from django.db import models
from django.contrib.auth.models import User
from products.models import ProductVariant

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name='Người dùng')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Cập nhật lần cuối')

    class Meta:
        verbose_name = 'Giỏ hàng'
        verbose_name_plural = 'Giỏ hàng'

    def __str__(self):
        return f"Giỏ hàng của {self.user.username}"

    def get_total_items(self):
        """Tính tổng số lượng sản phẩm trong giỏ hàng"""
        total = self.items.aggregate(total_qty=models.Sum('quantity'))['total_qty']
        return total if total is not None else 0

    def get_total_price(self):
        """Tính tổng thành tiền của toàn bộ sản phẩm trong giỏ hàng"""
        total = sum(item.get_subtotal() for item in self.items.all())
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Giỏ hàng')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='cart_items', verbose_name='Biến thể sản phẩm')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Số lượng')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời gian thêm')

    class Meta:
        verbose_name = 'Món hàng trong giỏ'
        verbose_name_plural = 'Các món hàng trong giỏ'
        unique_together = ('cart', 'product_variant')

    def __str__(self):
        return f"{self.quantity} x {self.product_variant}"

    def get_subtotal(self):
        """Thành tiền cho từng dòng món hàng trong giỏ"""
        return self.product_variant.product.get_final_price() * self.quantity
