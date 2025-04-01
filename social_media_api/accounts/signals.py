from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import CustomeUserModel
from notifications.models import Notification


@receiver(m2m_changed, sender=CustomeUserModel.followers)
def create_follow_unfollow_notifiaction(sender, instance, action, reverse, pk_set, **kwargs):

    for user_id in pk_set:
        followed_user = CustomeUserModel.objects.get(pk=user_id)

        if action == "follow":  # User started following
            Notification.objects.create(
                recipient=followed_user,  # Notify the followed user
                actor=instance,  # The user who followed
                verb="follow",
                target_content_type=ContentType.objects.get_for_model(
                    instance),
                target_object_id=instance.id
            )

        elif action == "unfollow":  # User unfollowed
            Notification.objects.create(
                recipient=followed_user,  # Notify the unfollowed user
                actor=instance,  # The user who unfollowed
                verb="unfollow",
                target_content_type=ContentType.objects.get_for_model(
                    instance),
                target_object_id=instance.id
            )
