from django.shortcuts import render, get_object_or_404 , redirect
from django.views import View
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.templatetags.static import static
from .models import *
from .filters import *
from my_site_register.permissions import get_logged_in_user 
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.db.utils import ProgrammingError, OperationalError
from django.utils.translation import gettext as _
import random
from collections import defaultdict
from urllib.parse import urlsplit, unquote
from reviews.models import Review

SESSION_CART_KEY = "cart_items"
SESSION_PROMO_KEY = "cart_promo_code"
PRODUCT_MODEL_MAP = {
    "processor": Processor,
    "gpu": GPU,
    "ram": RAM,
    "motherboard": Motherboard,
    "storage": Storage,
    "powersupply": PowerSupply,
    "case": Case,
    "cooler": Cooler,
    "laptop": Laptop,
}

CATEGORY_DISPLAY_MAP = {
    "cooler": "Cooler",
}


def _parse_cart_item_id(item_id):
    model_name, _, pk_raw = (item_id or "").partition("-")
    if not model_name or not pk_raw:
        return None, None
    try:
        return model_name, int(pk_raw)
    except ValueError:
        return None, None


def _get_stock_for_cart_item(item_id):
    model_name, pk = _parse_cart_item_id(item_id)
    model_cls = PRODUCT_MODEL_MAP.get(model_name)
    if not model_cls or pk is None:
        return None
    product = model_cls.objects.filter(pk=pk).only("stock").first()
    if not product:
        return None
    return max(0, int(getattr(product, "stock", 0)))


def _add_to_session_cart(request, item):
    cart = request.session.get(SESSION_CART_KEY, [])
    quantity_to_add = max(1, int(item.get("quantity", 1)))
    stock_limit = item.get("stock")
    if stock_limit is not None:
        stock_limit = max(0, int(stock_limit))
    for existing in cart:
        if existing["id"] == item["id"]:
            next_qty = int(existing.get("quantity", 1)) + quantity_to_add
            existing["quantity"] = min(next_qty, stock_limit) if stock_limit is not None else next_qty
            if stock_limit is not None:
                existing["stock"] = stock_limit
            request.session[SESSION_CART_KEY] = cart
            return
    final_qty = min(quantity_to_add, stock_limit) if stock_limit is not None else quantity_to_add
    cart.append({**item, "quantity": final_qty})
    request.session[SESSION_CART_KEY] = cart


def _get_session_cart(request):
    return request.session.get(SESSION_CART_KEY, [])


def _save_session_cart(request, cart):
    request.session[SESSION_CART_KEY] = cart


def _compute_cart_totals(cart, promo_obj=None):
    subtotal = sum(float(item.get("price", 0)) * int(item.get("quantity", 1)) for item in cart)
    shipping = 0 if subtotal > 120 else 10
    tax = subtotal * 0.01
    discount_percent = promo_obj.discount_percent if promo_obj else 0
    discount = subtotal * (discount_percent / 100) if discount_percent else 0
    total = subtotal + shipping + tax - discount
    return {
        "subtotal": subtotal,
        "shipping": shipping,
        "tax": tax,
        "discount": discount,
        "discount_percent": discount_percent,
        "total": total,
        "items_count": sum(int(item.get("quantity", 1)) for item in cart),
    }


def _build_cart_view_state(request):
    raw_items = _get_session_cart(request)
    cart_items = []
    for item in raw_items:
        price = float(item.get("price", 0))
        resolved_stock = _get_stock_for_cart_item(item.get("id", ""))
        stock_limit = resolved_stock if resolved_stock is not None else int(item.get("stock", 0) or 0)
        quantity = int(item.get("quantity", 1))
        if stock_limit > 0:
            quantity = min(quantity, stock_limit)
        cart_items.append(
            {
                **item,
                "price": price,
                "stock": stock_limit,
                "quantity": quantity,
                "line_total": price * quantity,
                "can_increase": True if resolved_stock is None and stock_limit == 0 else (quantity < stock_limit),
            }
        )

    promo_code = request.session.get(SESSION_PROMO_KEY, "").upper()
    try:
        if promo_code == "BUILDBOX10":
            PromoCode.objects.get_or_create(
                code="BUILDBOX10",
                defaults={"quantity": 500, "discount_percent": 5, "is_active": True},
            )
        promo_obj = PromoCode.objects.filter(code=promo_code, is_active=True).first() if promo_code else None
    except (ProgrammingError, OperationalError):
        promo_obj = None

    totals = _compute_cart_totals(cart_items, promo_obj)
    free_shipping_delta = max(0, 120 - totals["subtotal"])
    return {
        "cart_items": cart_items,
        "promo_code": promo_code if promo_obj else "",
        "promo_applied": bool(promo_obj),
        "free_shipping_delta": free_shipping_delta,
        **totals,
    }


def _get_reviews_context(product, current_user):
    content_type = ContentType.objects.get_for_model(product.__class__)
    reviews = (
        Review.objects.filter(content_type=content_type, object_id=product.pk, is_approved=True)
        .select_related("user")
        .prefetch_related("replies__user")
        .order_by("-created_at")
    )

    review_count = reviews.count()
    avg_rating = 0
    if review_count:
        total_rating = sum(r.rating for r in reviews)
        avg_rating = round(total_rating / review_count, 1)

    user_review = None
    if current_user:
        user_review = reviews.filter(user=current_user).first()

    return {
        "reviews": reviews,
        "review_count": review_count,
        "avg_rating": avg_rating,
        "user_review": user_review,
    }


def _detail_url_for_product(product):
    name_map = {
        "processor": "processor_detail",
        "gpu": "gpu_detail",
        "ram": "ram_detail",
        "motherboard": "motherboard_detail",
        "storage": "storage_detail",
        "powersupply": "power_supply_detail",
        "case": "case_detail",
        "cooler": "cooler_detail",
        "laptop": "laptop_detail",
    }
    route_name = name_map.get(product._meta.model_name)
    if not route_name:
        return "#"
    return reverse(route_name, kwargs={"pk": product.pk})


def _product_category_label(product):
    return CATEGORY_DISPLAY_MAP.get(product._meta.model_name, product._meta.model_name.replace("_", " ").title())


def _safe_main_image_url(product):
    try:
        return product.image.url if getattr(product, "image", None) else ""
    except ValueError:
        return ""


def _collect_extra_images_by_object_ids(model_class, object_ids):
    if not object_ids:
        return {}
    content_type = ContentType.objects.get_for_model(model_class)
    extras = defaultdict(list)
    rows = ProductImage.objects.filter(
        content_type=content_type,
        object_id__in=object_ids,
    ).order_by("object_id", "order", "id")
    for row in rows:
        if not getattr(row, "image", None):
            continue
        try:
            url = row.image.url
        except ValueError:
            continue
        if url:
            extras[row.object_id].append(url)
    return extras


