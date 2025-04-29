from rest_framework import serializers

from apps.channel.models.notification import Notification


class NotificationMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "notification_type",
            "title",
            "message_body",
            "created_at",
        ]


class NotificationDetailedSerializer(NotificationMinimalSerializer):
    class Meta(NotificationMinimalSerializer.Meta):
        fields = NotificationMinimalSerializer.Meta.fields


class FCMDeviceCreateSerializer(serializers.Serializer):
    registration_id = serializers.CharField()
    device_id = serializers.CharField()
    type = serializers.ChoiceField(
        choices=["android", "ios", "web"],
        default="android",
    )
