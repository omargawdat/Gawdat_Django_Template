from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from apps.users.api.customer.serializers import BaseUserRegisterSerializer
from apps.users.models.provider import Provider


class ProviderRegisterSerializer(BaseUserRegisterSerializer):
    class Meta(BaseUserRegisterSerializer.Meta):
        model = Provider
        fields = BaseUserRegisterSerializer.Meta.fields

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])

        return Provider.objects.create(**validated_data)


class ProviderLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ProviderOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
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


class ProviderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ["full_name", "image", "birthday", "gender", "email"]
