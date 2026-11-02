from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from cart.models import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm, OrderStatusUpdateForm

def is_admin_user(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@login_required
def checkout_view(request):
    """Trang thanh toán đơn hàng (Checkout)"""
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or cart.items.count() == 0:
        messages.warning(request, "Giỏ hàng của bạn đang trống. Vui lòng chọn sản phẩm trước khi thanh toán.")
        return redirect('products:product_list')

    items = cart.items.select_related('product_variant__product').all()
    total_price = cart.get_total_price()

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # 1. Kiểm tra lại tồn kho tức thời của tất cả các mặt hàng
                    for item in items:
                        variant = item.product_variant
                        if item.quantity > variant.stock_quantity:
                            messages.error(
                                request,
                                f"Sản phẩm '{variant.product.name}' (Size: {variant.size}, Màu: {variant.color}) chỉ còn {variant.stock_quantity} cái trong kho. Vui lòng cập nhật lại giỏ hàng."
                            )
                            return redirect('cart:detail')

                    # 2. Tạo bản ghi Đơn hàng (Order)
                    order = form.save(commit=False)
                    order.user = request.user
                    order.order_number = Order.generate_order_number()
                    order.total_amount = total_price
                    order.payment_method = 'COD'
                    order.payment_status = 'Unpaid'
                    order.order_status = 'Pending'
                    order.save()

                    # 3. Tạo các dòng chi tiết đơn hàng (OrderItem) và trừ tồn kho
                    for item in items:
                        variant = item.product_variant
                        product = variant.product
                        unit_price = product.get_final_price()
                        subtotal = unit_price * item.quantity

                        OrderItem.objects.create(
                            order=order,
                            product_variant=variant,
                            product_name=product.name,
                            variant_info=f"Size: {variant.size}, Màu: {variant.color}",
                            unit_price=unit_price,
                            quantity=item.quantity,
                            subtotal=subtotal
                        )

                        # Trừ tồn kho
                        variant.stock_quantity -= item.quantity
                        variant.save()

                    # 4. Xóa sạch giỏ hàng sau khi đặt thành công
                    cart.items.all().delete()

                messages.success(request, f"Chúc mừng bạn đã đặt hàng thành công! Mã đơn: #{order.order_number}")
                return redirect('orders:success', order_number=order.order_number)

            except Exception as e:
                messages.error(request, f"Đã xảy ra lỗi trong quá trình tạo đơn hàng: {str(e)}")
        else:
            messages.error(request, "Vui lòng kiểm tra lại các thông tin giao nhận bắt buộc.")
    else:
        # Tự động điền thông tin sẵn có từ tài khoản & hồ sơ
        initial_data = {
            'full_name': request.user.get_full_name() or request.user.username,
            'phone_number': getattr(request.user.profile, 'phone_number', ''),
            'shipping_address': getattr(request.user.profile, 'address', ''),
        }
        form = CheckoutForm(initial=initial_data)

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart,
        'items': items,
        'total_price': total_price,
    })


@login_required
def order_success(request, order_number):
    """Trang xác nhận đặt hàng thành công"""
    if str(order_number).isdigit():
        order = Order.objects.prefetch_related('items').filter(id=int(order_number), user=request.user).first()
        if order:
            return render(request, 'orders/order_success.html', {'order': order})
    order = get_object_or_404(Order.objects.prefetch_related('items'), order_number=order_number, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_history(request):
    """Danh sách lịch sử đơn hàng của khách hàng đang đăng nhập"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_number):
    """Chi tiết một đơn hàng cụ thể của khách hàng (Hỗ trợ cả order_number và ID)"""
    order = None
    if str(order_number).isdigit():
        order = Order.objects.prefetch_related('items').filter(id=int(order_number)).first()
    if not order:
        order = Order.objects.prefetch_related('items').filter(order_number=order_number).first()
    
    if not order or (order.user != request.user and not request.user.is_staff):
        raise Http404("Không tìm thấy đơn hàng phù hợp.")

    return render(request, 'orders/order_detail.html', {'order': order})


# -------------------- QUẢN TRỊ VIÊN (ADMIN ORDER VIEWS) --------------------

@login_required
@user_passes_test(is_admin_user)
def admin_order_list(request):
    """Quản lý danh sách toàn bộ đơn hàng trong hệ thống"""
    orders = Order.objects.select_related('user').all().order_by('-created_at')

    # Lọc theo trạng thái
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(order_status=status_filter)

    return render(request, 'orders/admin_orders.html', {
        'orders': orders,
        'status_filter': status_filter,
    })


@login_required
@user_passes_test(is_admin_user)
def admin_order_detail(request, order_number):
    """Chi tiết và xử lý trạng thái đơn hàng của Admin"""
    order = get_object_or_404(Order.objects.prefetch_related('items__product_variant'), order_number=order_number)

    if request.method == 'POST':
        old_status = order.order_status
        form = OrderStatusUpdateForm(request.POST, instance=order)
        if form.is_valid():
            updated_order = form.save()
            new_status = updated_order.order_status

            # Xử lý hoàn kho nếu chuyển từ trạng thái khác sang Cancelled (Hủy đơn)
            if old_status != 'Cancelled' and new_status == 'Cancelled':
                for item in updated_order.items.all():
                    if item.product_variant:
                        item.product_variant.stock_quantity += item.quantity
                        item.product_variant.save()
                messages.warning(request, f"Đơn hàng #{order.order_number} đã bị hủy. Hệ thống đã hoàn lại số lượng sản phẩm vào kho.")
            else:
                messages.success(request, f"Đã cập nhật trạng thái đơn #{order.order_number} thành '{updated_order.get_order_status_display()}'.")
            return redirect('orders:admin_order_detail', order_number=order.order_number)
        else:
            messages.error(request, "Dữ liệu trạng thái không hợp lệ.")
    else:
        form = OrderStatusUpdateForm(instance=order)

    return render(request, 'orders/admin_order_detail.html', {
        'order': order,
        'form': form,
    })
