from rest_framework import serializers

from apps.appInfo.models.app_info import AppInfo
from apps.appInfo.models.faq import FAQ


class AppInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppInfo
        fields = ["about_us", "terms", "policy"]


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ["question", "answer"]
