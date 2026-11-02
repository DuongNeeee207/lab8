from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from products.models import Product
from .forms import ReviewForm
from .models import Review

@login_required
@require_POST
def add_review(request, product_id):
    """Gửi đánh giá và nhận xét cho một sản phẩm"""
    product = get_object_or_404(Product, pk=product_id)
    form = ReviewForm(request.POST)

    if form.is_valid():
        # Kiểm tra xem người dùng đã từng đánh giá sản phẩm này chưa
        existing_review = Review.objects.filter(product=product, user=request.user).first()
        if existing_review:
            existing_review.rating = form.cleaned_data['rating']
            existing_review.comment = form.cleaned_data['comment']
            existing_review.save()
            messages.success(request, "Bạn đã cập nhật lại đánh giá cho sản phẩm này thành công!")
        else:
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Cảm ơn bạn đã gửi đánh giá cho sản phẩm!")
    else:
        messages.error(request, "Đánh giá không hợp lệ. Vui lòng nhập tối thiểu 5 ký tự nhận xét.")

    return redirect('products:product_detail', product_slug=product.slug)
