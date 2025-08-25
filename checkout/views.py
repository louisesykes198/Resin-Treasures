import stripe
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from store.models import Product, ProductVariant, Basket
from .models import Order, OrderItem
from .forms import OrderForm
from .delivery import DELIVERY_OPTIONS
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string

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
        # Get form data
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        street_address1 = request.POST.get("street_address1")
        street_address2 = request.POST.get("street_address2")
        town_or_city = request.POST.get("town_or_city")
        postcode = request.POST.get("postcode")
        county = request.POST.get("county")
        country = request.POST.get("country")
        delivery_method = request.POST.get("delivery_method")

        # Automatically determine parcel size
        if total < 20:
            parcel_size = "Small"
        elif total < 50:
            parcel_size = "Medium"
        else:
            parcel_size = "Large"

        # Calculate delivery price
        if total >= settings.FREE_DELIVERY_THRESHOLD:
            delivery_price = Decimal("0.00")
        else:
            delivery_price = Decimal(str(DELIVERY_OPTIONS[delivery_method][parcel_size]))

        grand_total = total + delivery_price

        # Create order
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
            delivery_method=delivery_method,
            delivery_size=parcel_size,
            delivery=delivery_price,
            total=total,
            grand_total=grand_total,
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

        # Add delivery as a separate line item
        if delivery_price > 0:
            line_items.append({
                "price_data": {
                    "currency": "gbp",
                    "product_data": {"name": "Delivery"},
                    "unit_amount": int(delivery_price * 100),
                },
                "quantity": 1,
            })

        # ✅ Stripe session creation (correctly indented inside POST)
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=f"https://resin-treasures-2025-f7167892b201.herokuapp.com/checkout/success/?order_id={order.id}",
            cancel_url=f"https://resin-treasures-2025-f7167892b201.herokuapp.com/checkout/cancel/?order_id={order.id}",
            metadata={"order_id": str(order.id)},
        )

        order.stripe_payment_intent = session.payment_intent
        order.save()

        # Clear basket
        basket_items.delete()
        request.session['order_id'] = order.id

        return redirect(session.url, code=303)

    else:
        # GET request — show form and calculate delivery if method is selected
        order_form = OrderForm()
        delivery_method = request.GET.get("delivery_method")

        if delivery_method:
            if total < 20:
                parcel_size = "Small"
            elif total < 50:
                parcel_size = "Medium"
            else:
                parcel_size = "Large"

            if total >= settings.FREE_DELIVERY_THRESHOLD:
                delivery_price = Decimal("0.00")
            else:
                delivery_price = Decimal(str(DELIVERY_OPTIONS[delivery_method][parcel_size]))

            grand_total = total + delivery_price
        else:
            delivery_price = None
            grand_total = total

    return render(request, "checkout/checkout.html", {
        "basket_items": basket_items,
        "total": total,
        "order_form": order_form,
        "free_delivery_threshold": settings.FREE_DELIVERY_THRESHOLD,
        "delivery_price": delivery_price,
        "grand_total": grand_total,
    })


def success_view(request):
    order_id = request.session.get("order_id") or request.GET.get("order_id")

    if not order_id:
        return render(request, "checkout/order_not_found.html", {
            "message": "We couldn't find your order. If you completed a purchase, please check your email or contact support."
        })

    order = Order.objects.filter(id=order_id).first()

    if not order:
        return render(request, "checkout/order_not_found.html", {
            "message": "We couldn’t find your order. It may still be processing. Please check your email or try again shortly."
        })

    context = {
        "order": order,
        "user": order.user,
    }

    request.session.pop("order_id", None)

    return render(request, "checkout/success.html", context)

def cancel_view(request): 
    return render(request, "checkout/cancel.html")

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WH_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print("⚠️ Invalid payload:", e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print("⚠️ Signature verification failed:", e)
        return HttpResponse(status=400)

    print("🔔 Received event:", event["type"])

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        order_id = session.get("metadata", {}).get("order_id")
        print("✅ Checkout session completed for order:", order_id)

        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                print("🛒 Order items in webhook:", order.items.all())
                order.status = "paid"
                order.save()
            except Order.DoesNotExist:
                print("⚠️ Order not found:", order_id)

    return HttpResponse(status=200)

def send_order_confirmation_email(order):
    subject = f"Your Resin Treasures Order #{order.id}"
    message = render_to_string('checkout/order_confirmation_email.html', {
        'order': order,
        'full_name': order.full_name,
    })
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        fail_silently=False,
    )
       
def notify_seller_of_order(order):
    print(f"📦 Seller email sent for order #{order.id}")
    subject = f"New Order Received: #{order.id}"
    message = render_to_string('checkout/seller_notification_email.txt', {
        'order': order,
        'full_name': order.full_name,
        'email': order.email,
        'grand_total': order.grand_total,
    })
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ['resintreasures5@gmail.com'],  # your business email
        fail_silently=False,
    )



