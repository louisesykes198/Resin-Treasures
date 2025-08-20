from .models import Category
from .models import Basket

from .models import Category, Basket

def categories_processor(request):
    return {
        'all_categories': Category.objects.all()
    }

def basket_context(request):
    if request.user.is_authenticated:
        # Logged-in: count from Basket model
        total_quantity = sum(item.quantity for item in Basket.objects.filter(user=request.user))
    else:
        # Anonymous: count from session
        basket = request.session.get('basket', {})
        total_quantity = sum(basket.values())

    return {'basket_quantity': total_quantity}



