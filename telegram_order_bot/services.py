from __future__ import annotations

from decimal import Decimal
from html import escape

from django.db.models import Q
from django.utils import timezone

from orders.models import Order

from .models import TelegramAdminLink, TelegramOrderNotification


STATUS_LABELS_RU = {
    "PENDING": "Ожидает",
    "PROCESSING": "В обработке",
    "SHIPPED": "В пути",
    "DELIVERED": "Доставлен",
    "CANCELLED": "Отменен",
}

STATUS_BADGES = {
    "PENDING": "Новый",
    "PROCESSING": "Сборка",
    "SHIPPED": "Доставка",
    "DELIVERED": "Завершен",
    "CANCELLED": "Отмена",
}


def get_status_label(status: str) -> str:
    return STATUS_LABELS_RU.get(status, status)


def get_status_badge(status: str) -> str:
    return STATUS_BADGES.get(status, status)


def _admin_links_queryset():
    return TelegramAdminLink.objects.select_related("user").filter(
        is_active=True,
        user__is_active=True,
    ).filter(Q(user__is_staff=True) | Q(user__is_superuser=True))


def is_authorized_admin(telegram_user_id: int) -> bool:
    return _admin_links_queryset().filter(telegram_user_id=telegram_user_id).exists()


def get_authorized_admin_link(telegram_user_id: int) -> TelegramAdminLink | None:
    return _admin_links_queryset().filter(telegram_user_id=telegram_user_id).first()


def touch_admin_presence(telegram_user_id: int, chat_id: int | None, username: str | None) -> None:
    link = get_authorized_admin_link(telegram_user_id)
    if not link:
        return

    updated_fields = []
    if chat_id and link.telegram_chat_id != chat_id:
        link.telegram_chat_id = chat_id
        updated_fields.append("telegram_chat_id")
    username = (username or "").strip()
    if link.telegram_username != username:
        link.telegram_username = username
        updated_fields.append("telegram_username")
    if updated_fields:
        updated_fields.append("updated_at")
        link.save(update_fields=updated_fields)


def format_money(value) -> str:
    amount = Decimal(str(value or 0))
    return f"${amount:.2f}"


def _compact_text(value: str | None, fallback: str) -> str:
    cleaned = (value or "").strip()
    return cleaned if cleaned else fallback


def build_welcome_message(link: TelegramAdminLink | None) -> str:
    username = link.user.username if link else "admin"
    chat_id = link.telegram_chat_id if link and link.telegram_chat_id else "будет сохранен после первого сообщения"
    return (
        "<b>BuildBox Order Desk</b>\n"
        f"Админ: <b>{escape(username)}</b>\n"
        f"Telegram user ID: <code>{link.telegram_user_id if link else '-'}</code>\n"
        f"Chat ID: <code>{chat_id}</code>\n\n"
        "<b>Доступные действия</b>\n"
        "• <code>/orders</code> — открыть последние заказы\n"
        "• кнопки под заказом — быстро сменить статус\n"
        "• новые заказы будут приходить сюда автоматически"
    )


def build_link_hint_message(telegram_user_id: int, chat_id: int | None) -> str:
    return (
        "<b>BuildBox Order Desk</b>\n"
        "Доступ пока не выдан.\n\n"
        "<b>Передай эти данные в Django admin</b>\n"
        f"Telegram user ID: <code>{telegram_user_id}</code>\n"
        f"Telegram chat ID: <code>{chat_id or '-'}</code>\n\n"
        "После добавления в <b>Telegram admin links</b> отправь команду <code>/start</code> ещё раз."
    )


def build_orders_list_message(orders: list[dict]) -> str:
    if not orders:
        return "<b>BuildBox Orders</b>\nПока нет заказов."

    lines = ["<b>BuildBox Orders</b>", "Последние заказы:", ""]
    for order in orders:
        lines.append(
            f"• <b>#{order['id']}</b> [{escape(order['status_badge'])}] "
            f"{escape(order['full_name'])} — <b>{escape(order['total_price'])}</b>"
        )
    lines.append("")
    lines.append("Нажми на кнопку ниже, чтобы открыть карточку заказа.")
    return "\n".join(lines)


