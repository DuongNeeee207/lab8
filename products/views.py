from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, ProductVariant
from .forms import ProductForm, ProductVariantForm, CategoryForm
from reviews.forms import ReviewForm

def is_admin_user(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def product_list(request):
    """Hiển thị danh sách tất cả sản phẩm thời trang kèm lọc và phân trang"""
    products = Product.objects.filter(is_active=True).select_related('category').prefetch_related('variants')

    # Lọc theo danh mục
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    # Lọc theo khoảng giá
    price_range = request.GET.get('price')
    if price_range == 'under_300':
        products = products.filter(price__lt=300000)
    elif price_range == '300_700':
        products = products.filter(price__gte=300000, price__lte=700000)
    elif price_range == 'over_700':
        products = products.filter(price__gt=700000)

    # Sắp xếp
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')

    # Phân trang: 9 sản phẩm mỗi trang
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'sort_by': sort_by,
        'price_range': price_range,
        'total_count': products.count(),
    })


def category_products(request, category_slug):
    """Hiển thị sản phẩm theo một danh mục cụ thể"""
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, is_active=True).prefetch_related('variants').order_by('-created_at')

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        'selected_category': category,
        'total_count': products.count(),
    })


def product_search(request):
    """Tìm kiếm sản phẩm theo từ khóa"""
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(is_active=True)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        'search_query': query,
        'total_count': products.count(),
    })


def product_detail(request, product_slug):
    """Trang chi tiết sản phẩm thời trang"""
    product = get_object_or_404(Product.objects.prefetch_related('variants', 'reviews__user'), slug=product_slug)
    variants = product.variants.all()
    reviews = product.reviews.all()
    review_form = ReviewForm()

    # Lấy danh sách sản phẩm liên quan cùng danh mục
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]

    return render(request, 'products/product_detail.html', {
        'product': product,
        'variants': variants,
        'reviews': reviews,
        'review_form': review_form,
        'related_products': related_products,
    })


# -------------------- QUẢN TRỊ VIÊN (ADMIN VIEWS) --------------------

@login_required
@user_passes_test(is_admin_user)
def admin_product_list(request):
    """Quản lý danh sách sản phẩm cho Admin"""
    products = Product.objects.select_related('category').prefetch_related('variants').order_by('-created_at')
    return render(request, 'products/admin_product_list.html', {'products': products})


@login_required
@user_passes_test(is_admin_user)
def admin_product_add(request):
    """Thêm mới sản phẩm thời trang"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Đã thêm sản phẩm '{product.name}' thành công! Vui lòng thêm các biến thể kích cỡ và màu sắc.")
            return redirect('products:admin_variants', pk=product.pk)
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin nhập.")
    else:
        form = ProductForm()
    return render(request, 'products/admin_product_form.html', {'form': form, 'title': 'Thêm sản phẩm mới'})


@login_required
@user_passes_test(is_admin_user)
def admin_product_edit(request, pk):
    """Chỉnh sửa thông tin sản phẩm"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Đã cập nhật sản phẩm '{product.name}' thành công!")
            return redirect('products:admin_product_list')
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin nhập.")
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/admin_product_form.html', {'form': form, 'product': product, 'title': f"Sửa sản phẩm: {product.name}"})


@login_required
@user_passes_test(is_admin_user)
def admin_product_delete(request, pk):
    """Xóa sản phẩm"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f"Đã xóa vĩnh viễn sản phẩm '{name}'.")
    return redirect('products:admin_product_list')


@login_required
@user_passes_test(is_admin_user)
def admin_variants(request, pk):
    """Quản lý các biến thể kích cỡ / màu sắc / tồn kho của một sản phẩm"""
    product = get_object_or_404(Product, pk=pk)
    variants = product.variants.all()

    if request.method == 'POST':
        form = ProductVariantForm(request.POST)
        if form.is_valid():
            variant = form.save(commit=False)
            variant.product = product
            try:
                variant.save()
                messages.success(request, f"Đã thêm biến thể Size {variant.size} - {variant.color} (Tồn kho: {variant.stock_quantity}).")
                return redirect('products:admin_variants', pk=product.pk)
            except Exception as e:
                messages.error(request, f"Lỗi: Biến thể với Size và Màu này hoặc SKU này đã tồn tại.")
        else:
            messages.error(request, "Dữ liệu biến thể không hợp lệ.")
    else:
        # Tự động gợi ý SKU
        suggested_sku = f"FS-{product.pk}-{len(variants)+1:02d}"
        form = ProductVariantForm(initial={'sku': suggested_sku})

    return render(request, 'products/admin_variants.html', {
        'product': product,
        'variants': variants,
        'form': form
    })


@login_required
@user_passes_test(is_admin_user)
def admin_variant_delete(request, pk):
    """Xóa một biến thể sản phẩm"""
    variant = get_object_or_404(ProductVariant, pk=pk)
    product_pk = variant.product.pk
    if request.method == 'POST':
        variant.delete()
        messages.success(request, "Đã xóa biến thể thành công.")
    return redirect('products:admin_variants', pk=product_pk)


@login_required
@user_passes_test(is_admin_user)
def admin_category_list(request):
    """Quản lý danh mục sản phẩm (Thêm mới, danh sách)"""
    categories = Category.objects.all().order_by('name')
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save()
            messages.success(request, f"Đã thêm danh mục mới: '{cat.name}'")
            return redirect('products:admin_category_list')
        else:
            messages.error(request, "Dữ liệu danh mục không hợp lệ.")
    else:
        form = CategoryForm()

    return render(request, 'products/admin_category_list.html', {
        'categories': categories,
        'form': form
    })


@login_required
@user_passes_test(is_admin_user)
def admin_category_delete(request, pk):
    """Xóa danh mục sản phẩm"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f"Đã xóa danh mục '{name}'.")
    return redirect('products:admin_category_list')
