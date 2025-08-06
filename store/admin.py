from django.contrib import admin
from .models import Category, Product, ProductVariant

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('image', 'description', 'color_name', 'price')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]

# ✅ Add this to auto-fill slug
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')        # ✅ Show name and order in admin list
    list_editable = ('order',)              # ✅ Make order editable inline
    prepopulated_fields = {"slug": ("name",)}


