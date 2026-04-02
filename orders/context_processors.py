def user_orders_count(request):
    cart = request.session.get("cart_items", [])
    count = 0
    for item in cart:
        try:
            count += max(0, int(item.get("quantity", 0)))
        except (TypeError, ValueError):
            continue
    return {"user_orders_count": count}
