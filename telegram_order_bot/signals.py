from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order

from .services import queue_new_order_notifications


@receiver(post_save, sender=Order)
def enqueue_order_notification(sender, instance, created, **kwargs):
    if not created:
        return
    transaction.on_commit(lambda: queue_new_order_notifications(instance.pk))