def _build_card_images(main_url, extra_urls):
    def canonical_key(url):
        if not url:
            return ""
        parsed = urlsplit(url)
        return unquote(parsed.path).strip().lower()

    images = []
    seen = set()
    if main_url:
        images.append(main_url)
        seen.add(canonical_key(main_url))
    for url in extra_urls or []:
        key = canonical_key(url)
        if url and key and key not in seen:
            images.append(url)
            seen.add(key)
    return images


def _get_additional_images_for_product(product):
    content_type = ContentType.objects.get_for_model(product.__class__)
    rows = ProductImage.objects.filter(content_type=content_type, object_id=product.pk).order_by("order", "id")
    main_url = _safe_main_image_url(product)
    main_key = unquote(urlsplit(main_url).path).strip().lower() if main_url else ""
    unique = []
    seen = set()
    if main_key:
        seen.add(main_key)
    for row in rows:
        if not getattr(row, "image", None):
            continue
        try:
            url = row.image.url
        except ValueError:
            continue
        key = unquote(urlsplit(url).path).strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        unique.append(row)
    return unique


def _attach_card_images_to_page(page_obj, model_class):
    objs = list(page_obj.object_list)
    obj_ids = [obj.pk for obj in objs]
    extras = _collect_extra_images_by_object_ids(model_class, obj_ids)
    for obj in objs:
        main_url = _safe_main_image_url(obj)
        obj.card_images = _build_card_images(main_url, extras.get(obj.pk, []))


class Home(View):
    def get(self, request, *args, **kwargs):
        pools = [
            list(Processor.objects.all()[:2]),
            list(GPU.objects.all()[:2]),
            list(Motherboard.objects.all()[:2]),
            list(RAM.objects.all()[:2]),
            list(Storage.objects.all()[:2]),
            list(PowerSupply.objects.all()[:2]),
            list(Case.objects.all()[:2]),
            list(Cooler.objects.all()[:2]),
        ]
        cards = []
        products_for_gallery = defaultdict(set)
        for bucket in pools:
            for product in bucket:
                image = _safe_main_image_url(product)
                model_name = product._meta.model_name
                products_for_gallery[model_name].add(product.pk)
                cards.append(
                    {
                        "name": getattr(product, "name", "Product"),
                        "price": getattr(product, "price", 0),
                        "image": image,
                        "product_id": product.pk,
                        "model_name": model_name,
                        "category": _product_category_label(product),
                        "detail_url": _detail_url_for_product(product),
                    }
                )
        gallery_map = {}
        for model_name, pks in products_for_gallery.items():
            model_cls = PRODUCT_MODEL_MAP.get(model_name)
            if not model_cls:
                continue
            extras = _collect_extra_images_by_object_ids(model_cls, list(pks))
            for pk, urls in extras.items():
                gallery_map[(model_name, pk)] = urls
        for card in cards:
            key = (card.get("model_name"), card.get("product_id"))
            card["card_images"] = _build_card_images(card.get("image", ""), gallery_map.get(key, []))
        random.shuffle(cards)
        hero_images = list(HomeHeroImage.objects.filter(is_active=True).order_by("order", "-created_at"))
        fallback_hero_url = "https://images.unsplash.com/photo-1717283413190-d4551453b92a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080"
        hero_image_urls = [img.image.url for img in hero_images if getattr(img, "image", None)]
        if not hero_image_urls:
            hero_image_urls = [fallback_hero_url]
        return render(
            request,
            'home.html',
            {
                "popular_components": cards[:4],
                "hero_image_urls": hero_image_urls,
                "hero_image_initial": hero_image_urls[0],
            },
        )


class AboutUsView(View):
    def get(self, request):
        gallery_images = []
        hero_images = list(HomeHeroImage.objects.filter(is_active=True).order_by("order", "-created_at"))
        for hero in hero_images:
            if getattr(hero, "image", None):
                gallery_images.append(hero.image.url)

        fallback_gallery = [
            "/media/home_hero/28d7079a65186eb90873ede6ddda9715.jpg",
            "/media/home_hero/2bc97ccd8f79571592dc05e408386ba1.jpg",
            "/media/home_hero/441b7509d792cba6bcc8f150270856be.jpg",
            "/media/home_hero/dad43e9f0ea2d832ecc332bfc9cad4a5.jpg",
            "/media/processors/processor_55.jpg",
            "/media/gpus/0783077cf860895ce4d2d105c675df02a8e49ca2e3787a2c2cba6899ee131331.jpg.webp",
        ]
        for image_url in fallback_gallery:
            if image_url not in gallery_images:
                gallery_images.append(image_url)

        stats = [
            {"value": 12000, "suffix": "+", "label": "builders launched with BuildBox"},
            {"value": 980, "suffix": "", "label": "configurations checked every hour"},
            {"value": 42, "suffix": "ms", "label": "average compatibility signal time"},
            {"value": 24, "suffix": "/7", "label": "support rhythm for urgent questions"},
        ]
        principles = [
            {
                "eyebrow": "Precision",
                "title": "Every recommendation has to survive reality.",
                "copy": "We treat component compatibility like an engineering problem, not a guess. Power, fit, thermals, sockets, and upgrade paths are part of the same conversation.",
            },
            {
                "eyebrow": "Clarity",
                "title": "Complex builds should still feel obvious.",
                "copy": "The best tools remove anxiety. We design flows that turn a thousand tiny decisions into a system you can trust in minutes.",
            },
            {
                "eyebrow": "Momentum",
                "title": "A great setup should feel inevitable, not intimidating.",
                "copy": "BuildBox is meant to keep people moving, from first idea to final checkout, without forcing them to become hardware experts overnight.",
            },
        ]
        chapters = [
            {
                "index": "01",
                "title": "Signal Before Specs",
                "copy": "We start with what the machine needs to do, then shape the hardware around that goal. Performance only matters when it is attached to purpose.",
            },
            {
                "index": "02",
                "title": "Compatibility as Confidence",
                "copy": "The configurator is not a gimmick. It is the moment where uncertainty drops and the build starts to feel real.",
            },
            {
                "index": "03",
                "title": "A Store That Feels Like a Studio",
                "copy": "Catalog, guidance, and storytelling should feel like one continuous experience, not a pile of disconnected product pages.",
            },
        ]
        workflow = [
            {
                "step": "Frame",
                "title": "We frame the mission first.",
                "copy": "Gaming, editing, streaming, workstations, compact desks, silent builds. Every system starts with context.",
            },
            {
                "step": "Shape",
                "title": "We shape a system, not a shopping list.",
                "copy": "The right board changes the right PSU. The right case changes cooling. We design around relationships, not isolated parts.",
            },
            {
                "step": "Refine",
                "title": "We refine until the build feels intentional.",
                "copy": "A finished BuildBox setup should look coherent, perform hard, and still leave room for the next upgrade.",
            },
        ]
        return render(
            request,
            "about_us.html",
            {
                "stats": stats,
                "principles": principles,
                "chapters": chapters,
                "workflow": workflow,
                "about_reel_src": static("about/buildbox-reel.webp"),
                "about_gallery_images": gallery_images[:6],
            },
        )


