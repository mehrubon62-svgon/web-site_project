from telegram_order_bot.services import STATUS_LABELS_RU


def build_main_menu_keyboard(ReplyKeyboardMarkup, KeyboardButton):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Заказы"), KeyboardButton(text="🆔 Кто я")],
            [KeyboardButton(text="🔄 Обновить")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие 👇",
    )


def build_orders_list_keyboard(InlineKeyboardBuilder, orders: list[dict]):
    builder = InlineKeyboardBuilder()
    for order in orders:
        builder.button(
            text=f"#{order['id']} • {order['status_badge']} • {order['total_price']}",
            callback_data=f"order:show:{order['id']}",
        )
    builder.button(text="Обновить заказы", callback_data="orders:list")
    builder.adjust(1)
    return builder.as_markup()


def build_order_actions_keyboard(InlineKeyboardBuilder, order_id: int, current_status: str):
    builder = InlineKeyboardBuilder()
    for status, label in STATUS_LABELS_RU.items():
        prefix = "✓ " if status == current_status else ""
        builder.button(
            text=f"{prefix}{label}",
            callback_data=f"order:set:{order_id}:{status}",
        )
    builder.button(text="К списку заказов", callback_data="orders:list")
    builder.adjust(2, 2, 1, 1)
    return builder.as_markup()
