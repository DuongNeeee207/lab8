from django import forms

class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=100, label="Họ và tên",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nguyễn Văn A'}))
    email = forms.EmailField(label="Email liên hệ",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}))
    subject = forms.CharField(max_length=150, label="Tiêu đề yêu cầu",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hỏi về kích cỡ sản phẩm, chính sách đổi hàng...'}))
    message = forms.CharField(label="Nội dung tin nhắn",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Nội dung chi tiết...'}))
