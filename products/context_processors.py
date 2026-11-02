def category_context(request):
    """
    Context processor cung cấp danh sách tất cả các danh mục
    kèm sản phẩm liên quan cho Mega Menu trên Navbar.
    """
    try:
        from products.models import Category
        categories = Category.objects.prefetch_related('products').all()
    except Exception:
        categories = []
    return {
        'nav_categories': categories
    }