class ShoppingCartView(View):
    def get(self, request):
        state = _build_cart_view_state(request)
        return render(
            request,
            "shopping_cart.html",
            state,
        )

    def post(self, request):
        action = request.POST.get("action", "")
        item_id = request.POST.get("item_id", "")
        entered_code = request.POST.get("promo_code", "").strip().upper()
        cart_items = _get_session_cart(request)
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

        if action == "increase" and item_id:
            for item in cart_items:
                if item.get("id") == item_id:
                    current_qty = int(item.get("quantity", 1))
                    stock_limit = _get_stock_for_cart_item(item_id)
                    if stock_limit is not None and current_qty >= stock_limit:
                        messages.error(request, _("Maximum stock reached for this item."))
                        break
                    item["quantity"] = current_qty + 1
                    break
            _save_session_cart(request, cart_items)

        elif action == "decrease" and item_id:
            updated = []
            for item in cart_items:
                if item.get("id") != item_id:
                    updated.append(item)
                    continue
                current_qty = int(item.get("quantity", 1))
                if current_qty > 1:
                    item["quantity"] = current_qty - 1
                    updated.append(item)
            _save_session_cart(request, updated)

        elif action == "remove" and item_id:
            updated = [item for item in cart_items if item.get("id") != item_id]
            _save_session_cart(request, updated)

        elif action == "clear":
            _save_session_cart(request, [])
            request.session.pop(SESSION_PROMO_KEY, None)

        elif action == "apply_promo":
            try:
                if entered_code == "BUILDBOX10":
                    PromoCode.objects.get_or_create(
                        code="BUILDBOX10",
                        defaults={"quantity": 500, "discount_percent": 5, "is_active": True},
                    )
                promo_obj = PromoCode.objects.filter(code=entered_code, is_active=True).first()
                if not promo_obj:
                    request.session.pop(SESSION_PROMO_KEY, None)
                    messages.error(request, _("Invalid promo code."))
                    return redirect("shopping_cart")

                user = get_logged_in_user(request)
                with transaction.atomic():
                    promo_obj = PromoCode.objects.select_for_update().get(pk=promo_obj.pk)
                    if promo_obj.remaining_quantity <= 0:
                        messages.error(request, _("This promo code has reached its usage limit."))
                        return redirect("shopping_cart")

                    if user:
                        if PromoCodeUsage.objects.filter(promo_code=promo_obj, user=user).exists():
                            messages.error(request, _("You already used this promo code."))
                            return redirect("shopping_cart")
                        PromoCodeUsage.objects.create(promo_code=promo_obj, user=user)
                    else:
                        anon_used = request.session.get("used_promo_codes", [])
                        if promo_obj.code in anon_used:
                            messages.error(request, _("You already used this promo code."))
                            return redirect("shopping_cart")
                        anon_used.append(promo_obj.code)
                        request.session["used_promo_codes"] = anon_used

                request.session[SESSION_PROMO_KEY] = promo_obj.code
                messages.success(
                    request,
                    _("Promo code applied: %(discount)s%% discount.") % {"discount": promo_obj.discount_percent},
                )
            except (ProgrammingError, OperationalError):
                messages.error(request, _("Promo codes are unavailable until migrations are applied."))

        if is_ajax and action in {"increase", "decrease", "remove", "clear"}:
            state = _build_cart_view_state(request)
            return JsonResponse(
                {
                    "ok": True,
                    "action": action,
                    "cart_empty": len(state["cart_items"]) == 0,
                    "items": [
                        {
                            "id": item["id"],
                            "quantity": item["quantity"],
                            "stock": item.get("stock", 0),
                            "line_total": round(float(item["line_total"]), 2),
                            "can_increase": bool(item.get("can_increase", False)),
                        }
                        for item in state["cart_items"]
                    ],
                    "totals": {
                        "subtotal": round(float(state["subtotal"]), 2),
                        "shipping": round(float(state["shipping"]), 2),
                        "tax": round(float(state["tax"]), 2),
                        "discount": round(float(state["discount"]), 2),
                        "discount_percent": int(state["discount_percent"]),
                        "total": round(float(state["total"]), 2),
                        "items_count": int(state["items_count"]),
                        "promo_applied": bool(state["promo_applied"]),
                        "promo_code": state["promo_code"],
                        "free_shipping_delta": round(float(state["free_shipping_delta"]), 2),
                    },
                }
            )

        return redirect("shopping_cart")


class CheckoutView(View):
    def get(self, request):
        user = get_logged_in_user(request)
        if not user:
            messages.error(request, _("Please log in first."))
            return redirect("login_view")

        raw_items = _get_session_cart(request)
        if not raw_items:
            messages.info(request, _("Your cart is empty."))
            return redirect("shopping_cart")

        cart_items = []
        for item in raw_items:
            price = float(item.get("price", 0))
            quantity = int(item.get("quantity", 1))
            cart_items.append({**item, "price": price, "quantity": quantity, "line_total": price * quantity})

        totals = _compute_cart_totals(cart_items, None)
        saved_address = None
        if user:
            saved = UserSavedAddress.objects.filter(user=user).first()
            if saved:
                saved_address = {
                    "full_name": saved.full_name,
                    "email": saved.email,
                    "phone": saved.phone,
                    "address1": saved.address1,
                    "address2": saved.address2,
                    "city": saved.city,
                    "region": saved.region,
                    "zip_code": saved.zip_code,
                    "country": saved.country,
                }

        return render(
            request,
            "checkout.html",
            {
                "cart_items": cart_items,
                "saved_address": saved_address,
                **totals,
            },
        )

    def post(self, request):
        user = get_logged_in_user(request)
        if not user:
            messages.error(request, _("Please log in first."))
            return redirect("login_view")

        action = request.POST.get("action", "")
        if action == "place_order":
            save_address = request.POST.get("save_address") == "1"
            raw_items = _get_session_cart(request)
            totals = _compute_cart_totals(raw_items, None)

            from orders.models import Order

            address = ", ".join(
                filter(
                    None,
                    [
                        request.POST.get("address1", "").strip(),
                        request.POST.get("address2", "").strip(),
                        request.POST.get("city", "").strip(),
                        request.POST.get("zip", "").strip(),
                        request.POST.get("country", "").strip() or "Tajikistan",
                    ],
                )
            )

            Order.objects.create(
                user=user,
                status="PENDING",
                total_price=totals["total"],
                full_name=request.POST.get("full_name", "").strip() or user.username,
                phone=request.POST.get("phone", "").strip() or "-",
                email=request.POST.get("email", "").strip() or user.email or "no-email@example.com",
                address=address or "Tajikistan",
                comment=request.POST.get("order_note", "").strip(),
            )

            if user and save_address:
                UserSavedAddress.objects.update_or_create(
                    user=user,
                    defaults={
                        "full_name": request.POST.get("full_name", "").strip(),
                        "email": request.POST.get("email", "").strip(),
                        "phone": request.POST.get("phone", "").strip(),
                        "address1": request.POST.get("address1", "").strip(),
                        "address2": request.POST.get("address2", "").strip(),
                        "city": request.POST.get("city", "").strip(),
                        "region": request.POST.get("region", "").strip(),
                        "zip_code": request.POST.get("zip", "").strip(),
                        "country": request.POST.get("country", "Tajikistan").strip() or "Tajikistan",
                    },
                )
            _save_session_cart(request, [])
            request.session.pop(SESSION_PROMO_KEY, None)
            messages.success(request, _("Order placed successfully."))
            return redirect("home")
        return redirect("checkout")


