from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.appInfo.api.info.serializers import AppInfoSerializer
from apps.appInfo.api.info.serializers import ContactUsSerializer
from apps.appInfo.api.info.serializers import FAQSerializer
from apps.appInfo.api.info.serializers import OnBoardingSerializer
from apps.appInfo.api.info.serializers import SocialAccountsSerializer
from apps.appInfo.models.app_info import AppInfo
from apps.appInfo.models.contact_us import ContactUs
from apps.appInfo.models.faq import FAQ
from apps.appInfo.models.onboarding import Onboarding
from apps.appInfo.models.social import SocialAccount
from apps.appInfo.other.constants import ContactCategory


class SocialAccountsAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["AppInfo/SocialMedia"],
        operation_id="GetSocialMedia",
        responses={
            200: SocialAccountsSerializer,
        },
        description="Retrieve social media and contact information.",
    )
    def get(self, request, *args, **kwargs):
        social_media = SocialAccount.get_solo()
        serializer = SocialAccountsSerializer(social_media)
        return Response(serializer.data)


class AppInfoAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["AppInfo/Info"],
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
        tags=["AppInfo/FAQ"],
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

    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        tags=["Communications/ContactUs"],
        operation_id="CreateContactUs",
        request={
            "application/json": ContactUsSerializer,
        },
        responses={201: ContactUsSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(customer=self.request.user)
        else:
            serializer.save(customer=None)


class ContactUsTypesListAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        tags=["Communications/ContactUs"],
        operation_id="listContactUsTypes",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "contact_types": {"type": "array", "items": {"type": "string"}}
                },
            }
        },
        description="Retrieve available contact us category types.",
    )
    def get(self, request):
        contact_types = list(ContactCategory)
        return Response({"contact_types": contact_types}, status=status.HTTP_200_OK)


class OnboardingAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["AppInfo/Onboarding"],
        operation_id="listOnboarding",
        responses={200: OnBoardingSerializer(many=True)},
        description="Retrieve active onboarding screens",
    )
    def get(self, request):
        onboardings = Onboarding.objects.filter(is_active=True)
        onboarding_serializer = OnBoardingSerializer(
            onboardings, many=True, context={"request": request}
        ).data
        return Response(onboarding_serializer, status=status.HTTP_200_OK)
