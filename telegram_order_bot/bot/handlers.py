from __future__ import annotations

from asgiref.sync import sync_to_async

from telegram_order_bot import services


def build_router():
    from aiogram import F, Router
    from aiogram.filters import Command
    from aiogram.types import CallbackQuery, KeyboardButton, Message, ReplyKeyboardMarkup
    from aiogram.utils.keyboard import InlineKeyboardBuilder

    from .keyboards import (
        build_main_menu_keyboard,
        build_order_actions_keyboard,
        build_orders_list_keyboard,
    )

    router = Router(name="telegram_order_bot")

    async def ensure_admin(message_or_query):
        tg_user = message_or_query.from_user
        chat = message_or_query.message.chat if isinstance(message_or_query, CallbackQuery) else message_or_query.chat
        is_allowed = await sync_to_async(services.is_authorized_admin)(tg_user.id)
        if not is_allowed:
            text = services.build_link_hint_message(tg_user.id, chat.id if chat else None)
            if isinstance(message_or_query, CallbackQuery):
                await message_or_query.answer("⛔ Нет доступа", show_alert=True)
                await message_or_query.message.answer(text)
            else:
                await message_or_query.answer(text)
            return False

        await sync_to_async(services.touch_admin_presence)(
            tg_user.id,
            chat.id if chat else None,
            tg_user.username or "",
        )
        return True

    async def send_orders_list(target_message):
        orders = await sync_to_async(services.get_recent_orders)(10)
        if not orders:
            await target_message.answer(
                services.build_orders_list_message([]),
                reply_markup=build_main_menu_keyboard(ReplyKeyboardMarkup, KeyboardButton),
            )
            return
        await target_message.answer(
            services.build_orders_list_message(orders),
            reply_markup=build_main_menu_keyboard(ReplyKeyboardMarkup, KeyboardButton),
        )
        await target_message.answer(
            "⚡ Быстрые карточки заказов:",
            reply_markup=build_orders_list_keyboard(InlineKeyboardBuilder, orders),
        )

    @router.message(Command("start"))
    async def cmd_start(message: Message):
        if not await ensure_admin(message):
            return
        link = await sync_to_async(services.get_authorized_admin_link)(message.from_user.id)
        await message.answer(
            services.build_welcome_message(link),
            reply_markup=build_main_menu_keyboard(ReplyKeyboardMarkup, KeyboardButton),
        )
        await send_orders_list(message)

    @router.message(Command("whoami"))
    async def cmd_whoami(message: Message):
        link = await sync_to_async(services.get_authorized_admin_link)(message.from_user.id)
        if not link:
            await message.answer(
                services.build_link_hint_message(
                    message.from_user.id,
                    message.chat.id if message.chat else None,
                )
            )
            return
        await sync_to_async(services.touch_admin_presence)(
            message.from_user.id,
            message.chat.id if message.chat else None,
            message.from_user.username or "",
        )
        link = await sync_to_async(services.get_authorized_admin_link)(message.from_user.id)
        await message.answer(
            services.build_welcome_message(link),
            reply_markup=build_main_menu_keyboard(ReplyKeyboardMarkup, KeyboardButton),
        )

    @router.message(Command("orders"))
    async def cmd_orders(message: Message):
        if not await ensure_admin(message):
            return
        await send_orders_list(message)

    @router.message(F.text == "📦 Заказы")
    async def text_orders(message: Message):
        if not await ensure_admin(message):
            return
        await send_orders_list(message)

    @router.message(F.text == "🆔 Кто я")
    async def text_whoami(message: Message):
        await cmd_whoami(message)

    @router.message(F.text == "🔄 Обновить")
    async def text_refresh(message: Message):
        if not await ensure_admin(message):
            return
        link = await sync_to_async(services.get_authorized_admin_link)(message.from_user.id)
        await message.answer(
            services.build_welcome_message(link),
            reply_markup=build_main_menu_keyboard(ReplyKeyboardMarkup, KeyboardButton),
        )
        await send_orders_list(message)

    @router.callback_query(F.data == "orders:list")
    async def callback_orders_list(query: CallbackQuery):
        if not await ensure_admin(query):
            return
        orders = await sync_to_async(services.get_recent_orders)(10)
        await query.answer("🔄 Список обновлен")
        if not orders:
            await query.message.edit_text(services.build_orders_list_message([]))
            return
        await query.message.edit_text(
            services.build_orders_list_message(orders),
            reply_markup=build_orders_list_keyboard(InlineKeyboardBuilder, orders),
        )

    @router.callback_query(F.data.startswith("order:show:"))
    async def callback_order_show(query: CallbackQuery):
        if not await ensure_admin(query):
            return
        _, _, order_id_raw = query.data.split(":", 2)
        snapshot = await sync_to_async(services.get_order_snapshot)(int(order_id_raw))
        if not snapshot:
            await query.answer("❌ Заказ не найден", show_alert=True)
            return
        await query.answer(f"📦 Заказ #{snapshot['id']}")
        await query.message.edit_text(
            snapshot["message_text"],
            reply_markup=build_order_actions_keyboard(
                InlineKeyboardBuilder,
                snapshot["id"],
                snapshot["status"],
            ),
        )

    @router.callback_query(F.data.startswith("order:set:"))
    async def callback_order_set_status(query: CallbackQuery):
        if not await ensure_admin(query):
            return

        _, _, order_id_raw, status = query.data.split(":", 3)
        result = await sync_to_async(services.set_order_status)(int(order_id_raw), status)
        if not result["ok"]:
            await query.answer("❌ Не удалось обновить статус", show_alert=True)
            return

        if result["changed"]:
            await query.answer(f"✅ Статус обновлен: {result['status_label']}")
        else:
            await query.answer("ℹ️ Статус уже установлен")

        snapshot = await sync_to_async(services.get_order_snapshot)(result["order_id"])
        if not snapshot:
            await query.message.edit_text("❌ Заказ больше не найден.")
            return

        await query.message.edit_text(
            snapshot["message_text"],
            reply_markup=build_order_actions_keyboard(
                InlineKeyboardBuilder,
                snapshot["id"],
                snapshot["status"],
            ),
        )

    return router
