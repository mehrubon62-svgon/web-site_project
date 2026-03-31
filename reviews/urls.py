from django.urls import path
from .views import AddReviewView, AddReviewReplyView, DeleteReviewView, DeleteReviewReplyView

urlpatterns = [
    path('reviews/reply/<int:review_id>/add/', AddReviewReplyView.as_view(), name='add_review_reply'),
    path('reviews/reply/<int:reply_id>/delete/', DeleteReviewReplyView.as_view(), name='delete_review_reply'),
    path('reviews/<str:model_name>/<int:pk>/add/', AddReviewView.as_view(), name='add_review'),
    path('reviews/<int:review_id>/delete/', DeleteReviewView.as_view(), name='delete_review'),
]
