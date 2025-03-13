from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Creates a notification when a new message is sent.
    """
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)



@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    # Check if the message content is changing and that the message is being edited (edited field is True)
    if instance.pk:
        original_message = Message.objects.get(pk=instance.pk)
        if original_message.content != instance.content:
            # Log the old message content before the edit
            MessageHistory.objects.create(
                message=instance,
                old_content=original_message.content
            )
            # Mark the message as edited
            instance.edited = True
