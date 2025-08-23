from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime
from store.models import Order
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from .forms import CustomUserCreationForm
from django.utils.text import slugify
from django.contrib.auth.models import User
import stripe
from django.conf import settings
from .models import Profile
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import CustomLoginForm
import random
from django.core.mail import send_mail
from .utils import generate_unique_username 


stripe.api_key = settings.STRIPE_SECRET_KEY

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            first = form.cleaned_data['first_name']
            last = form.cleaned_data['last_name']
            user.username = generate_unique_username(first, last)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Generate verification code
            code = str(random.randint(100000, 999999))

            # Create profile and store code
            profile = Profile.objects.create(user=user, verification_code=code)

            # Send welcome email with username and verification code
            send_mail(
                'Welcome to Resin Treasures 🌿',
                f"""Hello {user.first_name},

Your account has been created successfully.

🪄 Your login username: {user.username}  
🔐 Your verification code: {code}

Enter this code on the verification page to complete your registration.

Warmly,  
Resin Treasures""",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect('verify_account')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    authentication_form = CustomLoginForm

    def get_success_url(self):
        return reverse_lazy('home')  


def generate_unique_username(first, last):
    base_username = slugify(f"{first}_{last}")
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}_{counter}"
        counter += 1
    return username
    
@login_required
def my_account(request):
    # If you have orders linked to the user:
    orders = Order.objects.filter(user=request.user).order_by('-date')

    context = {
        "full_name": f"{request.user.first_name} {request.user.last_name}".strip(),
        "email": request.user.email,
        "username": request.user.username,
        "date_joined": localtime(request.user.date_joined),
        "orders": orders,
    }
    return render(request, "accounts/my_account.html", context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

class CustomLogoutView(LogoutView):
    next_page = 'home'

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)
    
@login_required
def account_settings(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    cards = []
    if profile.stripe_customer_id:
        sources = stripe.Customer.list_sources(
            profile.stripe_customer_id,
            object="card"
        )
        cards = sources.data

    return render(request, 'accounts/settings.html', {
        "cards": cards,
        "full_name": f"{user.first_name} {user.last_name}".strip(),
        "email": user.email,
        "username": user.username,
        "date_joined": localtime(user.date_joined),
    })

@login_required
def profile(request):
    """
    Display the user's profile page.
    """
    user = request.user
    context = {
        'user': user,
        # Add any other context info you want on the profile page
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def personal_details(request):
    if request.method == 'POST':
        # Get data from form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        # Update user
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        
        messages.success(request, 'Your personal details have been updated.')
        return redirect('personal_details')

    return render(request, 'accounts/personal_details.html')

@login_required
def order_history(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'accounts/order_history.html', {'orders': user_orders})

from django.shortcuts import get_object_or_404

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()  # assuming a related name 'items' for order products
    return render(request, 'accounts/order_detail.html', {
        'order': order,
        'order_items': order_items
    })

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account has been permanently deleted.")
        return redirect('home')  # or a gentle goodbye page


@login_required
def add_payment_method(request):
    user = request.user

    # Ensure profile exists
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        token = request.POST.get('stripeToken')

        # Create Stripe customer if needed
        if not profile.stripe_customer_id:
            customer = stripe.Customer.create(email=user.email)
            profile.stripe_customer_id = customer.id
            profile.save()

        # Attach card to customer
        stripe.Customer.create_source(profile.stripe_customer_id, source=token)

        messages.success(request, "Your card has been saved securely.")
        return redirect('account_settings')

    return render(request, 'accounts/add_payment.html', {
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    })
    
@login_required
def delete_payment_method(request, card_id):
    profile = Profile.objects.get(user=request.user)

    if profile.stripe_customer_id:
        stripe.Customer.delete_source(
            profile.stripe_customer_id,
            card_id
        )
        messages.success(request, "Your card has been removed.")
    return HttpResponseRedirect(reverse('account_settings') + '?tab=payment')

@login_required
def set_default_card(request, card_id):
    profile = Profile.objects.get(user=request.user)

    if profile.stripe_customer_id:
        stripe.Customer.modify(
            profile.stripe_customer_id,
            default_source=card_id
        )
        messages.success(request, "Your default card has been updated.")
            
        return HttpResponseRedirect(reverse('account_settings') + '?tab=payment')

@login_required
def verify_account(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        profile = request.user.profile
        if profile.verification_code == code:
            profile.is_verified = True
            profile.save()
            messages.success(request, "Your account is now verified 🌿")
            return redirect('home')
        else:
            messages.error(request, "Incorrect code. Please try again.")
    return render(request, 'accounts/verify.html')




