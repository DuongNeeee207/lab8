from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm

def is_admin_user(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def register_view(request):
    """Đăng ký tài khoản khách hàng mới"""
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Cập nhật thông tin Profile được tạo tự động bởi post_save signal
            profile = user.profile
            profile.phone_number = form.cleaned_data.get('phone_number', '')
            profile.address = form.cleaned_data.get('address', '')
            profile.save()

            # Đăng nhập tự động sau khi đăng ký thành công
            login(request, user)
            messages.success(request, f"Chào mừng {user.get_full_name() or user.username}! Bạn đã đăng ký tài khoản thành công.")
            return redirect('core:home')
        else:
            messages.error(request, "Đăng ký thất bại. Vui lòng kiểm tra lại thông tin nhập bên dưới.")
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Đăng nhập tài khoản"""
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Chào mừng bạn trở lại, {user.get_full_name() or user.username}!")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                if user.is_staff:
                    return redirect('core:admin_dashboard')
                return redirect('core:home')
            else:
                messages.error(request, "Tên đăng nhập hoặc mật khẩu không chính xác.")
        else:
            messages.error(request, "Thông tin đăng nhập không hợp lệ.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Đăng xuất tài khoản"""
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "Bạn đã đăng xuất thành công khỏi hệ thống FashionStore.")
    return redirect('core:home')


@login_required
def profile_view(request):
    """Xem và cập nhật thông tin cá nhân khách hàng"""
    profile = request.user.profile
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Hồ sơ cá nhân đã được cập nhật thành công!")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Cập nhật hồ sơ thất bại. Vui lòng kiểm tra các ô lỗi.")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    orders_count = request.user.orders.count()
    return render(request, 'accounts/profile.html', {
        'u_form': u_form,
        'p_form': p_form,
        'orders_count': orders_count,
    })


@login_required
@user_passes_test(is_admin_user)
def admin_customer_list(request):
    """Trang quản trị: Danh sách khách hàng trong hệ thống"""
    customers = User.objects.filter(is_staff=False).select_related('profile').order_by('-date_joined')
    return render(request, 'accounts/admin_customers.html', {
        'customers': customers
    })
