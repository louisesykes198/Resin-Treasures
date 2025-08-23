from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from checkout import views as checkout_views
from accounts.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),      # your main shop app
    path('accounts/', include('accounts.urls')), 
    path('basket/', include('basket.urls')),
    path('wishlist/', include('wishlist.urls')),
    path("newsletter/", include("newsletter.urls")),
    path('checkout/', include('checkout.urls')),
    path("webhooks/stripe/", checkout_views.stripe_webhook, name="stripe-webhook"),
    path('reviews/', include('reviews.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

