# Telegram Order Bot

Отдельное приложение для Telegram-бота админов магазина.

Что умеет:
- уведомляет админов о новых заказах;
- показывает последние заказы;
- позволяет менять статус заказа из Telegram;
- работает только для привязанных `staff/superuser` пользователей.

Как запустить:
1. Установить `aiogram`
2. Добавить `TELEGRAM_ORDER_BOT_TOKEN` в `.env`
3. Создать в Django admin записи `Telegram admin links`
4. Запустить:

```bash
python3 manage.py run_telegram_order_bot
```

