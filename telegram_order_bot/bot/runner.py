from __future__ import annotations

import asyncio
import contextlib
import logging

from asgiref.sync import sync_to_async
from django.conf import settings

from telegram_order_bot import services

from .handlers import build_router


logger = logging.getLogger(__name__)


async def notification_worker(bot, InlineKeyboardBuilder):
    interval = max(1, int(getattr(settings, "TELEGRAM_ORDER_BOT_POLL_INTERVAL", 5)))
    while True:
        notifications = await sync_to_async(services.get_pending_notifications)(20)
        for notification in notifications:
            try:
                from .keyboards import build_order_actions_keyboard

                await bot.send_message(
                    notification["chat_id"],
                    notification["message_text"],
                    reply_markup=build_order_actions_keyboard(
                        InlineKeyboardBuilder,
                        notification["order_id"],
                        notification["order_status"],
                    ),
                )
                await sync_to_async(services.mark_notification_sent)(notification["id"])
            except Exception as exc:  # pragma: no cover - runtime integration path
                logger.exception("Failed to send Telegram order notification %s", notification["id"])
                await sync_to_async(services.mark_notification_failed)(notification["id"], str(exc))
        await asyncio.sleep(interval)


async def run_bot():
    token = getattr(settings, "TELEGRAM_ORDER_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("TELEGRAM_ORDER_BOT_TOKEN is not configured.")

    from aiogram import Bot, Dispatcher
    from aiogram.client.default import DefaultBotProperties
    from aiogram.enums import ParseMode
    from aiogram.utils.keyboard import InlineKeyboardBuilder

    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher()
    dispatcher.include_router(build_router())

    worker_task = asyncio.create_task(notification_worker(bot, InlineKeyboardBuilder))
    try:
        await dispatcher.start_polling(bot)
    finally:
        worker_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await worker_task
        await bot.session.close()

