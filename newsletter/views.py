from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
from .forms import SubscribeForm

def subscribe(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)

        if form.is_valid():
            subscriber = form.save()

            # send confirmation email
            send_mail(
                subject="Welcome to Resin Treasures!",
                message=(
                    "Hi there!\n\n"
                    "Thanks for subscribing to Resin Treasures. "
                    "You’ll now be the first to hear about our latest creations, offers, and updates.\n\n"
                    "— Resin Treasures Team"
                ),
                from_email=None,
                recipient_list=[subscriber.email],
                fail_silently=False,
            )

            messages.success(request, "Thank you for subscribing! A confirmation email has been sent.")

        else:
            if 'email' in form.errors and any("already exists" in e for e in form.errors['email']):
                messages.info(request, "You’re already subscribed to Resin Treasures.")
            else:
                messages.error(request, "There was a problem with your subscription. Please try again.")

        return redirect("/")

    return redirect("/")





