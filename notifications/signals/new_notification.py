from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import Notification
from ..tasks import notificate_user_by_ws

@receiver(post_save, sender=Notification)
def new_notification(sender, instance, created, **kwargs):
    if created:
        notificate_user_by_ws.delay(
            user_id=instance.to_user.id,
            message=instance.message,
            event=instance.event,
        )
