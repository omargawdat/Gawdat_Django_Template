from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from apps.users.domain.validators.phone import PhoneValidator


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()

    def validate_phone_number(self, value):
        if not PhoneValidator.is_phone_in_working_country(value):
            raise serializers.ValidationError("Phone number is not in working country")
        return value


class VerifyOtpSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    otp = serializers.CharField(max_length=4)

    def validate_phone_number(self, value):
        if not PhoneValidator.is_phone_in_working_country(value):
            raise serializers.ValidationError("Phone number is not in working country")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    reset_token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages[0]) from e
        return value
