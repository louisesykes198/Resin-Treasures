from django.urls import path
from . import views

urlpatterns = [
    path(
        'product/<int:product_id>/review/',
        views.add_review,
        name='add_review'
    ),
    path(
        'my-reviews/',
        views.my_reviews,
        name='my_reviews'
    ),
    path(
        'review/<int:review_id>/edit/',
        views.edit_review,
        name='edit_review'
    ),
    path(
        'review/<int:review_id>/delete/',
        views.delete_review,
        name='delete_review'
    ),
    path(
        'all/',
        views.all_reviews,
        name='all_reviews'
    ),
    path(
        'review/<int:review_id>/respond/',
        views.respond_to_review,
        name='respond_to_review'
    ),
]

