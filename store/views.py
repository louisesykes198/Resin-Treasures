from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def home(request):
    return render(request, 'store/home.html')

def about(request):
    return render(request, 'store/about.html')

def contact(request):
    return render(request, 'store/contact.html')

def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'store/shop.html', {'products': products, 'categories': categories})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    variants = product.variants.all()  # if you're using ProductVariant
    return render(request, 'store/product_detail.html', {
        'product': product,
        'variants': variants
    })