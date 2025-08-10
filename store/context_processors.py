from .models import Category
from .models import Basket

def categories_processor(request):
    return {
        'all_categories': Category.objects.all()
    }

def basket_context(request):
    basket = request.session.get('basket', {})
    total_quantity = sum(basket.values())
    return {'basket_quantity': total_quantity}


