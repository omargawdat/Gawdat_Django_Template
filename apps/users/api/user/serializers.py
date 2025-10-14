from rest_framework import serializers

from apps.users.models.user import User


class CustomerProfileNestedSerializer(serializers.Serializer):
    """Nested customer profile data."""

    id = serializers.IntegerField(read_only=True)
    country = serializers.CharField(source="country.name", read_only=True)
    country_code = serializers.CharField(source="country.code", read_only=True)


class UserWithProfileSerializer(serializers.ModelSerializer):
    """User serializer with nested customer profile."""

    customer = CustomerProfileNestedSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "phone_number",
            "language",
            "customer",
        ]


class DeviceLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(
        required=True, help_text="JWT refresh token to invalidate"
    )
    registration_id = serializers.CharField(
        required=False, help_text="FCM registration ID of the device"
    )
