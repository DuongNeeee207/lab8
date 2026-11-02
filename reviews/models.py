from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Review(models.Model):
    RATING_CHOICES = [
        (5, '★★★★★ (5 Sao - Tuyệt vời)'),
        (4, '★★★★☆ (4 Sao - Tốt)'),
        (3, '★★★☆☆ (3 Sao - Bình thường)'),
        (2, '★★☆☆☆ (2 Sao - Kém)'),
        (1, '★☆☆☆☆ (1 Sao - Rất tệ)'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Sản phẩm')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Người đánh giá')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5, verbose_name='Số sao đánh giá')
    comment = models.TextField(verbose_name='Nhận xét chi tiết')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời gian đánh giá')

    class Meta:
        verbose_name = 'Đánh giá sản phẩm'
        verbose_name_plural = 'Đánh giá sản phẩm'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} đánh giá {self.product.name} ({self.rating} sao)"
