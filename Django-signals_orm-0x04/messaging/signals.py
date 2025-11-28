from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance: Message, created, **kwargs):
    """
    When a new Message is created, create a Notification for the receiver.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            title=f"New message from {instance.sender}",
            body=(instance.content[:200] if instance.content else ""),
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance: Message, **kwargs):
    """
    Before saving a Message, if it exists in DB and content changed, store previous content.
    Also set edited flag to True.
    """
    if not instance.pk:
        # New message — nothing to save
        return

    try:
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # If content changed, log history
    if old.content != instance.content:
        MessageHistory.objects.create(
            message=old,
            old_content=old.content,
            edited_at=timezone.now(),
            edited_by=getattr(instance, '_editing_user', None)  # optional helper set in view
        )
        instance.edited = True


@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def cleanup_user_related_data(sender, instance, **kwargs):
    """
    When a User is deleted, clean up related messages, notifications, and histories.
    With CASCADE on foreign keys, much of this is automatic — this signal ensures cleanup
    or allows custom cascade behavior.
    """
    # Delete notifications where user was receiver
    Notification.objects.filter(user=instance).delete()

    # Delete messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete message histories referencing deleted messages (cascade should have handled it)
    MessageHistory.objects.filter(edited_by=instance).delete()
