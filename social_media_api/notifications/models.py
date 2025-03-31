from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

CustomUser = get_user_model()


class Notification(models.Model):
    NOTIFIACTION_VERBS = [
        ('like', 'Like'),
        ('comment', 'Comment')
    ]
    recipient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='notifications')
    verb = models.CharField(max_length=100, choices=NOTIFIACTION_VERBS)
    target_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE)
    target_object_id = models.PositiveBigIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')
    timestamp = models.DateTimeField(auto_now_add=True)
