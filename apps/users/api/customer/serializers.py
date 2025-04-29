from rest_framework import serializers

from apps.channel.api.notification.serializers import FCMDeviceCreateSerializer
from apps.channel.constants import Language
from apps.location.api.address.serializers import AddressMinimalSerializer
from apps.location.api.country.serializers import CountryMinimalSerializer
from apps.payment.api.wallet_transaction.serializers import WalletMinimalSerializer
from apps.users.api.common.serializer_validations import ValidCountryPhoneNumberField
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
    country = CountryMinimalSerializer(read_only=True)
    addresses = AddressMinimalSerializer(many=True, read_only=True)
    wallet = WalletMinimalSerializer(read_only=True)

    class Meta(CustomerMinimalSerializer.Meta):
        fields = [
            *CustomerMinimalSerializer.Meta.fields,
            "country",
            "addresses",
            "wallet",
        ]


class CustomerCreateSerializer(serializers.Serializer):
    phone_number = ValidCountryPhoneNumberField()
    otp = serializers.CharField()
    device = FCMDeviceCreateSerializer()
    language = serializers.ChoiceField(choices=Language.choices)


class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "full_name",
            "image",
            "birth_date",
            "primary_address",
            "email",
        ]
