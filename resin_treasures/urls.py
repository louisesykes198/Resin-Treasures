from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),      # your main shop app
    path('accounts/', include('accounts.urls')), 
    path('basket/', include('basket.urls')),
    path('wishlist/', include('wishlist.urls')),
]

