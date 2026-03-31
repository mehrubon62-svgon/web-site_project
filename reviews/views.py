from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.utils import ProgrammingError, OperationalError
from django.http import JsonResponse
from django.utils.timezone import localtime
from urllib.parse import urlsplit, urlunsplit
from my_site_register.permissions import get_logged_in_user
from .models import Review, ReviewReply
from my_site_app.models import Processor, GPU, RAM, Motherboard, Storage, PowerSupply, Case, Laptop


MODEL_MAP = {
    "processor": Processor,
    "gpu": GPU,
    "ram": RAM,
    "motherboard": Motherboard,
    "storage": Storage,
    "powersupply": PowerSupply,
    "case": Case,
    "laptop": Laptop,
}


def _resolve_model_class(model_name):
    raw = (model_name or "").strip().lower()
    normalized = raw.replace("_", "").replace("-", "").replace(" ", "")
    aliases = {
        "powersupply": PowerSupply,
        "powersupplies": PowerSupply,
        "psu": PowerSupply,
    }
    if raw in MODEL_MAP:
        return MODEL_MAP[raw]
    if normalized in MODEL_MAP:
        return MODEL_MAP[normalized]
    if normalized in aliases:
        return aliases[normalized]
    for cls in MODEL_MAP.values():
        if cls._meta.model_name == raw or cls._meta.model_name == normalized:
            return cls
    return None


def _resolve_model_class_fallback(request, pk):
    ref = request.META.get("HTTP_REFERER", "")
    if ref:
        path_parts = [p for p in urlsplit(ref).path.strip("/").split("/") if p]
        route_key = path_parts[1] if len(path_parts) >= 2 and path_parts[0] == "main_site" else (path_parts[0] if path_parts else "")
        route_map = {
            "processor": Processor,
            "gpu": GPU,
            "ram": RAM,
            "motherboard": Motherboard,
            "storage": Storage,
            "power-supply": PowerSupply,
            "powersupply": PowerSupply,
            "case": Case,
            "laptop": Laptop,
        }
        if route_key in route_map:
            return route_map[route_key]

    candidates = [cls for cls in MODEL_MAP.values() if cls.objects.filter(pk=pk).exists()]
    if len(candidates) == 1:
        return candidates[0]
    return None


def _redirect_back_to_reviews(request):
    ref = request.META.get("HTTP_REFERER", "")
    if not ref:
        return redirect("home")
    parts = urlsplit(ref)
    return redirect(urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, "reviews-section")))


def _is_ajax(request):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def _review_stats_for(content_type, object_id):
    reviews_qs = Review.objects.filter(content_type=content_type, object_id=object_id, is_approved=True)
    count = reviews_qs.count()
    avg = round(sum(r.rating for r in reviews_qs) / count, 1) if count else 0
    return avg, count


class AddReviewView(View):
    def post(self, request, model_name, pk):
        if (model_name or "").strip().lower() == "reply":
            if _is_ajax(request):
                return JsonResponse({"ok": False, "error": "Invalid review route."}, status=400)
            messages.error(request, "Invalid review route.")
            return _redirect_back_to_reviews(request)

        user = get_logged_in_user(request)
        if not user:
            if _is_ajax(request):
                return JsonResponse({"ok": False, "error": "Please log in first."}, status=401)
            messages.error(request, "Please log in first.")
            return redirect("login_view")

        model_cls = _resolve_model_class(model_name)
        if not model_cls:
            model_cls = _resolve_model_class_fallback(request, pk)
        if not model_cls:
            if _is_ajax(request):
                return JsonResponse({"ok": False, "error": "Unsupported product type for review."}, status=400)
            messages.error(request, "Unsupported product type for review.")
            return redirect(request.META.get("HTTP_REFERER", "home"))

        product = get_object_or_404(model_cls, pk=pk)
        rating_raw = request.POST.get("rating", "5").strip()
        comment = request.POST.get("comment", "").strip()

        if not comment:
            if _is_ajax(request):
                return JsonResponse({"ok": False, "error": "Review text cannot be empty."}, status=400)
            messages.error(request, "Review text cannot be empty.")
            return redirect(request.META.get("HTTP_REFERER", "home"))

        try:
            rating = int(rating_raw)
        except ValueError:
            rating = 5
        rating = min(5, max(1, rating))

        content_type = ContentType.objects.get_for_model(model_cls)
        existing_reviews = Review.objects.filter(user=user, content_type=content_type, object_id=product.pk).order_by("-created_at")
        was_created = False
        if existing_reviews.exists():
            review = existing_reviews.first()
            review.rating = rating
            review.comment = comment
            review.is_approved = True
            review.save(update_fields=["rating", "comment", "is_approved"])
            # Safety cleanup for legacy duplicate rows.
            existing_reviews.exclude(pk=review.pk).delete()
            messages.success(request, "Your review was updated.")
        else:
            review = Review.objects.create(
                user=user,
                content_type=content_type,
                object_id=product.pk,
                rating=rating,
                comment=comment,
                is_approved=True,
            )
            was_created = True
            messages.success(request, "Review added successfully.")

        if _is_ajax(request):
            avg_rating, review_count = _review_stats_for(content_type, product.pk)
            return JsonResponse(
                {
                    "ok": True,
                    "created": was_created,
                    "review": {
                        "id": review.id,
                        "rating": review.rating,
                        "comment": review.comment,
                        "created_at": localtime(review.created_at).strftime("%b %d, %Y %H:%M"),
                        "username": user.username,
                        "avatar_url": user.profile_image.url if user.profile_image else "",
                    },
                    "avg_rating": avg_rating,
                    "review_count": review_count,
                }
            )
        return _redirect_back_to_reviews(request)


