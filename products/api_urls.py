from django.urls import path
from . import api_views

app_name = 'api'

urlpatterns = [
    path('products/', api_views.ProductListCreateAPIView.as_view(), name='product_list_create'),
    path('products/<int:pk>/', api_views.ProductDetailAPIView.as_view(), name='product_detail'),
    path('categories/', api_views.CategoryListAPIView.as_view(), name='category_list'),
]
