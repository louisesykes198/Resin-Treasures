from django.db import models
from django.conf import settings
from store.models import Product  # product still lives in store app

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"Wishlist: {self.user.username} → {self.product.name}"
