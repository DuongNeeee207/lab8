from django import forms
from .models import Product, ProductVariant, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']
        labels = {
            'name': 'Tên danh mục',
            'description': 'Mô tả tóm tắt',
            'image': 'Ảnh danh mục',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: Áo Sơ Mi Nam'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Giới thiệu về dòng sản phẩm...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'sale_price', 'image', 'is_active']
        labels = {
            'category': 'Danh mục sản phẩm',
            'name': 'Tên sản phẩm',
            'description': 'Mô tả sản phẩm (chất liệu, form dáng)',
            'price': 'Giá bán gốc (VNĐ)',
            'sale_price': 'Giá ưu đãi / khuyến mãi (VNĐ - tùy chọn)',
            'image': 'Ảnh đại diện chính',
            'is_active': 'Bật kinh doanh (hiển thị trên website)',
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: Áo Sơ Mi Oxford Dài Tay'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Chất liệu 100% cotton cao cấp...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: 450000'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: 390000'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Giá sản phẩm phải lớn hơn 0 VNĐ.")
        return price

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        sale_price = cleaned_data.get('sale_price')
        if sale_price and price and sale_price >= price:
            self.add_error('sale_price', "Giá khuyến mãi phải nhỏ hơn giá gốc.")
        return cleaned_data


class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['size', 'color', 'sku', 'stock_quantity']
        labels = {
            'size': 'Kích cỡ (Size)',
            'color': 'Màu sắc',
            'sku': 'Mã SKU kho',
            'stock_quantity': 'Số lượng tồn kho',
        }
        widgets = {
            'size': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: Trắng'}),
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: FS-SHIRT-WHT-M'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

    def clean_stock_quantity(self):
        qty = self.cleaned_data.get('stock_quantity')
        if qty is not None and qty < 0:
            raise forms.ValidationError("Số lượng tồn kho không được âm.")
        return qty
