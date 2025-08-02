from django.contrib import admin
from .models import Category, Product, ProductVariant

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('image', 'description', 'color', 'price')  # add price here
    # or if you want all fields automatically, you can use 'fields' or 'readonly_fields' as needed

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]

admin.site.register(Category)

