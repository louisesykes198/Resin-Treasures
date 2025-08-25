from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('delivery-info/', views.delivery_info, name='delivery_info'),
    path('returns/', views.returns, name='returns'),
    path('help-faqs/', views.help_faqs, name='help_faqs'),
    path('basket/', views.basket_view, name='basket'),
    path('add-to-basket/<int:variant_id>/', views.add_to_basket, name='add_to_basket'),
    path('buy-now/<int:variant_id>/', views.buy_now, name='buy_now'),
]