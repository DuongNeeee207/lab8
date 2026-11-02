from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from products.models import Product, Category
from orders.models import Order
from .forms import ContactForm

def is_admin_user(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def home_view(request):
    """Trang chủ FashionStore với phong cách thời trang tối giản, cao cấp"""
    categories = Category.objects.all()
    new_arrivals = Product.objects.filter(is_active=True).select_related('category').prefetch_related('variants').order_by('-created_at')[:8]
    sale_products = Product.objects.filter(is_active=True, sale_price__gt=0).select_related('category')[:4]

    return render(request, 'core/home.html', {
        'featured_categories': categories,
        'new_arrivals': new_arrivals,
        'sale_products': sale_products,
    })


def about_view(request):
    """Trang Giới thiệu thương hiệu FashionStore"""
    return render(request, 'core/about.html')


def contact_view(request):
    """Trang Liên hệ & Gửi thắc mắc"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Cảm ơn bạn đã liên hệ! Đội ngũ FashionStore sẽ phản hồi bạn trong thời gian sớm nhất.")
            return redirect('core:contact')
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin trong biểu mẫu.")
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})


@login_required
@user_passes_test(is_admin_user)
def admin_dashboard(request):
    """Bảng điều khiển quản trị tổng quan số liệu kinh doanh"""
    # 1. Tổng doanh thu (từ các đơn hàng đã thanh toán hoặc đã giao)
    revenue_data = Order.objects.exclude(order_status='Cancelled').aggregate(total_revenue=Sum('total_amount'))
    total_revenue = revenue_data['total_revenue'] or 0

    # 2. Số lượng đơn hàng theo trạng thái
    pending_orders = Order.objects.filter(order_status='Pending').count()
    shipping_orders = Order.objects.filter(order_status='Shipping').count()
    completed_orders = Order.objects.filter(order_status='Delivered').count()
    total_orders = Order.objects.count()

    # 3. Sản phẩm và khách hàng
    total_products = Product.objects.count()
    total_customers = User.objects.filter(is_staff=False).count()

    # 4. Danh sách 6 đơn hàng mới nhất
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:6]

    return render(request, 'core/admin_dashboard.html', {
        'total_revenue': total_revenue,
        'pending_orders': pending_orders,
        'shipping_orders': shipping_orders,
        'completed_orders': completed_orders,
        'total_orders': total_orders,
        'total_products': total_products,
        'total_customers': total_customers,
        'recent_orders': recent_orders,
    })
