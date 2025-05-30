from django.contrib import admin
from .models import Product, Price, InventoryMovement, Category

# --------- Price Inline para Product ----------
class PriceInline(admin.TabularInline):
    model = Price
    extra = 1  # número de formularios extra para nuevos precios
    min_num = 1
    can_delete = True

# --------- Admin personalizado para Product ----------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'brand', 'brand_code', 'name')
    inlines = [PriceInline]
    search_fields = ('code', 'brand', 'name')

# --------- Admin para InventoryMovement ----------
@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'date')
    search_fields = ('product__code', 'product__name')
    list_filter = ('movement_type',)

# --------- Admin para Category ----------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
