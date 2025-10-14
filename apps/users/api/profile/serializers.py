"""Serializers for customer profile completion flow."""

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from apps.channel.api.notification.serializers import FCMDeviceCreateSerializer
from apps.channel.constants import Language
from apps.location.models.country import Country
from apps.users.api.serializer_validations import ValidCountryPhoneNumberField


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Complete Customer Profile",
            value={
                "country": "SA",
                "language": "ar",
                "phone_number": "+966555555555",
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
class CustomerProfileCompletionSerializer(serializers.Serializer):
    """
    Complete Customer profile after signup.

    Step 2 of registration:
    1. User signs up via allauth (email + password)
    2. User completes Customer profile here
    """

    # User fields
    phone_number = ValidCountryPhoneNumberField(
        required=False,
        allow_null=True,
        help_text=_("Phone number with country code (e.g., +966555555555)"),
    )
    language = serializers.ChoiceField(
        choices=Language.choices,
        required=False,
        help_text=_("Preferred language"),
    )

    # Customer profile fields
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.filter(is_active=True),
        required=True,
        help_text=_("Country for the customer"),
    )

    # Optional device registration
    device = FCMDeviceCreateSerializer(required=False, allow_null=True)
