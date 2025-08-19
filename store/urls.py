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
]
