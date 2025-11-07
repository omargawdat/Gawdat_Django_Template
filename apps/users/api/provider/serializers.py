from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from apps.channel.api.notification.serializers import FCMDeviceCreateSerializer
from apps.channel.constants import Language
from apps.users.models.provider import Provider


class ProviderMinimalSerializer(serializers.ModelSerializer):
    """Minimal provider serializer."""

    # Since user is primary_key, pk will be the user_id
    id = serializers.IntegerField(source="pk", read_only=True)

    class Meta:
        model = Provider
        fields = [
            "id",
            "company_name",
            "email",
            "date_joined",
        ]


class ProviderDetailedSerializer(ProviderMinimalSerializer):
    """Detailed provider serializer with all fields."""

    class Meta(ProviderMinimalSerializer.Meta):
        fields = [
            # User auth fields (via proxy properties)
            "id",
            "email",
            "language",
            "is_active",
            "date_joined",
            # Provider profile fields
            "company_name",
        ]


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Update Provider Profile",
            value={
                "company_name": "ACME Corporation",
                "language": "en",
            },
            request_only=True,
        ),
    ]
)
class ProviderUpdateSerializer(serializers.ModelSerializer):
    """Update provider profile."""

    language = serializers.ChoiceField(choices=Language.choices, required=False)

    class Meta:
        model = Provider
        fields = [
            "company_name",
            "language",
        ]

    def update(self, instance, validated_data):
        """Handle User fields and Provider fields."""
        # Handle User fields
        language = validated_data.pop("language", None)

        if language:
            instance.user.language = language
            instance.user.save()

        # Handle Provider fields
        return super().update(instance, validated_data)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Complete Provider Profile",
            value={
                "company_name": "ACME Corporation",
                "language": "en",
                "device": {
                    "registration_id": "firebase_token_here",
                    "device_id": "device_12345",
                    "type": "android",
                },
            },
            request_only=True,
        ),
    ]
)
class ProviderSetupSerializer(serializers.Serializer):
    """Complete Provider profile after signup."""

    # User fields
    language = serializers.ChoiceField(
        choices=Language.choices,
        required=False,
        help_text=_("Preferred language"),
    )

    # Provider profile fields
    company_name = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        help_text=_("Company name for the provider"),
    )

    # Optional device registration
    device = FCMDeviceCreateSerializer(required=False, allow_null=True)
