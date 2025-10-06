from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from apps.channel.api.notification.serializers import FCMDeviceCreateSerializer
from apps.channel.constants import Language
from apps.location.api.country.serializers import CountrySerializer
from apps.location.models.country import Country
from apps.payment.api.wallet.serializers import WalletMinimalSerializer
from apps.users.api.serializer_validations import ValidCountryPhoneNumberField
from apps.users.models.customer import Customer


class CustomerMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "phone_number",
            "full_name",
            "email",
            "image",
            "gender",
            "birth_date",
            "primary_address",
            "is_profile_completed",
            "language",
        ]


class CustomerDetailedSerializer(CustomerMinimalSerializer):
    country = CountrySerializer(read_only=True)
    wallet = WalletMinimalSerializer(read_only=True)

    class Meta(CustomerMinimalSerializer.Meta):
        fields = [
            *CustomerMinimalSerializer.Meta.fields,
            "country",
            "wallet",
        ]


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Customer Authentication Example",
            value={
                "phone_number": "+966111111111",
                "otp": "00000",
                "device": {
                    "registration_id": "your_registration_id",
                    "device_id": "your_device_id",
                    "type": "android",
                },
                "language": "en",
                "country": "SA",
            },
            request_only=True,
        ),
    ]
)
class CustomerCreateSerializer(serializers.Serializer):
    phone_number = ValidCountryPhoneNumberField()
    otp = serializers.CharField()
    device = FCMDeviceCreateSerializer(required=False, allow_null=True)
    language = serializers.ChoiceField(choices=Language.choices)
    referral_customer_id = serializers.IntegerField(required=False, allow_null=True)
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.filter(is_active=True),
        required=True,
    )


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Update Customer Profile",
            value={
                "full_name": "John Doe",
                "email": "john.doe@example.com",
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

    class Meta:
        model = Customer
        fields = [
            "full_name",
            "image",
            "birth_date",
            "primary_address",
            "email",
            "gender",
            "language",
            "country",
        ]
