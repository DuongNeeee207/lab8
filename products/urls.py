from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Giao diện khách hàng
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.category_products, name='category_products'),
    path('search/', views.product_search, name='search'),
    path('detail/<slug:product_slug>/', views.product_detail, name='product_detail'),

    # Giao diện quản trị Admin
    path('management/products/', views.admin_product_list, name='admin_product_list'),
    path('management/products/add/', views.admin_product_add, name='admin_product_add'),
    path('management/products/<int:pk>/edit/', views.admin_product_edit, name='admin_product_edit'),
    path('management/products/<int:pk>/delete/', views.admin_product_delete, name='admin_product_delete'),
    path('management/products/<int:pk>/variants/', views.admin_variants, name='admin_variants'),
    path('management/variants/<int:pk>/delete/', views.admin_variant_delete, name='admin_variant_delete'),
    path('management/categories/', views.admin_category_list, name='admin_category_list'),
    path('management/categories/<int:pk>/delete/', views.admin_category_delete, name='admin_category_delete'),
]
