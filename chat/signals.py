"""
Custom signals sent during the creation messages.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from chat.models import Message

# A new ad has created.
ad_created_or_updated = Signal(providing_args=["user", "advertisement", "request"])

# обработчик сохранения объекта сообщения
@receiver(post_save, sender=Message)
def post_save_message(sender, instance, created, **kwargs):
    # если объект был создан
    if created:
        # указываем чату, в котором находится данное сообщение, что это последнее сообщение
        instance.chat.last_send_message = instance
        # и обновляем данный внешний ключ чата
        instance.chat.save(update_fields=['last_send_message'])
