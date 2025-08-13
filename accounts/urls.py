from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLogoutView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('my-account/', views.my_account, name='my_account'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('account/settings/', views.account_settings, name='account_settings'),
]