class AddCatalogItemToCartView(View):
    model_map = PRODUCT_MODEL_MAP

    def post(self, request, model_name, pk):
        model_class = self.model_map.get(model_name)
        if not model_class:
            messages.error(request, _("Unsupported product type."))
            return redirect(request.META.get("HTTP_REFERER", "home"))

        product = get_object_or_404(model_class, pk=pk)
        image = ""
        try:
            image = product.image.url if getattr(product, "image", None) else ""
        except ValueError:
            image = ""

        try:
            quantity = int(request.POST.get("quantity", "1"))
        except ValueError:
            quantity = 1
        quantity = max(1, quantity)
        stock_limit = max(0, int(getattr(product, "stock", 0)))
        if stock_limit > 0:
            quantity = min(quantity, stock_limit)
        else:
            messages.error(request, _("This product is out of stock."))
            return redirect(request.META.get("HTTP_REFERER", "home"))

        _add_to_session_cart(
            request,
            {
                "id": f"{model_name}-{product.pk}",
                "name": getattr(product, "name", "Product"),
                "price": float(getattr(product, "price", 0)),
                "image": image,
                "category": model_name.replace("_", " ").title(),
                "quantity": quantity,
                "stock": stock_limit,
            },
        )
        messages.success(request, _("Added to cart!"))
        return redirect(request.META.get("HTTP_REFERER", "home"))


