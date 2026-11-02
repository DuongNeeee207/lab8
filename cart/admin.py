from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('get_subtotal',)

    def get_subtotal(self, instance):
        return f"{instance.get_subtotal():,} VNĐ" if instance.pk else "0 VNĐ"
    get_subtotal.short_description = 'Thành tiền'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total_items', 'get_total_price_display', 'updated_at')
    inlines = [CartItemInline]

    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Số lượng món'

    def get_total_price_display(self, obj):
        return f"{obj.get_total_price():,} VNĐ"
    get_total_price_display.short_description = 'Tổng tiền'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product_variant', 'quantity', 'added_at')
