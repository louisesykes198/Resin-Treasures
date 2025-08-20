from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout_view, name='checkout'),
    path('success/', views.success_view, name='checkout_success'),
    path('cancel/', views.cancel_view, name='checkout_cancel'),
]
