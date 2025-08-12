from django.db.models import Prefetch, Min, Q
from django.shortcuts import render, get_object_or_404
from .models import Product, Category, ProductVariant
from .models import Basket
import re
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib import messages
from .forms import ContactForm

def home(request):
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
        'categories': categories,
    })

def about(request):
    return render(request, 'store/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            full_message = f"Message from {name} ({email}):\n\n{message}"

            email_message = EmailMessage(
                subject=f"Contact Form Submission from {name}",
                body=full_message,
                from_email='store@resintreasures.co.uk',  # fake From
                to=['resintreasures5@gmail.com'],  # your sister's email
                headers={'Reply-To': email},  # replies go to customer email
            )
            email_message.send(fail_silently=False)

            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'store/contact.html', {'form': form})

def shop(request):
    sort = request.GET.get('sort', '')
    selected_category_slug = request.GET.get('category', '')
    query = request.GET.get('q', '')
    categories = Category.objects.all()

    products = Product.objects.all()

    # Filter by category
    if selected_category_slug:
        category = get_object_or_404(Category, slug=selected_category_slug)
        products = products.filter(categories=category)
    else:
        category = None

    # Escape regex special chars for safe search
    query = re.escape(query.strip())

    # Filter by search query
    if query:
        products = products.filter(
            Q(name__iregex=rf'\b{query}\b') |
            Q(categories__name__iregex=rf'\b{query}\b') |
            Q(variants__description__iregex=rf'\b{query}\b') |
            Q(variants__color_name__iregex=rf'\b{query}\b')
        ).distinct()

    # Annotate with min_price from variants
    products = products.annotate(min_price=Min('variants__price'))

    # Prefetch variants (keeping your all_variants)
    variants_prefetch = Prefetch(
        'variants',
        queryset=ProductVariant.objects.order_by('id'),
        to_attr='all_variants'
    )
    products = products.prefetch_related(variants_prefetch)

    # Sorting logic
    if sort == 'price_asc':
        products = products.order_by('min_price')
    elif sort == 'price_desc':
        products = products.order_by('-min_price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')

    context = {
        'products': products,
        'categories': categories,
        'sort': sort,
        'selected_category': selected_category_slug,
        'selected_category_obj': category,
        'search_query': query,
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


