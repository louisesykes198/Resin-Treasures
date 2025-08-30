from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from store.models import Product
from django.views.decorators.http import require_POST


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(
                request,
                "Your review has been submitted."
            )
            return redirect('product_detail', pk=product.id)
    else:
        form = ReviewForm()

    return render(
        request,
        'reviews/add_review.html',
        {'form': form, 'product': product}
    )


@login_required
def my_reviews(request):
    reviews = Review.objects.filter(user=request.user).select_related(
        'product'
    )
    return render(
        request,
        'reviews/my_reviews.html',
        {'reviews': reviews}
    )


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(
        Review, id=review_id, user=request.user
    )
    form = ReviewForm(request.POST or None, instance=review)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(
            request,
            "Your review has been updated."
        )
        return redirect('my_reviews')
    return render(
        request,
        'reviews/edit_review.html',
        {'form': form, 'review': review}
    )


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(
        Review, id=review_id, user=request.user
    )
    if request.method == 'POST':
        review.delete()
        messages.success(
            request,
            "Your review has been deleted."
        )
        return redirect('my_reviews')


def all_reviews(request):
    reviews = Review.objects.select_related(
        'product', 'user'
    ).order_by('-created_at')

    product_id = request.GET.get('product')
    rating = request.GET.get('rating')

    if product_id:
        reviews = reviews.filter(product__id=product_id)
    if rating:
        reviews = reviews.filter(rating=rating)

    products = Product.objects.all()
    return render(
        request,
        'reviews/all_reviews.html',
        {
            'reviews': reviews,
            'products': products,
            'selected_product': product_id,
            'selected_rating': rating,
        }
    )


@login_required
@require_POST
def respond_to_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user.is_staff:
        response = request.POST.get('creator_response')
        review.creator_response = response
        review.save()
        messages.success(
            request,
            "Your response has been added."
        )
    return redirect('all_reviews')


