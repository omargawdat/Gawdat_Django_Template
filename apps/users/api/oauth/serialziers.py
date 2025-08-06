from dj_rest_auth.registration.serializers import SocialLoginSerializer
from rest_framework import serializers


class GoogleIDTokenSerializer(SocialLoginSerializer):
    id_token = serializers.CharField(required=True)

    def validate(self, attrs):
        attrs["access_token"] = attrs.get("id_token")
        return super().validate(attrs)


class FacebookAccessTokenSerializer(SocialLoginSerializer):
    access_token = serializers.CharField(required=True, trim_whitespace=True)

    def validate(self, attrs):
        return super().validate(attrs)
