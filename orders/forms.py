from django import forms
from .models import Order
import re

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone_number', 'shipping_address', 'note']
        labels = {
            'full_name': 'Họ và tên người nhận (*)',
            'phone_number': 'Số điện thoại nhận hàng (*)',
            'shipping_address': 'Địa chỉ giao hàng chi tiết (*)',
            'note': 'Ghi chú cho đơn hàng / shipper (tùy chọn)',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: Nguyễn Văn An'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: 0912345678'}),
            'shipping_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Số nhà, tên đường, phường/xã, quận/huyện, tỉnh/thành phố'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ví dụ: Giao hàng giờ hành chính, gọi trước khi giao...'}),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        # Kiểm tra định dạng số điện thoại Việt Nam (10 chữ số bắt đầu bằng số 0)
        phone_pattern = r'^(0[3|5|7|8|9])[0-9]{8}$'
        if not re.match(phone_pattern, phone):
            raise forms.ValidationError("Số điện thoại không hợp lệ. Vui lòng nhập 10 chữ số (Ví dụ: 0912345678).")
        return phone


class OrderStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_status', 'payment_status']
        labels = {
            'order_status': 'Trạng thái đơn hàng',
            'payment_status': 'Trạng thái thanh toán',
        }
        widgets = {
            'order_status': forms.Select(attrs={'class': 'form-select'}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
        }
