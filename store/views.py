from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from .models import Product, Category, ProductVariant
from .models import Basket
from django.db.models import Q

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
    query = request.GET.get('q', '')
    categories = Category.objects.all()

    products = Product.objects.all()  # ✅ Make sure this is defined early

    # Filter by category
    if selected_category_slug:
        category = get_object_or_404(Category, slug=selected_category_slug)
        products = products.filter(categories=category)
    else:
        category = None

    # Filter by search query
    from django.db.models import Q
    from django.db.models.functions import Lower

    if query:
        products = products.filter(
        Q(name__iregex=rf'\b{query}\b') |
        Q(categories__name__iregex=rf'\b{query}\b') |
        Q(variants__description__iregex=rf'\b{query}\b') |
        Q(variants__color_name__iregex=rf'\b{query}\b')
    ).distinct()

    import re

    query = request.GET.get('q', '')
    query = re.escape(query.strip())


    # Prefetch variants
    variants_prefetch = Prefetch(
        'variants',
        queryset=ProductVariant.objects.order_by('id'),
        to_attr='all_variants'
    )
    products = products.prefetch_related(variants_prefetch)

    # Sorting logic...
    # (keep your existing sorting code here)

    context = {
        'products': products,
        'categories': categories,
        'sort': sort,
        'selected_category': selected_category_slug,
        'selected_category_obj': category,
        'search_query': '',
    }

    return render(request, 'store/shop.html', context)

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

def basket_context(request):
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    else:
        basket = []
    return {'basket': basket}

from django.shortcuts import redirect

def add_to_basket(request, variant_id):
    basket = request.session.get('basket', {})

    # Increment quantity or set to 1
    basket[str(variant_id)] = basket.get(str(variant_id), 0) + 1

    request.session['basket'] = basket
    return redirect('basket_summary')  # or wherever you want to go


