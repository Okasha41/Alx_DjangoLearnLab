from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    model = Notification
    fields = ['id', 'recipient', 'verb', 'target', 'timestamp']
