from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.utils.text import slugify


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


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='variants/')
    description = models.TextField()
    color_name = models.CharField(max_length=50, blank=True)
    color_code = models.CharField(max_length=7, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Thumbnail
    thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(250, 250)],
        format='JPG',
        options={'quality': 85}
    )

    def __str__(self):
        return f"{self.product.name} - {self.color_name or 'Variant'}"









