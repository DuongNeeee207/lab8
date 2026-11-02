from rest_framework import serializers
from .models import Product, ProductVariant, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at']


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'size', 'color', 'sku', 'stock_quantity']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    variants = ProductVariantSerializer(many=True, read_only=True)
    final_price = serializers.ReadOnlyField(source='get_final_price')
    total_stock = serializers.ReadOnlyField(source='get_total_stock')
    average_rating = serializers.ReadOnlyField(source='get_average_rating')

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'category_name', 'name', 'slug', 'description',
            'price', 'sale_price', 'final_price', 'image', 'is_active',
            'total_stock', 'average_rating', 'variants', 'created_at', 'updated_at'
        ]
