from .models import Order


def user_orders_count(request):
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        return {'user_orders_count': Order.objects.filter(user=user).count()}
    return {'user_orders_count': 0}