def build_order_message(order: Order, heading: str = "Заказ") -> str:
    configuration_name = order.configuration.name if order.configuration else "Без сохраненной конфигурации"
    created = timezone.localtime(order.created_at).strftime("%Y-%m-%d %H:%M")
    comment = _compact_text(order.comment, "Без комментария")
    username = order.user.username if order.user_id else "Unknown"
    badge = get_status_badge(order.status)

    return (
        f"<b>{escape(heading)} #{order.id}</b>\n"
        f"Метка: <b>{escape(badge)}</b>\n"
        f"Статус: <b>{escape(get_status_label(order.status))}</b>\n"
        f"Сумма: <b>{escape(format_money(order.total_price))}</b>\n\n"
        f"<b>Клиент</b>\n"
        f"• Пользователь: <b>{escape(username)}</b>\n"
        f"• Получатель: <b>{escape(order.full_name)}</b>\n"
        f"• Телефон: <code>{escape(order.phone)}</code>\n"
        f"• Email: <code>{escape(order.email)}</code>\n\n"
        f"<b>Доставка</b>\n"
        f"• Адрес: {escape(order.address)}\n"
        f"• Комментарий: {escape(comment)}\n\n"
        f"<b>Сборка</b>\n"
        f"• Конфигурация: {escape(configuration_name)}\n"
        f"• Создан: {escape(created)}"
    )


def queue_new_order_notifications(order_id: int) -> int:
    order = (
        Order.objects.select_related("user", "configuration")
        .filter(pk=order_id)
        .first()
    )
    if not order:
        return 0

    message_text = build_order_message(order, heading="Новый заказ")
    created_count = 0
    admin_links = _admin_links_queryset().filter(receive_new_order_notifications=True)
    for admin_link in admin_links:
        _, created = TelegramOrderNotification.objects.get_or_create(
            admin_link=admin_link,
            order=order,
            event_type=TelegramOrderNotification.EVENT_NEW_ORDER,
            defaults={"message_text": message_text},
        )
        if created:
            created_count += 1
    return created_count


def get_recent_orders(limit: int = 10) -> list[dict]:
    orders = (
        Order.objects.select_related("user", "configuration")
        .order_by("-created_at")[:limit]
    )
    return [
        {
            "id": order.id,
            "status": order.status,
            "status_label": get_status_label(order.status),
            "status_badge": get_status_badge(order.status),
            "total_price": format_money(order.total_price),
            "full_name": order.full_name,
        }
        for order in orders
    ]


def get_order_snapshot(order_id: int) -> dict | None:
    order = Order.objects.select_related("user", "configuration").filter(pk=order_id).first()
    if not order:
        return None
    return {
        "id": order.id,
        "status": order.status,
        "status_label": get_status_label(order.status),
        "message_text": build_order_message(order),
    }


def set_order_status(order_id: int, new_status: str) -> dict:
    valid_statuses = {choice[0] for choice in Order.STATUS_CHOICES}
    if new_status not in valid_statuses:
        return {"ok": False, "error": "invalid_status"}

    order = Order.objects.filter(pk=order_id).first()
    if not order:
        return {"ok": False, "error": "order_not_found"}

    if order.status == new_status:
        return {
            "ok": True,
            "changed": False,
            "order_id": order.id,
            "status": order.status,
            "status_label": get_status_label(order.status),
        }

    order.status = new_status
    order.save(update_fields=["status", "updated_at"])
    snapshot = get_order_snapshot(order.id)
    return {
        "ok": True,
        "changed": True,
        "order_id": order.id,
        "status": snapshot["status"],
        "status_label": snapshot["status_label"],
        "message_text": snapshot["message_text"],
    }


def get_pending_notifications(limit: int = 20) -> list[dict]:
    notifications = (
        TelegramOrderNotification.objects.select_related("admin_link", "order")
        .filter(
            delivery_status=TelegramOrderNotification.STATUS_PENDING,
            admin_link__is_active=True,
            admin_link__receive_new_order_notifications=True,
        )
        .exclude(admin_link__telegram_chat_id__isnull=True)
        .order_by("created_at")[:limit]
    )
    return [
        {
            "id": notification.id,
            "chat_id": notification.admin_link.telegram_chat_id,
            "order_id": notification.order_id,
            "order_status": notification.order.status,
            "message_text": notification.message_text,
        }
        for notification in notifications
    ]


def mark_notification_sent(notification_id: int) -> None:
    TelegramOrderNotification.objects.filter(pk=notification_id).update(
        delivery_status=TelegramOrderNotification.STATUS_SENT,
        sent_at=timezone.now(),
        error_message="",
        updated_at=timezone.now(),
    )


def mark_notification_failed(notification_id: int, error_message: str) -> None:
    TelegramOrderNotification.objects.filter(pk=notification_id).update(
        delivery_status=TelegramOrderNotification.STATUS_FAILED,
        error_message=(error_message or "")[:2000],
        updated_at=timezone.now(),
    )
