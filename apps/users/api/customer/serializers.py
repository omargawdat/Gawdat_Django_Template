from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from apps.channel.constants import Language
from apps.location.api.country.serializers import CountrySerializer
from apps.location.models.country import Country
from apps.payment.api.wallet.serializers import WalletMinimalSerializer
from apps.users.api.serializer_validations import ValidCountryPhoneNumberField
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
    country = CountrySerializer(read_only=True)
    # Wallet is on User, not Customer
    wallet = WalletMinimalSerializer(source="user.wallet", read_only=True)

    class Meta(CustomerMinimalSerializer.Meta):
        fields = [
            *CustomerMinimalSerializer.Meta.fields,
            "country",
            "wallet",
        ]


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
    email = serializers.EmailField(required=False)
    language = serializers.ChoiceField(choices=Language.choices, required=False)
    phone_number = ValidCountryPhoneNumberField(required=False)

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
            "phone_number",
        ]

    def update(self, instance, validated_data):
        # Handle User fields
        email = validated_data.pop("email", None)
        language = validated_data.pop("language", None)
        phone_number = validated_data.pop("phone_number", None)

        if email:
            instance.user.email = email
        if language:
            instance.user.language = language
        if phone_number:
            instance.user.phone_number = phone_number
        if email or language or phone_number:
            instance.user.save()

        # Handle Customer fields
        return super().update(instance, validated_data)
