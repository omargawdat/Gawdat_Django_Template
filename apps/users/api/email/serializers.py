from rest_framework import serializers

from apps.users.models.customer import Customer


class CheckEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Customer
        fields = [
            "email",
            "password",
        ]


class VerifyCustomerEmailSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True, max_length=5)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
