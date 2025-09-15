from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.appInfo.api.info.serializers import AppInfoSerializer
from apps.appInfo.api.info.serializers import ContactUsSerializer
from apps.appInfo.api.info.serializers import FAQSerializer
from apps.appInfo.api.info.serializers import SocialAccountsSerializer
from apps.appInfo.models.app_info import AppInfo
from apps.appInfo.models.contact_us import ContactUs
from apps.appInfo.models.faq import FAQ
from apps.appInfo.models.social import SocialAccount


class SocialAccountsAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["AppInfo"],
        operation_id="ContactUs",
        request={
            "application/json": ContactUsSerializer,
        },
        examples=[
            OpenApiExample(
                name="Contact Us Example",
                value={
                    "contactType": "GENERAL",
                    "description": "I love using your app!",
                },
                request_only=True,
            )
        ],
        responses={201: ContactUsSerializer},
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


class ContactUsCreateView(CreateAPIView):
    serializer_class = ContactUsSerializer
    queryset = ContactUs.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        tags=["AppInfo"],
        operation_id="ContactUs",
        request={
            "application/json": ContactUsSerializer,
        },
        responses={201: ContactUsSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
