from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings
from cloudinary.models import CloudinaryField
import json
from django.contrib import admin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


import re
from django.core.exceptions import ValidationError

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    image = CloudinaryField('image')
    description = models.TextField()
    color_name = models.CharField(max_length=50, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    color_codes = models.JSONField(default=list, blank=True, null=True)

    class Meta:
        unique_together = ('product', 'color_name')

    def __str__(self):
        return f"{self.product.name} - {self.color_name or 'No Color'}"

    @property
    def color_list(self):
        """Returns a list of hex colors."""
        return self.color_codes or []

    @property
    def swatch_background(self):
        if isinstance(self.color_codes, list) and self.color_codes:
            if len(self.color_codes) == 1:
                return self.color_codes[0]
            else:
                return f"linear-gradient(to right, {', '.join(self.color_codes)})"
        return '#ffffff'

    def clean(self):
        """Validate that color_codes contains proper hex colors."""
        hex_pattern = re.compile(r'^#(?:[0-9a-fA-F]{3}){1,2}$')
        if self.color_codes:
            if not isinstance(self.color_codes, list):
                raise ValidationError("color_codes must be a list of hex strings.")
            for color in self.color_codes:
                if not isinstance(color, str) or not hex_pattern.match(color.strip()):
                    raise ValidationError(f"Invalid hex color: {color}")

    def save(self, *args, **kwargs):
        self.clean()  # Ensure validation before saving
        super().save(*args, **kwargs)

class ProductVariantImage(models.Model):
    variant = models.ForeignKey(
        'ProductVariant',
        related_name='extra_images',
        on_delete=models.CASCADE
    )
    image = CloudinaryField('image')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.variant} ({self.description})"


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.variant} x {self.quantity}"

    def get_total_price(self):
        return self.variant.price * self.quantity
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_payment_intent = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_method = models.CharField(max_length=50, default='locker')  # or blank=True
    delivery_size = models.CharField(max_length=20, default='Medium')    # or blank=True
    delivery = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('shipped', 'Shipped'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )

    full_name = models.CharField(max_length=200, default='')
    email = models.EmailField(default='')
    house_name_or_number = models.CharField(max_length=100, blank=True)
    street_address1 = models.CharField(max_length=255, default='')  # ← Add this
    street_address2 = models.CharField(max_length=255, blank=True, default='')  # ← Add this
    town_or_city = models.CharField(max_length=100, default='')  # ← Add this
    postcode = models.CharField(max_length=20, default='')
    county = models.CharField(max_length=100, blank=True, default='')  # ← Add this
    country = models.CharField(max_length=100, default='')
    phone_number = models.CharField(max_length=20, default='')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, null=True, blank=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        if self.product_variant:
            return f"{self.product_variant.product.name} ({self.product_variant.color_name}) × {self.quantity}"
        elif self.product:
            return f"{self.product.name} × {self.quantity}"
        else:
            return f"Unknown product × {self.quantity}"

class NumberItem(models.Model):
    value = models.IntegerField()

    def __str__(self):
        return str(self.value)
    









    










