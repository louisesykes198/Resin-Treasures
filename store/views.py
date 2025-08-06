from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from .models import Product, Category, ProductVariant


def home(request):
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
        'categories': categories,
    })

def about(request):
    return render(request, 'store/about.html')

def contact(request):
    return render(request, 'store/contact.html')

from django.db.models import Prefetch

from django.shortcuts import get_object_or_404

def shop(request):
    sort = request.GET.get('sort', '')
    selected_category_slug = request.GET.get('category', '')
    categories = Category.objects.all()

    products = Product.objects.all()

    if selected_category_slug:
        category = get_object_or_404(Category, slug=selected_category_slug)
        products = products.filter(categories=category)
    else:
        category = None

    # Prefetch variants
    variants_prefetch = Prefetch(
        'variants',
        queryset=ProductVariant.objects.order_by('id'),
        to_attr='all_variants'
    )
    products = products.prefetch_related(variants_prefetch)

    # Sorting
    if sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')
    elif sort == 'price_asc':
        products = sorted(products, key=lambda p: p.all_variants[0].price if p.all_variants else 0)
    elif sort == 'price_desc':
        products = sorted(products, key=lambda p: p.all_variants[0].price if p.all_variants else 0, reverse=True)

    return render(request, 'store/shop.html', {
        'products': products,
        'categories': categories,
        'sort': sort,
        'selected_category': selected_category_slug,
        'selected_category_obj': category,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    variants = product.variants.all()

    # Process color into a list
    for variant in variants:
        if variant.color_name:
            # Replace " and " with "," and split
            color_str = variant.color_name.lower().replace(' and ', ',')
            variant.color_list = [c.strip() for c in color_str.split(',') if c.strip()]
        else:
            variant.color_list = []

    return render(request, 'store/product_detail.html', {
        'product': product,
        'variants': variants
    })


