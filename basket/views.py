from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, ProductVariant
from django.views.decorators.http import require_POST
from store.models import Basket
from django.contrib.auth.models import User
from django.contrib import messages

def basket_summary(request):
    basket_items = []
    total = 0

    if request.user.is_authenticated:
        # Logged-in users: fetch from database
        basket_qs = Basket.objects.filter(user=request.user)
        for item in basket_qs:
            subtotal = item.variant.price * item.quantity
            total += subtotal
            basket_items.append({
                "key": f"variant_{item.variant.id}",
                "product": item.variant.product,
                "variant": item.variant,
                "quantity": item.quantity,
                "subtotal": subtotal,
            })
    else:
        # Anonymous users: fetch from session
        basket = request.session.get('basket', {})
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
    user = request.user

    if not user.is_authenticated:
        messages.error(request, "You must be logged in to add to basket.")
        return redirect("shop")

    if variant_id:
        variant = ProductVariant.objects.get(id=variant_id)
    else:
        variant = ProductVariant.objects.filter(product_id=product_id).first()

    basket_item, created = Basket.objects.get_or_create(
        user=user,
        variant=variant,
        defaults={'quantity': 1}
    )

    if not created:
        basket_item.quantity += 1
        basket_item.save()

    return redirect("basket_summary")

@require_POST
def remove_one_from_basket(request, product_id):
    variant_id = request.POST.get("variant_id")

    if request.user.is_authenticated:
        if variant_id:
            variant = get_object_or_404(ProductVariant, id=variant_id)
        else:
            variant = get_object_or_404(ProductVariant, product_id=product_id)
        try:
            basket_item = Basket.objects.get(user=request.user, variant=variant)
            if basket_item.quantity > 1:
                basket_item.quantity -= 1
                basket_item.save()
            else:
                basket_item.delete()
        except Basket.DoesNotExist:
            pass
    else:
        basket = request.session.get("basket", {})
        key = f"variant_{variant_id}" if variant_id else f"product_{product_id}"
        if key in basket:
            if basket[key] > 1:
                basket[key] -= 1
            else:
                del basket[key]
        request.session["basket"] = basket
        request.session.modified = True

    return redirect("basket_summary")


@require_POST
def remove_from_basket(request, product_id):
    variant_id = request.POST.get("variant_id")

    if request.user.is_authenticated:
        if variant_id:
            variant = get_object_or_404(ProductVariant, id=variant_id)
        else:
            variant = get_object_or_404(ProductVariant, product_id=product_id)
        Basket.objects.filter(user=request.user, variant=variant).delete()
    else:
        basket = request.session.get("basket", {})
        key = f"variant_{variant_id}" if variant_id else f"product_{product_id}"
        if key in basket:
            del basket[key]
        request.session["basket"] = basket
        request.session.modified = True

    return redirect("basket_summary")


@require_POST
def empty_basket(request):
    if request.user.is_authenticated:
        Basket.objects.filter(user=request.user).delete()
    else:
        request.session['basket'] = {}
        request.session.modified = True
    return redirect('basket_summary')

def basket_view(request):
    basket_items = Basket.objects.filter(user=request.user)

    # Calculate subtotal for each item
    for item in basket_items:
        item.price = item.variant.price if item.variant else item.product.min_price
        item.subtotal = item.price * item.quantity

    # Total for the basket
    total = sum(item.subtotal for item in basket_items)

    return render(request, "basket/basket.html", {
        "basket_items": basket_items,
        "total": total
    })







