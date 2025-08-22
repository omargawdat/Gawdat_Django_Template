from constance import config
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.appInfo.api.info.serializers import AppInfoSerializer
from apps.appInfo.api.info.serializers import FAQSerializer
from apps.appInfo.models.app_info import AppInfo
from apps.appInfo.models.faq import FAQ


class SocialAccountsAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["AppInfo"],
        operation_id="getSocialAccounts",
        responses={200: "application/json"},
    )
    def get(self, request, *args, **kwargs):
        data = {
            "email": config.CONTACT_EMAIL,
            "phone_number": config.CONTACT_PHONE,
            "twitter": config.TWITTER_URL,
            "instagram": config.INSTAGRAM_URL,
            "tiktok": config.TIKTOK_URL,
            "website": config.WEBSITE_URL,
        }
        return Response(data)


class AppInfoAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["AppInfo"],
        operation_id="getAppInfo",
        responses={200: AppInfoSerializer},
    )
    def get(self, request, *args, **kwargs):
        app_info = AppInfo.get_solo()
        serializer = AppInfoSerializer(app_info)
        return Response(serializer.data)


class FAQListView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["AppInfo"],
        operation_id="listFaqs",
        responses={200: FAQSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        queryset = FAQ.objects.all()
        serializer = FAQSerializer(queryset, many=True)
        return Response(serializer.data)
