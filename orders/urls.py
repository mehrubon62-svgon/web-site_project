from django.urls import path
from .views import OrderHistoryView

urlpatterns = [
    path('orders/', OrderHistoryView.as_view(), name='order_history'),
]
