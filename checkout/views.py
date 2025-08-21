import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from store.models import Product  # we need to fetch product info
from .models import Order, OrderItem
from store.models import Product, ProductVariant, Basket
from .forms import OrderForm


stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout_view(request):
    basket_items = Basket.objects.filter(user=request.user)

    if not basket_items.exists():
        return redirect("basket")

    # Calculate subtotal for each item and total
    for item in basket_items:
        item.price = item.variant.price if item.variant else item.product.min_price
        item.subtotal = item.price * item.quantity

    total = sum(item.subtotal for item in basket_items)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        street_address1 = request.POST.get("street_address1")
        street_address2 = request.POST.get("street_address2")
        town_or_city = request.POST.get("town_or_city")
        postcode = request.POST.get("postcode")
        county = request.POST.get("county")
        country = request.POST.get("country")

        # Create the order with updated field names
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            street_address1=street_address1,
            street_address2=street_address2,
            town_or_city=town_or_city,
            postcode=postcode,
            county=county,
            country=country,
            total=total,
        )

        # Create order items and Stripe line items
        line_items = []
        for item in basket_items:
            OrderItem.objects.create(
                order=order,
                product_variant=item.variant if item.variant else None,
                product=item.product if not item.variant else None,
                quantity=item.quantity,
                price=item.price,
            )

            product_name = item.variant.product.name if item.variant else item.product.name
            variant_name = f" - {item.variant.color_name}" if item.variant else ""
            line_items.append({
                "price_data": {
                    "currency": "gbp",
                    "product_data": {"name": f"{product_name}{variant_name}"},
                    "unit_amount": int(item.price * 100),
                },
                "quantity": item.quantity,
            })

        # Create Stripe session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=request.build_absolute_uri("/checkout/success/"),
            cancel_url=request.build_absolute_uri("/checkout/cancel/"),
        )

        order.stripe_payment_intent = session.payment_intent
        order.save()

        # Clear basket
        basket_items.delete()
        
        request.session['order_id'] = order.id

        return redirect(session.url, code=303)

    else:
        order_form = OrderForm()

    return render(request, "checkout/checkout.html", {
        "basket_items": basket_items,
        "total": total,
        "order_form": order_form,
    })

def success_view(request):
    order_id = request.session.get('order_id')
    order = Order.objects.get(id=order_id) if order_id else None

    return render(request, "checkout/success.html", {
        "order": order,
    })

def cancel_view(request):
    return render(request, "checkout/cancel.html")

