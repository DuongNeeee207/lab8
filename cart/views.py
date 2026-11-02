from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from products.models import ProductVariant
from .models import Cart, CartItem

def get_or_create_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

@login_required
def cart_detail(request):
    """Trang chi tiết giỏ hàng của khách hàng"""
    cart = get_or_create_user_cart(request.user)
    items = cart.items.select_related('product_variant__product').all()
    total_price = cart.get_total_price()
    total_items = cart.get_total_items()

    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'items': items,
        'total_price': total_price,
        'total_items': total_items,
    })

@login_required
@require_POST
def cart_add(request, variant_id):
    """Thêm một biến thể sản phẩm vào giỏ hàng"""
    variant = get_object_or_404(ProductVariant.objects.select_related('product'), pk=variant_id)
    cart = get_or_create_user_cart(request.user)

    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            quantity = 1
    except ValueError:
        quantity = 1

    # Kiểm tra tồn kho
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product_variant=variant)
    current_in_cart = 0 if created else (cart_item.quantity - quantity)
    new_quantity = quantity if created else (cart_item.quantity + quantity)

    if new_quantity > variant.stock_quantity:
        messages.warning(
            request,
            f"Rất tiếc! Biến thể '{variant.product.name} (Size: {variant.size}, Màu: {variant.color})' chỉ còn {variant.stock_quantity} sản phẩm trong kho."
        )
        if created:
            cart_item.delete()
        return redirect('products:product_detail', product_slug=variant.product.slug)

    cart_item.quantity = new_quantity
    cart_item.save()

    messages.success(
        request,
        f"Đã thêm thành công {quantity} sản phẩm '{variant.product.name}' vào giỏ hàng!"
    )
    return redirect('cart:detail')

@login_required
@require_POST
def cart_update(request, item_id):
    """Cập nhật số lượng sản phẩm trong giỏ hàng"""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    action = request.POST.get('action')

    if action == 'increase':
        if cart_item.quantity + 1 > cart_item.product_variant.stock_quantity:
            messages.warning(request, f"Không thể tăng thêm. Kho chỉ còn {cart_item.product_variant.stock_quantity} sản phẩm.")
        else:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, "Đã cập nhật số lượng.")
    elif action == 'decrease':
        if cart_item.quantity - 1 <= 0:
            cart_item.delete()
            messages.info(request, "Đã xóa sản phẩm khỏi giỏ hàng.")
        else:
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(request, "Đã cập nhật số lượng.")

    return redirect('cart:detail')

@login_required
@require_POST
def cart_remove(request, item_id):
    """Xóa hoàn toàn một mục khỏi giỏ hàng"""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item_name = cart_item.product_variant.product.name
    cart_item.delete()
    messages.info(request, f"Đã xóa '{item_name}' khỏi giỏ hàng của bạn.")
    return redirect('cart:detail')
