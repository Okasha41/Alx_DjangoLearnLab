from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
from accounts.models import CustomeUserModel
from .models import Like, Comment


@receiver(post_save, sender=Comment)
def create_comment_notifiaction(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.post.author,
            actor=instance.user,
            verb='comment',
            target_content_type=ContentType.objects.get_for_model(
                instance.post),
            target_object_id=instance.post.id
        )


@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.post.author,
            actor=instance.user,
            verb='like',
            target_content_type=ContentType.objects.get_for_model(
                instance.post),
            target_object_id=instance.post.id
        )
