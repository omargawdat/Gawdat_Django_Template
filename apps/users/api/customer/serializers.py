from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from apps.channel.api.notification.serializers import FCMDeviceCreateSerializer
from apps.channel.constants import Language
from apps.location.api.address.serializers import AddressMinimalSerializer
from apps.location.api.country.serializers import CountryMinimalSerializer
from apps.location.domain.selector.address import AddressSelector
from apps.payment.api.wallet.serializers import WalletMinimalSerializer
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
    addresses = SerializerMethodField()
    wallet = WalletMinimalSerializer(read_only=True)

    class Meta(CustomerMinimalSerializer.Meta):
        fields = [
            *CustomerMinimalSerializer.Meta.fields,
            "country",
            "addresses",
            "wallet",
        ]

    def get_addresses(self, obj):
        addresses = AddressSelector.get_all_customer_addresses(customer=obj)
        return AddressMinimalSerializer(addresses, many=True).data


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
            "birth_date",
            "gender",
            "language",
        ]
