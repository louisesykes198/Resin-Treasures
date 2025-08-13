from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime
from store.models import Order

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # change 'home' to your homepage name
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')
    
@login_required
def my_account(request):
    return render(request, 'accounts/my_account.html')

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