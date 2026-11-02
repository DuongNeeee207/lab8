from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
    """
    API endpoint:
    - GET /api/products/ : Danh sách sản phẩm
    - POST /api/products/ : Thêm sản phẩm (Chỉ Admin)
    """
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('variants')
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint:
    - GET /api/products/<int:pk>/ : Chi tiết sản phẩm
    - PUT / PATCH /api/products/<int:pk>/ : Cập nhật sản phẩm (Chỉ Admin)
    - DELETE /api/products/<int:pk>/ : Xóa sản phẩm (Chỉ Admin)
    """
    queryset = Product.objects.all().select_related('category').prefetch_related('variants')
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]


class CategoryListAPIView(generics.ListAPIView):
    """
    API endpoint:
    - GET /api/categories/ : Danh sách danh mục sản phẩm
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
