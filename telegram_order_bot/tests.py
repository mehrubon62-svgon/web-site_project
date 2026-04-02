from django.test import TestCase

from my_site_register.models import UniqUser
from orders.models import Order

from .models import TelegramAdminLink, TelegramOrderNotification
from .services import get_authorized_admin_link, set_order_status


class TelegramOrderBotTests(TestCase):
    def setUp(self):
        self.admin_user = UniqUser.objects.create_user(
            username="admin_user",
            password="pass12345",
            is_staff=True,
            email="admin@example.com",
        )
        self.regular_user = UniqUser.objects.create_user(
            username="customer_user",
            password="pass12345",
            email="customer@example.com",
        )
        self.admin_link = TelegramAdminLink.objects.create(
            user=self.admin_user,
            telegram_user_id=111111111,
            telegram_chat_id=111111111,
        )

    def create_order(self):
        return Order.objects.create(
            user=self.regular_user,
            status="PENDING",
            total_price="1499.99",
            full_name="John Smith",
            phone="+992900000000",
            email="john@example.com",
            address="Dushanbe, Rudaki 10",
            comment="Leave at the reception",
        )

    def test_only_staff_link_is_authorized(self):
        self.assertIsNotNone(get_authorized_admin_link(self.admin_link.telegram_user_id))

        outsider = UniqUser.objects.create_user(
            username="outsider",
            password="pass12345",
            email="outsider@example.com",
        )
        unauthorized_link = TelegramAdminLink.objects.create(
            user=outsider,
            telegram_user_id=222222222,
            telegram_chat_id=222222222,
        )
        self.assertIsNone(get_authorized_admin_link(unauthorized_link.telegram_user_id))

    def test_new_order_signal_creates_notification_for_active_admin(self):
        with self.captureOnCommitCallbacks(execute=True):
            order = self.create_order()

        notification = TelegramOrderNotification.objects.get(order=order, admin_link=self.admin_link)
        self.assertEqual(notification.delivery_status, TelegramOrderNotification.STATUS_PENDING)
        self.assertIn("Новый заказ", notification.message_text)

    def test_status_update_changes_order(self):
        order = self.create_order()

        result = set_order_status(order.id, "SHIPPED")

        self.assertTrue(result["ok"])
        self.assertTrue(result["changed"])
        order.refresh_from_db()
        self.assertEqual(order.status, "SHIPPED")
