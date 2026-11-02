def cart_context(request):
    """
    Context processor cung cấp số lượng món hàng và tổng tiền giỏ hàng
    cho toàn bộ các template (hiển thị badge giỏ hàng trên navbar).
    """
    cart_count = 0
    cart_total = 0
    if request.user.is_authenticated:
        try:
            from cart.models import Cart
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                cart_count = cart.get_total_items()
                cart_total = cart.get_total_price()
        except Exception:
            pass
    return {
        'nav_cart_count': cart_count,
        'nav_cart_total': cart_total,
    }
