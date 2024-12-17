from rest_framework import serializers

from apps.appInfo.models.about import AboutUs
from apps.appInfo.models.social import SocialAccount
from apps.appInfo.models.terms import TermsAndConditions


class SocialAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ["email", "phone_number", "instagram", "tiktok", "website"]


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ["content_en", "content_ar"]


class TermsAndConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndConditions
        fields = ["content_en", "content_ar"]
