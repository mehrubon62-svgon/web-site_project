from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from my_site_register.permissions import get_logged_in_user
from .models import Order


class OrderHistoryView(View):
    def get(self, request):
        user = get_logged_in_user(request)
        if not user:
            messages.error(request, "Please log in first.")
            return redirect("login_view")

        orders = Order.objects.filter(user=user).select_related("configuration").order_by("-created_at")
        return render(request, "order_history.html", {"orders": orders})
