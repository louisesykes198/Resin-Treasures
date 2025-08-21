from django.db.models import Prefetch, Min, Q
from django.shortcuts import redirect, render, get_object_or_404
from .models import Product, Category, ProductVariant
from .models import Basket
import re
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib import messages
from .forms import ContactForm
from django.contrib.auth.decorators import login_required
from django.conf import settings


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

    # Escape regex special chars
    query = re.escape(query.strip())

    # Filter by search query
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(categories__name__icontains=query) |
            Q(variants__description__icontains=query) |
            Q(variants__color_name__icontains=query)
        )

    # Prefetch variants + add min_price
    products = products.prefetch_related(
        Prefetch('variants', queryset=ProductVariant.objects.order_by('id'), to_attr='all_variants')
    ).annotate(min_price=Min('variants__price')).distinct()

    # --- Sorting ---
    if sort == 'price_asc':
        products = products.order_by('min_price')
    elif sort == 'price_desc':
        products = products.order_by('-min_price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')

    return render(request, 'store/shop.html', {
        'products': products,
        'categories': categories,
        'selected_category': category,
        'sort': sort,
    })

from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render
from .models import Product, ProductVariant, ProductVariantImage


def product_detail(request, pk):
    variants_prefetch = Prefetch(
        'variants',
        queryset=ProductVariant.objects.prefetch_related(
            Prefetch('extra_images', queryset=ProductVariantImage.objects.all(), to_attr='all_images')
        ),
        to_attr='all_variants'
    )

    product = Product.objects.prefetch_related(variants_prefetch).get(pk=pk)
    variants = product.all_variants

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

def add_to_basket(request, variant_id):
    basket = request.session.get('basket', {})

    # Increment quantity or set to 1
    basket[str(variant_id)] = basket.get(str(variant_id), 0) + 1

    request.session['basket'] = basket
    return redirect('basket_summary')  # or wherever you want to go

@login_required
def basket_view(request):
    basket_items = Basket.objects.filter(user=request.user)  # get from DB

    total = sum(item.get_total_price() for item in basket_items)

    return render(request, "basket/basket.html", {
        "basket_items": basket_items,
        "total": total,
        "free_delivery_threshold": settings.FREE_DELIVERY_THRESHOLD,
})

def delivery_info(request):
    return render(request, 'store/delivery_info.html')

def returns(request):
    return render(request, 'store/returns.html')

def help_faqs(request):
    return render(request, 'store/help_faqs.html')