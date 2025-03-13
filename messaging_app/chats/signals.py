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
    if instance.pk:
        # Get the original message object
        original_message = Message.objects.get(pk=instance.pk)
        
        # Check if the content has changed
        if original_message.content != instance.content:
            # Log the old message content before it is updated
            MessageHistory.objects.create(
                message=instance,
                old_content=original_message.content
            )
            # Mark the message as edited
            instance.edited = True
