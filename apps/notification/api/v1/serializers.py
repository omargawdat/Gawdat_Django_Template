from rest_framework import serializers

from apps.notification.models.notification import Notification


class NotificationOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "notification_type", "title", "message_body", "booking"]
