from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

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
    color = models.CharField(max_length=50, blank=True)  # optional
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # new field for price

    def __str__(self):
        return f"{self.product.name} - {self.color or 'Variant'}"







