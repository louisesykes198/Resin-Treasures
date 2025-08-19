from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, ProductVariant
from django.views.decorators.http import require_POST

def basket_summary(request):
    basket = request.session.get('basket', {})
    basket_items = []
    total = 0

    for key, quantity in basket.items():
        if key.startswith("variant_"):
            variant_id = int(key.split("_")[1])
            variant = get_object_or_404(ProductVariant, id=variant_id)
            product = variant.product
            price = variant.price
        else:
            product_id = int(key.split("_")[1])
            product = get_object_or_404(Product, id=product_id)
            variant = None
            price = getattr(product, 'min_price', 0)

        subtotal = price * quantity
        total += subtotal

        basket_items.append({
            "key": key,
            "product": product,
            "variant": variant,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    return render(request, "basket/basket.html", {
        "basket_items": basket_items,
        "total": total,
    })


@require_POST
def add_to_basket(request, product_id):
    variant_id = request.POST.get("variant_id")
    basket = request.session.get("basket", {})

    if variant_id:
        key = f"variant_{variant_id}"
    else:
        key = f"product_{product_id}"

    basket[key] = basket.get(key, 0) + 1
    request.session["basket"] = basket
    return redirect("basket_summary")


@require_POST
def remove_one_from_basket(request, product_id):
    variant_id = request.POST.get("variant_id")
    basket = request.session.get("basket", {})

    if variant_id:
        key = f"variant_{variant_id}"
    else:
        key = f"product_{product_id}"

    if key in basket:
        if basket[key] > 1:
            basket[key] -= 1
        else:
            del basket[key]

    request.session["basket"] = basket
    return redirect("basket_summary")


@require_POST
def remove_from_basket(request, product_id):
    """Remove the item completely, regardless of quantity"""
    variant_id = request.POST.get("variant_id")
    basket = request.session.get("basket", {})

    if variant_id:
        key = f"variant_{variant_id}"
    else:
        key = f"product_{product_id}"

    if key in basket:
        del basket[key]

    request.session["basket"] = basket
    return redirect("basket_summary")


@require_POST
def empty_basket(request):
    request.session['basket'] = {}
    return redirect('basket_summary')




