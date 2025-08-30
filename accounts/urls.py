from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLogoutView

urlpatterns = [
    path('register/', views.register, name='register'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='accounts/login.html'),
        name='login'
    ),
    path('my-account/', views.my_account, name='my_account'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('account/settings/', views.account_settings, name='account_settings'),
    path('profile/', views.profile, name='profile'),
    path('profile/details/', views.personal_details, name='personal_details'),
    path('profile/orders/', views.order_history, name='order_history'),
    path(
        'profile/orders/<int:order_id>/',
        views.order_detail,
        name='order_detail'
    ),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('add-payment/', views.add_payment_method, name='add_payment_method'),
    path(
        'delete-card/<str:card_id>/',
        views.delete_payment_method,
        name='delete_payment_method'
    ),
    path(
        'set-default-card/<str:card_id>/',
        views.set_default_card,
        name='set_default_card'
    ),
    path('verify/', views.verify_account, name='verify_account'),
]


