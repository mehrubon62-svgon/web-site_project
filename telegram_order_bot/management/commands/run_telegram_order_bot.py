import asyncio

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Run the Telegram order bot for admins."

    def handle(self, *args, **options):
        if not getattr(settings, "TELEGRAM_ORDER_BOT_TOKEN", "").strip():
            raise CommandError("TELEGRAM_ORDER_BOT_TOKEN is not set.")

        try:
            from telegram_order_bot.bot.runner import run_bot
        except ModuleNotFoundError as exc:
            if exc.name == "aiogram":
                raise CommandError(
                    "aiogram is not installed. Install it first, for example: pip install aiogram"
                ) from exc
            raise

        self.stdout.write(self.style.SUCCESS("Starting Telegram order bot..."))
        asyncio.run(run_bot())

