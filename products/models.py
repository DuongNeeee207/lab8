from django.db import models
from django.utils.text import slugify
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Tên danh mục')
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name='Đường dẫn slug')
    description = models.TextField(blank=True, verbose_name='Mô tả danh mục')
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name='Ảnh danh mục')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')

    class Meta:
        verbose_name = 'Danh mục sản phẩm'
        verbose_name_plural = 'Danh mục sản phẩm'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Danh mục')
    name = models.CharField(max_length=200, verbose_name='Tên sản phẩm')
    slug = models.SlugField(max_length=250, unique=True, blank=True, verbose_name='Đường dẫn slug')
    description = models.TextField(verbose_name='Mô tả chi tiết')
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Giá gốc (VNĐ)')
    sale_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='Giá khuyến mãi (VNĐ)')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Ảnh sản phẩm chính')
    is_active = models.BooleanField(default=True, verbose_name='Bật hiển thị')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Cập nhật lần cuối')

    class Meta:
        verbose_name = 'Sản phẩm'
        verbose_name_plural = 'Sản phẩm'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_final_price(self):
        """Trả về giá khuyến mãi nếu có và nhỏ hơn giá gốc, ngược lại trả về giá gốc"""
        if self.sale_price and self.sale_price > 0 and self.sale_price < self.price:
            return self.sale_price
        return self.price

    def is_on_sale(self):
        return self.sale_price is not None and self.sale_price > 0 and self.sale_price < self.price

    def get_total_stock(self):
        """Tính tổng số lượng tồn kho của tất cả các biến thể"""
        total = self.variants.aggregate(total_stock=models.Sum('stock_quantity'))['total_stock']
        return total if total is not None else 0

    def get_average_rating(self):
        """Tính điểm đánh giá trung bình từ các review"""
        avg = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return round(avg, 1) if avg else 5.0


class ProductVariant(models.Model):
    SIZE_CHOICES = [
        ('S', 'Size S'),
        ('M', 'Size M'),
        ('L', 'Size L'),
        ('XL', 'Size XL'),
        ('XXL', 'Size XXL'),
        ('FREESIZE', 'Freesize'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name='Sản phẩm')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='M', verbose_name='Kích cỡ (Size)')
    color = models.CharField(max_length=50, default='Trắng', verbose_name='Màu sắc')
    sku = models.CharField(max_length=60, unique=True, verbose_name='Mã định danh kho (SKU)')
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name='Số lượng tồn kho')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')

    class Meta:
        verbose_name = 'Biến thể sản phẩm'
        verbose_name_plural = 'Biến thể sản phẩm'
        unique_together = ('product', 'size', 'color')

    def __str__(self):
        return f"{self.product.name} - [{self.size} / {self.color}] (Còn {self.stock_quantity})"
