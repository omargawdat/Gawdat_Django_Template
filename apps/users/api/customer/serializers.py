from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from apps.users.domain.validators.phone import PhoneValidator
from apps.users.models import MobileUser
from apps.users.models.customer import Customer


class BaseUserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MobileUser
        fields = ["phone_number", "password", "full_name", "email"]

    def validate_phone_number(self, value):
        if not PhoneValidator.is_phone_in_working_country(value):
            raise serializers.ValidationError("Phone number is not from an accepted country")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages[0]) from e
        return value


class CustomerRegisterSerializer(BaseUserRegisterSerializer):
    class Meta(BaseUserRegisterSerializer.Meta):
        model = Customer
        fields = BaseUserRegisterSerializer.Meta.fields

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return Customer.objects.create(**validated_data)


class CustomerLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)


class CustomerOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "phone_number",
            "is_phone_verified",
            "full_name",
            "image",
            "birthday",
            "gender",
            "is_active",
            "email",
        ]


class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["full_name", "image", "birthday", "gender", "email"]
