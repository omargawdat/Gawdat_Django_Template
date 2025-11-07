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
            "language",
            "customer",
        ]


class ProviderProfileNestedSerializer(serializers.Serializer):
    """Nested provider profile data."""

    id = serializers.IntegerField(read_only=True)
    company_name = serializers.CharField(read_only=True)


class UserWithProviderProfileSerializer(serializers.ModelSerializer):
    """User serializer with nested provider profile."""

    provider = ProviderProfileNestedSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "language",
            "provider",
        ]


class CheckEmailSerializer(serializers.Serializer):
    """Check if user exists by email."""

    email = serializers.EmailField(required=True)


class EmailExistsResponseSerializer(serializers.Serializer):
    """Response for email existence check."""

    exists = serializers.BooleanField()
    email = serializers.EmailField()
