from django.shortcuts import render
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
