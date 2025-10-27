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
            "language",
            "customer",
        ]
