from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from django.views.decorators.http import require_POST

def basket_summary(request):
    basket = request.session.get('basket', {})
    basket_items = []
    total = 0

    for item_id, quantity in basket.items():
        product = get_object_or_404(Product, id=item_id)
        variant = product.variants.first()  # Adjust if needed
        price = variant.price if variant else 0
        subtotal = price * quantity
        total += subtotal

        basket_items.append({
            'product': product,
            'variant': variant,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'basket/basket.html', {
        'basket_items': basket_items,
        'total': total
    })

@require_POST
def add_to_basket(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    basket = request.session.get('basket', {})

    basket[str(product_id)] = basket.get(str(product_id), 0) + 1

    request.session['basket'] = basket

    return redirect('basket_summary')

@require_POST
def remove_from_basket(request, product_id):
    basket = request.session.get('basket', {})

    if str(product_id) in basket:
        # Option 1: reduce quantity by 1
        if basket[str(product_id)] > 1:
            basket[str(product_id)] -= 1
        else:
            # Option 2: remove entirely if quantity is 1
            del basket[str(product_id)]
        request.session['basket'] = basket

    return redirect('basket_summary')

@require_POST
def empty_basket(request):
    request.session['basket'] = {}
    return redirect('basket_summary')



