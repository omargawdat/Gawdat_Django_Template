from rest_framework import serializers


class DeviceLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(
        required=True, help_text="JWT refresh token to invalidate"
    )
    registration_id = serializers.CharField(
        required=False, help_text="FCM registration ID of the device"
    )
