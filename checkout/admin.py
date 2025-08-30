from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_variant', 'quantity', 'price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'grand_total', 'status')
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
