from django.apps import AppConfig


class TelegramOrderBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "telegram_order_bot"
    verbose_name = "Telegram Order Bot"

    def ready(self):
        from . import signals  # noqa: F401