class AddReviewReplyView(View):
    def post(self, request, review_id):
        user = get_logged_in_user(request)
        if not user:
            if _is_ajax(request):
                return JsonResponse({"ok": False, "error": "Please log in first."}, status=401)
            messages.error(request, "Please log in first.")
            return redirect("login_view")

        review = get_object_or_404(Review, pk=review_id, is_approved=True)
        comment = request.POST.get("comment", "").strip()
        if not comment:
            if _is_ajax(request):
                return JsonResponse({"ok": False, "error": "Reply cannot be empty."}, status=400)
            messages.error(request, "Reply cannot be empty.")
            return _redirect_back_to_reviews(request)

        try:
            reply = ReviewReply.objects.create(review=review, user=user, comment=comment)
            messages.success(request, "Reply added.")
            if _is_ajax(request):
                return JsonResponse(
                    {
                        "ok": True,
                        "reply": {
                            "id": reply.id,
                            "comment": reply.comment,
                            "created_at": localtime(reply.created_at).strftime("%b %d, %Y %H:%M"),
                            "username": user.username,
                            "avatar_url": user.profile_image.url if user.profile_image else "",
                            "review_id": review.id,
                        },
                    }
                )
        except (ProgrammingError, OperationalError):
            if _is_ajax(request):
                return JsonResponse({"ok": False, "error": "Replies are not ready yet. Run migrations and try again."}, status=500)
            messages.error(request, "Replies are not ready yet. Run migrations and try again.")
        except Exception:
            if _is_ajax(request):
                return JsonResponse({"ok": False, "error": "Unexpected server error while adding reply."}, status=500)
            messages.error(request, "Unexpected server error while adding reply.")
        return _redirect_back_to_reviews(request)


class DeleteReviewView(View):
    def post(self, request, review_id):
        user = get_logged_in_user(request)
        if not user:
            if _is_ajax(request):
                return JsonResponse({"ok": False, "error": "Please log in first."}, status=401)
            messages.error(request, "Please log in first.")
            return redirect("login_view")

        review = get_object_or_404(Review, pk=review_id)
        if review.user_id != user.id:
            if _is_ajax(request):
                return JsonResponse({"ok": False, "error": "You can delete only your own review."}, status=403)
            messages.error(request, "You can delete only your own review.")
            return _redirect_back_to_reviews(request)

        review.delete()
        if _is_ajax(request):
            return JsonResponse({"ok": True, "review_id": review_id})
        messages.success(request, "Review deleted.")
        return _redirect_back_to_reviews(request)


class DeleteReviewReplyView(View):
    def post(self, request, reply_id):
        user = get_logged_in_user(request)
        if not user:
            if _is_ajax(request):
                return JsonResponse({"ok": False, "error": "Please log in first."}, status=401)
            messages.error(request, "Please log in first.")
            return redirect("login_view")

        reply = get_object_or_404(ReviewReply, pk=reply_id)
        if reply.user_id != user.id:
            if _is_ajax(request):
                return JsonResponse({"ok": False, "error": "You can delete only your own reply."}, status=403)
            messages.error(request, "You can delete only your own reply.")
            return _redirect_back_to_reviews(request)

        review_id = reply.review_id
        reply.delete()
        if _is_ajax(request):
            return JsonResponse({"ok": True, "reply_id": reply_id, "review_id": review_id})
        messages.success(request, "Reply deleted.")
        return _redirect_back_to_reviews(request)
