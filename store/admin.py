from django import forms
from django.contrib import admin
from .models import Category, Product, ProductVariant, ProductVariantImage

# Custom form to make the description field bigger
class ProductVariantAdminForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10, 'cols': 80}),  # bigger textarea
        }

# Inline for extra images for a variant
class ProductVariantImageInline(admin.TabularInline):
    model = ProductVariantImage
    extra = 1

# Inline for variants in a product
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('image', 'description', 'color_name', 'color_codes', 'price')
    show_change_link = True

# Product admin with inline variants
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]

# ProductVariant admin with inline extra images
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    form = ProductVariantAdminForm  # use the custom form here
    inlines = [ProductVariantImageInline]
    fields = (
        'product',
        'image',
        'description',
        'color_name',
        'color_codes',
        'price',
    )
    list_display = ('product', 'color_name', 'price')
    help_texts = {
        'color_codes': (
            'Enter a list of hex colors in JSON format, '
            'e.g. ["#6a0dad", "#000000"]'
        )
    }

# Category admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    prepopulated_fields = {"slug": ("name",)}










