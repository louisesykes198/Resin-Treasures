from django.urls import path
from . import views

urlpatterns = [
    path('', views.basket_summary, name='basket_summary'),
    path('add/<int:product_id>/', views.add_to_basket, name='add_to_basket'),
    path('remove/<int:product_id>/', views.remove_from_basket, name='remove_from_basket'),
    path('empty/', views.empty_basket, name='empty_basket'),
]



