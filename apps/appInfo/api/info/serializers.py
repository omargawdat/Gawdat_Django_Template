from rest_framework import serializers

from apps.appInfo.models.app_info import AppInfo
from apps.appInfo.models.contact_us import ContactUs
from apps.appInfo.models.faq import FAQ
from apps.appInfo.models.onboarding import Onboarding
from apps.appInfo.models.social import SocialAccount


class SocialAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ["email", "phone_number", "instagram", "tiktok", "website"]


class AppInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppInfo
        fields = ["about_us", "terms", "policy"]


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ["question", "answer"]


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ["contact_type", "description"]


class OnBoardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Onboarding
        fields = ["id", "title", "sub_text", "image"]
