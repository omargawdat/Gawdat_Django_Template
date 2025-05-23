from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.appInfo.api.info.serializers import AppInfoSerializer
from apps.appInfo.api.info.serializers import FAQSerializer
from apps.appInfo.api.info.serializers import SocialAccountsSerializer
from apps.appInfo.models.app_info import AppInfo
from apps.appInfo.models.faq import FAQ
from apps.appInfo.models.social import SocialAccount


class SocialAccountsAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["AppInfo"],
        operation_id="getSocialAccounts",
        responses={200: SocialAccountsSerializer},
    )
    def get(self, request, *args, **kwargs):
        social_media = SocialAccount.get_solo()
        serializer = SocialAccountsSerializer(social_media)
        return Response(serializer.data)


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
