from rest_framework.generics import ListAPIView
from rest_framework import permissions
from .models import Notification
from .serializers import NotificationSerializer


class ListNotifications(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Notification.objects.filter(user=user)
        return queryset
