from django.core.exceptions import ValidationError
from django.db import models

from my_site_register.models import UniqUser
from orders.models import Order


class TelegramAdminLink(models.Model):
    user = models.OneToOneField(
        UniqUser,
        on_delete=models.CASCADE,
        related_name="telegram_admin_link",
        verbose_name="Admin user",
    )
    telegram_user_id = models.BigIntegerField(unique=True, verbose_name="Telegram user ID")
    telegram_chat_id = models.BigIntegerField(blank=True, null=True, verbose_name="Telegram chat ID")
    telegram_username = models.CharField(max_length=255, blank=True, verbose_name="Telegram username")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    receive_new_order_notifications = models.BooleanField(
        default=True,
        verbose_name="Receive new order notifications",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Telegram admin link"
        verbose_name_plural = "Telegram admin links"
        ordering = ["user__username"]

    def clean(self):
        if self.user_id and not (self.user.is_staff or self.user.is_superuser):
            raise ValidationError("Only staff or superuser accounts can be linked to the Telegram order bot.")

    def __str__(self):
        return f"{self.user.username} -> {self.telegram_user_id}"


class TelegramOrderNotification(models.Model):
    EVENT_NEW_ORDER = "NEW_ORDER"
    EVENT_CHOICES = [
        (EVENT_NEW_ORDER, "New order"),
    ]

    STATUS_PENDING = "PENDING"
    STATUS_SENT = "SENT"
    STATUS_FAILED = "FAILED"
    DELIVERY_STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_SENT, "Sent"),
        (STATUS_FAILED, "Failed"),
    ]

    admin_link = models.ForeignKey(
        TelegramAdminLink,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="Telegram admin link",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="telegram_notifications",
        verbose_name="Order",
    )
    event_type = models.CharField(
        max_length=30,
        choices=EVENT_CHOICES,
        default=EVENT_NEW_ORDER,
        verbose_name="Event type",
    )
    message_text = models.TextField(verbose_name="Message text")
    delivery_status = models.CharField(
        max_length=20,
        choices=DELIVERY_STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name="Delivery status",
    )
    error_message = models.TextField(blank=True, verbose_name="Error message")
    sent_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Telegram order notification"
        verbose_name_plural = "Telegram order notifications"
        ordering = ["delivery_status", "-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["admin_link", "order", "event_type"],
                name="uniq_tg_order_event_per_admin",
            )
        ]

    def __str__(self):
        return f"Notification #{self.pk} -> order #{self.order_id} ({self.delivery_status})"

