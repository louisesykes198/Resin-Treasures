from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from .models import Product, Category, ProductVariant

def home(request):
    return render(request, 'store/home.html')

def about(request):
    return render(request, 'store/about.html')

def contact(request):
    return render(request, 'store/contact.html')

def shop(request):
    sort = request.GET.get('sort', '')
    categories = Category.objects.all()

    # Prefetch variants ordered by id and attach to each product as 'all_variants'
    variants_prefetch = Prefetch(
        'variants',
        queryset=ProductVariant.objects.order_by('id'),
        to_attr='all_variants'
    )
    products = Product.objects.prefetch_related(variants_prefetch)

    # Sort by name easily using queryset ordering
    if sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')

    # Sort by first variant price in Python (since price is on variants)
    elif sort == 'price_asc':
        products = sorted(products, key=lambda p: p.all_variants[0].price if p.all_variants else 0)
    elif sort == 'price_desc':
        products = sorted(products, key=lambda p: p.all_variants[0].price if p.all_variants else 0, reverse=True)

    return render(request, 'store/shop.html', {
        'products': products,
        'categories': categories,
        'sort': sort,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    variants = product.variants.all()
    return render(request, 'store/product_detail.html', {
        'product': product,
        'variants': variants
    })

