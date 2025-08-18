from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from djangorestframework_camel_case.parser import CamelCaseJSONParser
from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView

from apps.channel.domain.services.email_otp import GenerateOTP
from apps.users.api.user.serializers import DeviceLogoutSerializer
from apps.users.domain.services.user import UserServices
from apps.users.models.user import User
from config.helpers.env import env


@extend_schema(
    tags=["User/Common"],
)
class DocumentedTokenRefreshView(TokenRefreshView):
    pass


class LogoutAllDevicesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["User/Common"],
        operation_id="logoutAllDevices",
        description="Log out the current user from all devices by invalidating their refresh tokens.",
        request=None,
        responses={
            204: OpenApiResponse(
                description="Successfully logged out from all devices"
            ),
            401: OpenApiResponse(
                description="Authentication credentials were not provided or are invalid"
            ),
        },
    )
    def post(self, request):
        user = request.user
        UserServices.user_logout_all_devices(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogoutDeviceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [CamelCaseJSONParser]

    @extend_schema(
        tags=["User/Common"],
        operation_id="logoutDevice",
        request=DeviceLogoutSerializer,
        responses={
            204: OpenApiResponse(description="Successfully logged out from the device"),
            401: OpenApiResponse(
                description="Authentication credentials were not provided or are invalid"
            ),
        },
    )
    def post(self, request):
        serializer = DeviceLogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        UserServices.user_logout_specific_device(
            user=request.user,
            refresh_token=serializer.validated_data["refresh_token"],
            registration_id=serializer.validated_data["registration_id"],
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class SendOTPView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["User/Common"],
        operation_id="sendOTP",
        description="Send OTP verification code to user's email",
        responses={
            200: OpenApiResponse(description="Verification code sent to email"),
        },
    )
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Email Not Found!"}, status=200)

        # Generate OTP and store in session
        expiry_minutes = 10
        otp = GenerateOTP.generate_otp()
        GenerateOTP.store_otp_in_session(
            request.session, email, otp, expiry_minutes=expiry_minutes
        )

        # Prepare context for email template
        context = {
            "otp_code": otp,
            "expiry_minutes": expiry_minutes,
            "email": email,
            "user": user,
        }

        # Render HTML email template
        html_message = render_to_string("account/email/verification_otp.html", context)

        # Send email with HTML content
        email_message = EmailMessage(
            subject="Your Verification Code",
            body=html_message,
            from_email=f"Support <no-reply@{env.domain_name}>",
            to=[email],
        )
        email_message.content_subtype = "html"
        email_message.send()

        return Response({"detail": "Verification code sent to your email"}, status=200)


class SetPasswordView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        new_password = request.data.get("new_password")

        if not email or not otp or not new_password:
            return Response(
                {"error": "Missing data"}, status=status.HTTP_400_BAD_REQUEST
            )

        is_valid, message = GenerateOTP.validate_otp(request.session, email, otp)
        if not is_valid:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email=email)
        user.set_password(new_password)
        user.save()

        request.session.pop("otp_data", None)
        request.session.modified = True

        return Response({"detail": "Password changed successfully"}, status=200)