class ProcessorListView(View):
    def get(self, request):
        processors = Processor.objects.all()
        processor_filter = ProcessorFilter(request.GET, queryset=processors)
        
        paginator = Paginator(processor_filter.qs, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        _attach_card_images_to_page(page_obj, Processor)
        
        # Get user's wishlist items
        user_wishlist = []
        user = get_logged_in_user(request)
        if user:
            content_type = ContentType.objects.get_for_model(Processor)
            user_wishlist = list(Wishlist.objects.filter(
                user=user,
                content_type=content_type
            ).values_list('object_id', flat=True))
        
        context = {
            'filter': processor_filter,
            'page_obj': page_obj,
            'category': 'Processors',
            'category_slug': 'processors',
            'user_wishlist': user_wishlist
        }
        return render(request, 'catalog/processors.html', context)


class GPUListView(View):
    def get(self, request):
        gpus = GPU.objects.all()
        gpu_filter = GPUFilter(request.GET, queryset=gpus)
        
        paginator = Paginator(gpu_filter.qs, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        _attach_card_images_to_page(page_obj, GPU)
        
        # Get user's wishlist items
        user_wishlist = []
        user = get_logged_in_user(request)
        if user:
            content_type = ContentType.objects.get_for_model(GPU)
            user_wishlist = list(Wishlist.objects.filter(
                user=user,
                content_type=content_type
            ).values_list('object_id', flat=True))
        
        context = {
            'filter': gpu_filter,
            'page_obj': page_obj,
            'category': 'Graphics Cards',
            'category_slug': 'gpus',
            'user_wishlist': user_wishlist
        }
        return render(request, 'catalog/gpus.html', context)


class RAMListView(View):
    def get(self, request):
        ram = RAM.objects.all()
        ram_filter = RAMFilter(request.GET, queryset=ram)
        
        paginator = Paginator(ram_filter.qs, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        _attach_card_images_to_page(page_obj, RAM)
        
        # Get user's wishlist items
        user_wishlist = []
        user = get_logged_in_user(request)
        if user:
            content_type = ContentType.objects.get_for_model(RAM)
            user_wishlist = list(Wishlist.objects.filter(
                user=user,
                content_type=content_type
            ).values_list('object_id', flat=True))
        
        context = {
            'filter': ram_filter,
            'page_obj': page_obj,
            'category': 'RAM',
            'category_slug': 'ram',
            'user_wishlist': user_wishlist
        }
        return render(request, 'catalog/ram.html', context)


class MotherboardListView(View):
    def get(self, request):
        motherboards = Motherboard.objects.all()
        motherboard_filter = MotherboardFilter(request.GET, queryset=motherboards)
        
        paginator = Paginator(motherboard_filter.qs, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        _attach_card_images_to_page(page_obj, Motherboard)
        
        # Get user's wishlist items
        user_wishlist = []
        user = get_logged_in_user(request)
        if user:
            content_type = ContentType.objects.get_for_model(Motherboard)
            user_wishlist = list(Wishlist.objects.filter(
                user=user,
                content_type=content_type
            ).values_list('object_id', flat=True))
        
        context = {
            'filter': motherboard_filter,
            'page_obj': page_obj,
            'category': 'Motherboards',
            'category_slug': 'motherboards',
            'user_wishlist': user_wishlist
        }
        return render(request, 'catalog/motherboards.html', context)


class StorageListView(View):
    def get(self, request):
        storage = Storage.objects.all()
        storage_filter = StorageFilter(request.GET, queryset=storage)
        
        paginator = Paginator(storage_filter.qs, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        _attach_card_images_to_page(page_obj, Storage)
        
        # Get user's wishlist items
        user_wishlist = []
        user = get_logged_in_user(request)
        if user:
            content_type = ContentType.objects.get_for_model(Storage)
            user_wishlist = list(Wishlist.objects.filter(
                user=user,
                content_type=content_type
            ).values_list('object_id', flat=True))
        
        context = {
            'filter': storage_filter,
            'page_obj': page_obj,
            'category': 'Storage',
            'category_slug': 'storage',
            'user_wishlist': user_wishlist
        }
        return render(request, 'catalog/storage.html', context)


class PowerSupplyListView(View):
    def get(self, request):
        power_supplies = PowerSupply.objects.all()
        psu_filter = PowerSupplyFilter(request.GET, queryset=power_supplies)
        
        paginator = Paginator(psu_filter.qs, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        _attach_card_images_to_page(page_obj, PowerSupply)
        
        # Get user's wishlist items
        user_wishlist = []
        user = get_logged_in_user(request)
        if user:
            content_type = ContentType.objects.get_for_model(PowerSupply)
            user_wishlist = list(Wishlist.objects.filter(
                user=user,
                content_type=content_type
            ).values_list('object_id', flat=True))
        
        context = {
            'filter': psu_filter,
            'page_obj': page_obj,
            'category': 'Power Supplies',
            'category_slug': 'power-supplies',
            'user_wishlist': user_wishlist
        }
        return render(request, 'catalog/power_supplies.html', context)


class CaseListView(View):
    def get(self, request):
        cases = Case.objects.all()
        case_filter = CaseFilter(request.GET, queryset=cases)
        
        paginator = Paginator(case_filter.qs, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        _attach_card_images_to_page(page_obj, Case)
        
        # Get user's wishlist items
        user_wishlist = []
        user = get_logged_in_user(request)
        if user:
            content_type = ContentType.objects.get_for_model(Case)
            user_wishlist = list(Wishlist.objects.filter(
                user=user,
                content_type=content_type
            ).values_list('object_id', flat=True))
        
        context = {
            'filter': case_filter,
            'page_obj': page_obj,
            'category': 'Cases',
            'category_slug': 'cases',
            'user_wishlist': user_wishlist
        }
        return render(request, 'catalog/cases.html', context)


class CoolerListView(View):
    def get(self, request):
        coolers = Cooler.objects.all()
        cooler_filter = CoolerFilter(request.GET, queryset=coolers)

        paginator = Paginator(cooler_filter.qs, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        _attach_card_images_to_page(page_obj, Cooler)

        user_wishlist = []
        user = get_logged_in_user(request)
        if user:
            content_type = ContentType.objects.get_for_model(Cooler)
            user_wishlist = list(Wishlist.objects.filter(
                user=user,
                content_type=content_type
            ).values_list('object_id', flat=True))

        context = {
            'filter': cooler_filter,
            'page_obj': page_obj,
            'category': 'Coolers',
            'category_slug': 'coolers',
            'user_wishlist': user_wishlist
        }
        return render(request, 'catalog/coolers.html', context)


class LaptopListView(View):
    def get(self, request):
        laptops = Laptop.objects.all()
        laptop_filter = LaptopFilter(request.GET, queryset=laptops)
        
        paginator = Paginator(laptop_filter.qs, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        _attach_card_images_to_page(page_obj, Laptop)
        
        # Get user's wishlist items
        user_wishlist = []
        user = get_logged_in_user(request)
        if user:
            content_type = ContentType.objects.get_for_model(Laptop)
            user_wishlist = list(Wishlist.objects.filter(
                user=user,
                content_type=content_type
            ).values_list('object_id', flat=True))
        
        context = {
            'filter': laptop_filter,
            'page_obj': page_obj,
            'category': 'Laptops',
            'category_slug': 'laptops',
            'user_wishlist': user_wishlist
        }
        return render(request, 'catalog/laptops.html', context)


class ProcessorDetailView(View):
    def get(self, request, pk):
        processor = get_object_or_404(Processor, pk=pk)
        
        # Check if in wishlist
        user = get_logged_in_user(request)
        in_wishlist = False
        if user:
            content_type = ContentType.objects.get_for_model(Processor)
            in_wishlist = Wishlist.objects.filter(
                user=user,
                content_type=content_type,
                object_id=pk
            ).exists()
            additional_images = _get_additional_images_for_product(processor)
        else:
            content_type = ContentType.objects.get_for_model(Processor)
            additional_images = _get_additional_images_for_product(processor)
        
        context = {
            'product': processor,
            'product_model': processor._meta.model_name,
            'category': 'Processor',
            'wishlist_url': reverse('add_wish_processor', kwargs={'pk': pk}),
            'in_wishlist': in_wishlist,
            'additional_images': additional_images,
            **_get_reviews_context(processor, user),
        }
        return render(request, 'catalog/product_detail.html', context)


class GPUDetailView(View):
    def get(self, request, pk):
        gpu = get_object_or_404(GPU, pk=pk)
        
        user = get_logged_in_user(request)
        in_wishlist = False
        if user:
            content_type = ContentType.objects.get_for_model(GPU)
            in_wishlist = Wishlist.objects.filter(
                user=user,
                content_type=content_type,
                object_id=pk
            ).exists()
            additional_images = _get_additional_images_for_product(gpu)
        else:
            content_type = ContentType.objects.get_for_model(GPU)
            additional_images = _get_additional_images_for_product(gpu)
        
        context = {
            'product': gpu,
            'product_model': gpu._meta.model_name,
            'category': 'GPU',
            'wishlist_url': reverse('add_wish_gpu', kwargs={'pk': pk}),
            'in_wishlist': in_wishlist,
            'additional_images': additional_images,
            **_get_reviews_context(gpu, user),
        }
        return render(request, 'catalog/product_detail.html', context)


class RAMDetailView(View):
    def get(self, request, pk):
        ram = get_object_or_404(RAM, pk=pk)
        
        user = get_logged_in_user(request)
        in_wishlist = False
        if user:
            content_type = ContentType.objects.get_for_model(RAM)
            in_wishlist = Wishlist.objects.filter(
                user=user,
                content_type=content_type,
                object_id=pk
            ).exists()
            additional_images = _get_additional_images_for_product(ram)
        else:
            content_type = ContentType.objects.get_for_model(RAM)
            additional_images = _get_additional_images_for_product(ram)
        
        context = {
            'product': ram,
            'product_model': ram._meta.model_name,
            'category': 'RAM',
            'wishlist_url': reverse('add_wish_ram', kwargs={'pk': pk}),
            'in_wishlist': in_wishlist,
            'additional_images': additional_images,
            **_get_reviews_context(ram, user),
        }
        return render(request, 'catalog/product_detail.html', context)


class MotherboardDetailView(View):
    def get(self, request, pk):
        motherboard = get_object_or_404(Motherboard, pk=pk)
        
        user = get_logged_in_user(request)
        in_wishlist = False
        if user:
            content_type = ContentType.objects.get_for_model(Motherboard)
            in_wishlist = Wishlist.objects.filter(
                user=user,
                content_type=content_type,
                object_id=pk
            ).exists()
            additional_images = _get_additional_images_for_product(motherboard)
        else:
            content_type = ContentType.objects.get_for_model(Motherboard)
            additional_images = _get_additional_images_for_product(motherboard)
        
        context = {
            'product': motherboard,
            'product_model': motherboard._meta.model_name,
            'category': 'Motherboard',
            'wishlist_url': reverse('add_wish_motherboard', kwargs={'pk': pk}),
            'in_wishlist': in_wishlist,
            'additional_images': additional_images,
            **_get_reviews_context(motherboard, user),
        }
        return render(request, 'catalog/product_detail.html', context)


class StorageDetailView(View):
    def get(self, request, pk):
        storage = get_object_or_404(Storage, pk=pk)
        
        user = get_logged_in_user(request)
        in_wishlist = False
        if user:
            content_type = ContentType.objects.get_for_model(Storage)
            in_wishlist = Wishlist.objects.filter(
                user=user,
                content_type=content_type,
                object_id=pk
            ).exists()
            additional_images = _get_additional_images_for_product(storage)
        else:
            content_type = ContentType.objects.get_for_model(Storage)
            additional_images = _get_additional_images_for_product(storage)
        
        context = {
            'product': storage,
            'product_model': storage._meta.model_name,
            'category': 'Storage',
            'wishlist_url': reverse('add_wish_storage', kwargs={'pk': pk}),
            'in_wishlist': in_wishlist,
            'additional_images': additional_images,
            **_get_reviews_context(storage, user),
        }
        return render(request, 'catalog/product_detail.html', context)


class PowerSupplyDetailView(View):
    def get(self, request, pk):
        psu = get_object_or_404(PowerSupply, pk=pk)
        
        user = get_logged_in_user(request)
        in_wishlist = False
        if user:
            content_type = ContentType.objects.get_for_model(PowerSupply)
            in_wishlist = Wishlist.objects.filter(
                user=user,
                content_type=content_type,
                object_id=pk
            ).exists()
            additional_images = _get_additional_images_for_product(psu)
        else:
            content_type = ContentType.objects.get_for_model(PowerSupply)
            additional_images = _get_additional_images_for_product(psu)
        
        context = {
            'product': psu,
            'product_model': psu._meta.model_name,
            'category': 'Power Supply',
            'wishlist_url': reverse('add_wish_power_supply', kwargs={'pk': pk}),
            'in_wishlist': in_wishlist,
            'additional_images': additional_images,
            **_get_reviews_context(psu, user),
        }
        return render(request, 'catalog/product_detail.html', context)


class CaseDetailView(View):
    def get(self, request, pk):
        case = get_object_or_404(Case, pk=pk)
        
        user = get_logged_in_user(request)
        in_wishlist = False
        if user:
            content_type = ContentType.objects.get_for_model(Case)
            in_wishlist = Wishlist.objects.filter(
                user=user,
                content_type=content_type,
                object_id=pk
            ).exists()
            additional_images = _get_additional_images_for_product(case)
        else:
            content_type = ContentType.objects.get_for_model(Case)
            additional_images = _get_additional_images_for_product(case)
        
        context = {
            'product': case,
            'product_model': case._meta.model_name,
            'category': 'Case',
            'wishlist_url': reverse('add_wish_case', kwargs={'pk': pk}),
            'in_wishlist': in_wishlist,
            'additional_images': additional_images,
            **_get_reviews_context(case, user),
        }
        return render(request, 'catalog/product_detail.html', context)


class CoolerDetailView(View):
    def get(self, request, pk):
        cooler = get_object_or_404(Cooler, pk=pk)

        user = get_logged_in_user(request)
        in_wishlist = False
        if user:
            content_type = ContentType.objects.get_for_model(Cooler)
            in_wishlist = Wishlist.objects.filter(
                user=user,
                content_type=content_type,
                object_id=pk
            ).exists()
            additional_images = _get_additional_images_for_product(cooler)
        else:
            content_type = ContentType.objects.get_for_model(Cooler)
            additional_images = _get_additional_images_for_product(cooler)

        context = {
            'product': cooler,
            'product_model': cooler._meta.model_name,
            'category': 'Cooler',
            'wishlist_url': reverse('add_wish_cooler', kwargs={'pk': pk}),
            'in_wishlist': in_wishlist,
            'additional_images': additional_images,
            **_get_reviews_context(cooler, user),
        }
        return render(request, 'catalog/product_detail.html', context)


class LaptopDetailView(View):
    def get(self, request, pk):
        laptop = get_object_or_404(Laptop, pk=pk)
        
        user = get_logged_in_user(request)
        in_wishlist = False
        if user:
            content_type = ContentType.objects.get_for_model(Laptop)
            in_wishlist = Wishlist.objects.filter(
                user=user,
                content_type=content_type,
                object_id=pk
            ).exists()
            additional_images = _get_additional_images_for_product(laptop)
        else:
            content_type = ContentType.objects.get_for_model(Laptop)
            additional_images = _get_additional_images_for_product(laptop)
        
        context = {
            'product': laptop,
            'product_model': laptop._meta.model_name,
            'category': 'Laptop',
            'wishlist_url': reverse('add_wish_laptop', kwargs={'pk': pk}),
            'in_wishlist': in_wishlist,
            'additional_images': additional_images,
            **_get_reviews_context(laptop, user),
        }
        return render(request, 'catalog/product_detail.html', context)
    

# class ProcessorDetailView(View):
#     def get(self, request, pk):
#         processor = get_object_or_404(Processor, pk=pk)
#         context = {'product': processor, 'category': 'Processor'}
#         return render(request, 'catalog/product_detail.html', context)

class AddWishProcessor(View):
    def post(self, request, pk):
        user = get_logged_in_user(request)
        if user:
            processor = get_object_or_404(Processor, pk=pk)
            content_type = ContentType.objects.get_for_model(Processor)
            
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=user,
                content_type=content_type,
                object_id=pk
            )
            
            if not created:
                wishlist_item.delete()
                messages.success(request, 'Removed from wishlist!')
            else:
                messages.success(request, 'Added to wishlist!')
            
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        else:
            messages.error(request, 'First you need to login to add wishes to wishlist')
            return redirect('login_view')


class AddWishGPU(View):
    def post(self, request, pk):
        user = get_logged_in_user(request)
        if user:
            gpu = get_object_or_404(GPU, pk=pk)
            content_type = ContentType.objects.get_for_model(GPU)
            
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=user,
                content_type=content_type,
                object_id=pk
            )
            
            if not created:
                wishlist_item.delete()
                messages.success(request, 'Removed from wishlist!')
            else:
                messages.success(request, 'Added to wishlist!')
            
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        else:
            messages.error(request, 'First you need to login to add wishes to wishlist')
            return redirect('login_view')


class AddWishRAM(View):
    def post(self, request, pk):
        user = get_logged_in_user(request)
        if user:
            ram = get_object_or_404(RAM, pk=pk)
            content_type = ContentType.objects.get_for_model(RAM)
            
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=user,
                content_type=content_type,
                object_id=pk
            )
            
            if not created:
                wishlist_item.delete()
                messages.success(request, 'Removed from wishlist!')
            else:
                messages.success(request, 'Added to wishlist!')
            
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        else:
            messages.error(request, 'First you need to login to add wishes to wishlist')
            return redirect('login_view')


class AddWishMotherboard(View):
    def post(self, request, pk):
        user = get_logged_in_user(request)
        if user:
            motherboard = get_object_or_404(Motherboard, pk=pk)
            content_type = ContentType.objects.get_for_model(Motherboard)
            
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=user,
                content_type=content_type,
                object_id=pk
            )
            
            if not created:
                wishlist_item.delete()
                messages.success(request, 'Removed from wishlist!')
            else:
                messages.success(request, 'Added to wishlist!')
            
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        else:
            messages.error(request, 'First you need to login to add wishes to wishlist')
            return redirect('login_view')


class AddWishStorage(View):
    def post(self, request, pk):
        user = get_logged_in_user(request)
        if user:
            storage = get_object_or_404(Storage, pk=pk)
            content_type = ContentType.objects.get_for_model(Storage)
            
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=user,
                content_type=content_type,
                object_id=pk
            )
            
            if not created:
                wishlist_item.delete()
                messages.success(request, 'Removed from wishlist!')
            else:
                messages.success(request, 'Added to wishlist!')
            
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        else:
            messages.error(request, 'First you need to login to add wishes to wishlist')
            return redirect('login_view')


class AddWishPowerSupply(View):
    def post(self, request, pk):
        user = get_logged_in_user(request)
        if user:
            psu = get_object_or_404(PowerSupply, pk=pk)
            content_type = ContentType.objects.get_for_model(PowerSupply)
            
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=user,
                content_type=content_type,
                object_id=pk
            )
            
            if not created:
                wishlist_item.delete()
                messages.success(request, 'Removed from wishlist!')
            else:
                messages.success(request, 'Added to wishlist!')
            
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        else:
            messages.error(request, 'First you need to login to add wishes to wishlist')
            return redirect('login_view')


class AddWishCase(View):
    def post(self, request, pk):
        user = get_logged_in_user(request)
        if user:
            case = get_object_or_404(Case, pk=pk)
            content_type = ContentType.objects.get_for_model(Case)
            
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=user,
                content_type=content_type,
                object_id=pk
            )
            
            if not created:
                wishlist_item.delete()
                messages.success(request, 'Removed from wishlist!')
            else:
                messages.success(request, 'Added to wishlist!')
            
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        else:
            messages.error(request, 'First you need to login to add wishes to wishlist')
            return redirect('login_view')


class AddWishCooler(View):
    def post(self, request, pk):
        user = get_logged_in_user(request)
        if user:
            cooler = get_object_or_404(Cooler, pk=pk)
            content_type = ContentType.objects.get_for_model(Cooler)

            wishlist_item, created = Wishlist.objects.get_or_create(
                user=user,
                content_type=content_type,
                object_id=pk
            )

            if not created:
                wishlist_item.delete()
                messages.success(request, 'Removed from wishlist!')
            else:
                messages.success(request, 'Added to wishlist!')

            return redirect(request.META.get('HTTP_REFERER', 'home'))
        else:
            messages.error(request, 'First you need to login to add wishes to wishlist')
            return redirect('login_view')


class AddWishLaptop(View):
    def post(self, request, pk):
        user = get_logged_in_user(request)
        if user:
            laptop = get_object_or_404(Laptop, pk=pk)
            content_type = ContentType.objects.get_for_model(Laptop)
            
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=user,
                content_type=content_type,
                object_id=pk
            )
            
            if not created:
                wishlist_item.delete()
                messages.success(request, 'Removed from wishlist!')
            else:
                messages.success(request, 'Added to wishlist!')
            
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        else:
            messages.error(request, 'First you need to login to add wishes to wishlist')
            return redirect('login_view')


class WishlistView(View):
    def get(self, request):
        user = get_logged_in_user(request)
        if not user:
            messages.error(request, 'First you need to login to view wishlist')
            return redirect('login_view')

        items = Wishlist.objects.filter(user=user).select_related('content_type').order_by('-created_at')

        enriched = []
        for item in items:
            product = item.content_object
            if not product:
                continue
            image = ""
            try:
                image = product.image.url if getattr(product, "image", None) else ""
            except ValueError:
                image = ""
            enriched.append(
                {
                    "id": item.id,
                    "name": getattr(product, "name", "Unknown product"),
                    "manufacturer": getattr(product, "manufacturer", ""),
                    "price": getattr(product, "price", 0),
                    "category": item.content_type.model,
                    "image": image,
                    "product_id": product.pk,
                    "created_at": item.created_at,
                }
            )

        return render(request, "wishlist.html", {"items": enriched})


class RemoveWishlistItemView(View):
    def post(self, request, pk):
        user = get_logged_in_user(request)
        if not user:
            messages.error(request, 'First you need to login')
            return redirect('login_view')
        item = get_object_or_404(Wishlist, pk=pk, user=user)
        item.delete()
        messages.success(request, 'Removed from wishlist!')
        return redirect('wishlist')


class AddWishlistItemToCartView(View):
    def post(self, request, pk):
        user = get_logged_in_user(request)
        if not user:
            messages.error(request, 'First you need to login')
            return redirect('login_view')
        item = get_object_or_404(Wishlist, pk=pk, user=user)
        product = item.content_object
        if not product:
            messages.error(request, 'Product is unavailable.')
            return redirect('wishlist')

        image = ""
        try:
            image = product.image.url if getattr(product, "image", None) else ""
        except ValueError:
            image = ""

        _add_to_session_cart(
            request,
            {
                "id": f"{item.content_type.model}-{product.pk}",
                "name": getattr(product, "name", "Product"),
                "price": float(getattr(product, "price", 0)),
                "image": image,
                "category": "Wishlist",
            },
        )
        messages.success(request, _('Added to cart!'))
        return redirect('wishlist')


class ExploreAllView(View):
    """Страница со смешанным набором товаров из разных категорий."""
    def get(self, request):
        user = get_logged_in_user(request)
        search_query = (request.GET.get("q") or request.GET.get("search") or "").strip().lower()
        allowed_models = {
            "processor",
            "gpu",
            "motherboard",
            "ram",
            "storage",
            "powersupply",
            "case",
            "cooler",
        }
        showcase_items = ExploreShowcaseItem.objects.filter(is_active=True).select_related("content_type")
        cards = []
        cards_for_gallery = []

        if showcase_items.exists():
            for item in showcase_items:
                if item.content_type.model not in allowed_models:
                    continue
                product = item.content_object
                if not product:
                    continue
                image = ""
                image = _safe_main_image_url(product)
                cards.append(
                    {
                        "title": item.title or getattr(product, "name", "Product"),
                        "name": getattr(product, "name", "Product"),
                        "manufacturer": getattr(product, "manufacturer", ""),
                        "price": getattr(product, "price", 0),
                        "stock": max(0, int(getattr(product, "stock", 0) or 0)),
                        "image": image,
                        "category": CATEGORY_DISPLAY_MAP.get(item.content_type.model, item.content_type.model.replace("_", " ").title()),
                        "category_key": item.content_type.model,
                        "content_type_id": item.content_type_id,
                        "object_id": product.pk,
                        "detail_url": _detail_url_for_product(product),
                    }
                )
                cards_for_gallery.append((item.content_type_id, product.pk, len(cards) - 1))
        else:
            pools = [
                list(Processor.objects.all()[:4]),
                list(GPU.objects.all()[:4]),
                list(Motherboard.objects.all()[:4]),
                list(RAM.objects.all()[:4]),
                list(Storage.objects.all()[:4]),
                list(PowerSupply.objects.all()[:4]),
                list(Case.objects.all()[:4]),
                list(Cooler.objects.all()[:4]),
            ]
            for bucket in pools:
                for product in bucket:
                    image = ""
                    image = _safe_main_image_url(product)
                    ct_id = ContentType.objects.get_for_model(product.__class__).id
                    cards.append(
                        {
                            "title": getattr(product, "name", "Product"),
                            "name": getattr(product, "name", "Product"),
                            "manufacturer": getattr(product, "manufacturer", ""),
                            "price": getattr(product, "price", 0),
                            "stock": max(0, int(getattr(product, "stock", 0) or 0)),
                            "image": image,
                            "category": _product_category_label(product),
                            "category_key": product._meta.model_name,
                            "content_type_id": ct_id,
                            "object_id": product.pk,
                            "detail_url": _detail_url_for_product(product),
                        }
                    )
                    cards_for_gallery.append((ct_id, product.pk, len(cards) - 1))
            cards.sort(key=lambda x: (x["category"].lower(), x["name"].lower()))

        ct_to_object_ids = defaultdict(set)
        for ct_id, obj_id, _ in cards_for_gallery:
            ct_to_object_ids[ct_id].add(obj_id)
        extra_map = defaultdict(list)
        for ct_id, object_ids in ct_to_object_ids.items():
            rows = ProductImage.objects.filter(
                content_type_id=ct_id,
                object_id__in=list(object_ids),
            ).order_by("object_id", "order", "id")
            for row in rows:
                if not getattr(row, "image", None):
                    continue
                try:
                    url = row.image.url
                except ValueError:
                    continue
                if url:
                    extra_map[(ct_id, row.object_id)].append(url)
        for ct_id, obj_id, idx in cards_for_gallery:
            cards[idx]["card_images"] = _build_card_images(
                cards[idx].get("image", ""),
                extra_map.get((ct_id, obj_id), []),
            )

        if search_query:
            aliases = {
                "processor": {"processor", "processors", "cpu", "процессор", "процессоры"},
                "gpu": {"gpu", "graphics", "graphics card", "graphics cards", "video card", "videocard", "видеокарта", "видеокарты", "графика"},
                "ram": {"ram", "memory", "оперативная память", "озу", "память"},
                "motherboard": {"motherboard", "motherboards", "mainboard", "материнская плата", "материнка"},
                "storage": {"storage", "ssd", "hdd", "накопитель", "диск", "хранилище"},
                "powersupply": {"psu", "power supply", "power supplies", "блок питания", "питание"},
                "case": {"case", "pc case", "корпус"},
                "cooler": {"cooler", "cooling", "fan", "кулер", "охлаждение", "вентилятор"},
                "laptop": {"laptop", "notebook", "ноутбук", "ноутбуки"},
            }

            def matches_query(card):
                haystacks = [
                    str(card.get("name", "")).lower(),
                    str(card.get("manufacturer", "")).lower(),
                    str(card.get("category", "")).lower(),
                ]
                if any(search_query in value for value in haystacks):
                    return True
                category_key = str(card.get("category_key", "")).lower()
                alias_values = aliases.get(category_key, set())
                return any(search_query in alias for alias in alias_values)

            cards = [c for c in cards if matches_query(c)]

        # Filters
        q_category = (request.GET.get("category") or "").strip().lower()
        q_min = request.GET.get("min_price")
        q_max = request.GET.get("max_price")
        q_sort = (request.GET.get("sort") or "").strip()

        if q_category:
            cards = [c for c in cards if c["category"].lower() == q_category]
        try:
            if q_min:
                min_price = float(q_min)
                cards = [c for c in cards if float(c["price"]) >= min_price]
        except ValueError:
            pass
        try:
            if q_max:
                max_price = float(q_max)
                cards = [c for c in cards if float(c["price"]) <= max_price]
        except ValueError:
            pass

        if q_sort == "price_asc":
            cards.sort(key=lambda x: float(x["price"]))
        elif q_sort == "price_desc":
            cards.sort(key=lambda x: float(x["price"]), reverse=True)
        elif q_sort == "name_asc":
            cards.sort(key=lambda x: x["name"].lower())

        categories = sorted({c["category"] for c in cards})

        paginator = Paginator(cards, 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        page_cards = list(page_obj.object_list)

        liked_keys = set()
        if user:
            liked_keys = set(
                Wishlist.objects.filter(user=user).values_list("content_type_id", "object_id")
            )

        wish_url_map = {
            "processor": "add_wish_processor",
            "gpu": "add_wish_gpu",
            "ram": "add_wish_ram",
            "motherboard": "add_wish_motherboard",
            "storage": "add_wish_storage",
            "powersupply": "add_wish_power_supply",
            "case": "add_wish_case",
            "cooler": "add_wish_cooler",
        }

        for c in page_cards:
            c["in_wishlist"] = (c["content_type_id"], c["object_id"]) in liked_keys
            c["wishlist_url_name"] = wish_url_map.get(c["category"].lower().replace(" ", ""), "")

        return render(
            request,
            "explore_all.html",
            {
                "cards": page_cards,
                "page_obj": page_obj,
                "categories": categories,
                "current_category": q_category,
                "min_price": q_min or "",
                "max_price": q_max or "",
                "sort": q_sort,
                "search_query": search_query,
            },
        )


class ToggleExploreLikeView(View):
    def post(self, request):
        user = get_logged_in_user(request)
        if not user:
            messages.error(request, "First you need to login")
            return redirect("login_view")

        ct_id = request.POST.get("content_type_id")
        obj_id = request.POST.get("object_id")
        next_url = request.POST.get("next") or "explore_all"

        try:
            ct_id = int(ct_id)
            obj_id = int(obj_id)
        except (TypeError, ValueError):
            return redirect(next_url)

        like, created = ExploreLike.objects.get_or_create(
            user=user,
            content_type_id=ct_id,
            object_id=obj_id,
        )
        if not created:
            like.delete()
        return redirect(next_url)


class ToggleWishlistAjaxView(View):
    def post(self, request):
        user = get_logged_in_user(request)
        if not user:
            return JsonResponse({"ok": False, "error": "auth_required"}, status=401)

        ct_id = request.POST.get("content_type_id")
        obj_id = request.POST.get("object_id")
        try:
            ct_id = int(ct_id)
            obj_id = int(obj_id)
        except (TypeError, ValueError):
            return JsonResponse({"ok": False, "error": "bad_params"}, status=400)

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=user,
            content_type_id=ct_id,
            object_id=obj_id,
        )
        if not created:
            wishlist_item.delete()
            in_wishlist = False
        else:
            in_wishlist = True

        return JsonResponse({"ok": True, "in_wishlist": in_wishlist})
