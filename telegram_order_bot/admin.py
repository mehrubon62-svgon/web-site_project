from django.contrib import admin

from .models import TelegramAdminLink, TelegramOrderNotification


@admin.register(TelegramAdminLink)
class TelegramAdminLinkAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "telegram_user_id",
        "telegram_chat_id",
        "telegram_username",
        "is_active",
        "receive_new_order_notifications",
        "updated_at",
    )
    list_filter = ("is_active", "receive_new_order_notifications", "created_at", "updated_at")
    search_fields = ("user__username", "user__email", "telegram_user_id", "telegram_username")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Admin link",
            {
                "fields": (
                    "user",
                    "telegram_user_id",
                    "telegram_chat_id",
                    "telegram_username",
                    "is_active",
                    "receive_new_order_notifications",
                )
            },
        ),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(TelegramOrderNotification)
class TelegramOrderNotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "admin_link",
        "event_type",
        "delivery_status",
        "sent_at",
        "created_at",
    )
    list_filter = ("event_type", "delivery_status", "created_at", "sent_at")
    search_fields = (
        "order__id",
        "order__user__username",
        "admin_link__user__username",
        "error_message",
    )
    readonly_fields = ("created_at", "updated_at", "sent_at")

