from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile

class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, label="Họ đệm",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: Nguyễn Văn'}))
    last_name = forms.CharField(max_length=50, required=True, label="Tên",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: An'}))
    email = forms.EmailField(required=True, label="Địa chỉ Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}))
    password = forms.CharField(label="Mật khẩu",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập ít nhất 8 ký tự'}))
    confirm_password = forms.CharField(label="Xác nhận mật khẩu",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập lại mật khẩu'}))
    phone_number = forms.CharField(max_length=15, required=False, label="Số điện thoại",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0912345678'}))
    address = forms.CharField(required=False, label="Địa chỉ giao hàng",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số nhà, tên đường, phường/xã, quận/huyện'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Tên đăng nhập (Username)',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: user123'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Tên đăng nhập này đã có người sử dụng. Vui lòng chọn tên khác.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Địa chỉ email này đã được đăng ký tài khoản.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')
        if pwd and confirm and pwd != confirm:
            self.add_error('confirm_password', "Mật khẩu xác nhận không trùng khớp.")
        if pwd and len(pwd) < 8:
            self.add_error('password', "Mật khẩu phải chứa ít nhất 8 ký tự.")
        return cleaned_data


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Tên đăng nhập",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên tài khoản', 'autofocus': True}))
    password = forms.CharField(label="Mật khẩu",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật khẩu'}))


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, label="Họ đệm",
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, required=True, label="Tên",
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'avatar']
        labels = {
            'phone_number': 'Số điện thoại',
            'address': 'Địa chỉ giao hàng mặc định',
            'avatar': 'Ảnh đại diện',
        }
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }
