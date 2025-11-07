from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from apps.channel.api.notification.serializers import FCMDeviceCreateSerializer
from apps.channel.constants import Language
from apps.location.api.country.serializers import CountrySerializer
from apps.location.models.country import Country
from apps.payment.api.wallet.serializers import WalletMinimalSerializer
from apps.users.models.customer import Customer


class CustomerMinimalSerializer(serializers.ModelSerializer):
    # Since user is primary_key, pk will be the user_id
    id = serializers.IntegerField(source="pk", read_only=True)

    class Meta:
        model = Customer
        fields = [
            "id",
            "full_name",
            "image",
            "gender",
            "birth_date",
            "primary_address",
            "is_profile_completed",
        ]


class CustomerDetailedSerializer(CustomerMinimalSerializer):
    # Customer-specific fields
    country = CountrySerializer(read_only=True)
    wallet = WalletMinimalSerializer(source="user.wallet", read_only=True)

    class Meta(CustomerMinimalSerializer.Meta):
        fields = [
            # User auth fields (via proxy properties)
            "id",
            "email",
            "language",
            "date_joined",
            # Customer profile fields
            "full_name",
            "image",
            "gender",
            "birth_date",
            "primary_address",
            "is_profile_completed",
            "country",
            "wallet",
        ]


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Update Customer Profile",
            value={
                "full_name": "John Doe",
                "gender": "male",
                "birth_date": "1990-01-01",
                "primary_address": 1,
                "language": "en",
                "country": 1,
            },
            request_only=True,
        ),
    ]
)
class CustomerUpdateSerializer(serializers.ModelSerializer):
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.filter(is_active=True),
        required=False,
    )
    language = serializers.ChoiceField(choices=Language.choices, required=False)

    class Meta:
        model = Customer
        fields = [
            "full_name",
            "image",
            "birth_date",
            "primary_address",
            "gender",
            "language",
            "country",
        ]

    def update(self, instance, validated_data):
        # Handle User fields
        language = validated_data.pop("language", None)

        if language:
            instance.user.language = language
            instance.user.save()

        # Handle Customer fields
        return super().update(instance, validated_data)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Complete Customer Profile",
            value={
                "country": "SA",
                "language": "ar",
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
class CustomerSetupSerializer(serializers.Serializer):
    """Complete Customer profile after signup."""

    # User fields
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
