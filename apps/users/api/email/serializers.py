from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from apps.users.models.customer import Customer


class CheckEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)
    phone_number = PhoneNumberField(required=True)

    class Meta:
        model = Customer
        fields = [
            "email",
            "phone_number",
            "password",
        ]


class VerifyCustomerEmailSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True, max_length=5)
