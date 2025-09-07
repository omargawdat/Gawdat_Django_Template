from datetime import timedelta

from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from apps.users.api.customer.serializers import CustomerDetailedSerializer
from apps.users.api.email.serializers import CheckEmailSerializer
from apps.users.api.email.serializers import RegisterSerializer
from apps.users.api.email.serializers import VerifyCustomerEmailSerializer
from apps.users.domain.selectors.customer import CustomerSelector
from apps.users.domain.services.customer import CustomerService
from apps.users.domain.services.email import EmailService
from apps.users.domain.services.token import TokenService
from apps.users.domain.utilities.otp import OTPUtility
from apps.users.models.customer import Customer
from config.settings.base import OTP_EMAIL_SECONDS


class CheckEmailView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CheckEmailSerializer

    @extend_schema(
        tags=["User/Email"],
        operation_id="checkEmail",
        description="Check if an email is registered, verified, and has a password set.",
        request=CheckEmailSerializer,
        responses={
            200: OpenApiResponse(
                description="Email is registered",
                response={
                    "properties": {
                        "is_registered": {"type": "boolean", "example": True},
                        "is_verified": {"type": "boolean", "example": True},
                        "has_password": {"type": "boolean", "example": True},
                    }
                },
            ),
            404: OpenApiResponse(
                description="Email is not registered",
                response={
                    "properties": {
                        "is_registered": {"type": "boolean", "example": False},
                        "is_verified": {"type": "boolean", "example": False},
                        "has_password": {"type": "boolean", "example": False},
                    }
                },
            ),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            customer = Customer.objects.get(email=email)
            return Response(
                {
                    "is_registered": True,
                    "is_verified": customer.is_verified,
                    "has_password": bool(customer.password),
                },
                status=status.HTTP_200_OK,
            )

        except Customer.DoesNotExist:
            return Response(
                {"is_registered": False, "is_verified": False, "has_password": False},
                status=status.HTTP_404_NOT_FOUND,
            )


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterSerializer

    @extend_schema(
        tags=["User/Email"],
        operation_id="registerUser",
        description="Register a new user with email, phone number, and password.",
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(
                description="User registered successfully",
                response={
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "User registered successfully.",
                        }
                    }
                },
            ),
            400: OpenApiResponse(
                description="Email is already registered",
                response={
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Email is already registered.",
                        }
                    }
                },
            ),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        username = email.split("@")[0]
        phone_number = serializer.validated_data["phone_number"]
        password = serializer.validated_data["password"]

        if CustomerSelector.is_email_exists(email=email):
            return Response(
                {"detail": "Email is already registered."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create customer service
        customer = CustomerService.create_customer(
            email=email,
            username=username,
            phone_number=phone_number,
            password=password,
        )

        # Generate OTP then Send Email

        otp = OTPUtility.generate_otp()
        expires_at = timezone.now() + timedelta(seconds=OTP_EMAIL_SECONDS)

        cache.set(
            f"otp_{email}",
            {"otp": otp, "attempts": 0, "expires_at": expires_at.isoformat()},
            timeout=OTP_EMAIL_SECONDS,
        )

        email_send = EmailService()
        email_send.send_email(
            subject="Verify your account - 1K Coffee",
            message=f"Your OTP is {otp}",
            recipient_list=[email],
            template_name="emails/verify_email.html",
            context={"user": email, "otp_code": otp, "expires_at": expires_at},
        )

        tokens_data = TokenService.generate_token_for_user(customer)
        customer_detail = CustomerDetailedSerializer(
            customer, context={"request": request}
        )
        return Response(
            {
                "is_verified": customer.is_verified,
                "access": tokens_data.access,
                "refresh": tokens_data.refresh,
                "customer": customer_detail.data,
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyCustomerEmailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VerifyCustomerEmailSerializer

    @extend_schema(
        tags=["User/Email"],
        operation_id="verifyCustomerEmail",
        description="Verify a customer's email using an OTP code.",
        request=VerifyCustomerEmailSerializer,
        responses={
            200: OpenApiResponse(
                description="Email verified successfully",
                response={
                    "properties": {
                        "is_verified": {"type": "boolean", "example": True},
                        "access": {
                            "type": "string",
                            "example": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        },
                        "refresh": {
                            "type": "string",
                            "example": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        },
                        "customer": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "email": {
                                    "type": "string",
                                    "example": "user@example.com",
                                },
                                "username": {"type": "string", "example": "user"},
                                "phone_number": {
                                    "type": "string",
                                    "example": "1234567890",
                                },
                                "is_verified": {"type": "boolean", "example": True},
                            },
                        },
                    }
                },
            ),
            400: OpenApiResponse(
                description="Invalid OTP",
                response={
                    "properties": {
                        "error": {
                            "type": "string",
                            "example": "Invalid OTP or OTP has expired",
                        }
                    }
                },
            ),
            401: OpenApiResponse(
                description="Invalid token",
                response={
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Invalid or expired token.",
                        }
                    }
                },
            ),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp_code = serializer.validated_data["otp"]
        access_token = request.headers.get("Authorization").split(" ")[1]

        try:
            token = AccessToken(access_token)
            user_id = token.get("user_id")
            customer = Customer.objects.get(id=user_id)
        except (TokenError, Customer.DoesNotExist, AttributeError, IndexError):
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        customer = get_object_or_404(Customer, id=user_id)

        try:
            OTPUtility.verify_or_bust(customer.email, otp_code)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not customer.is_verified:
            customer.is_verified = True
            customer.save(update_fields=["is_verified"])

        tokens_data = TokenService.generate_token_for_user(customer)

        customer_serializer = CustomerDetailedSerializer(
            customer, context={"request": request}
        )
        return Response(
            {
                "is_verified": True,
                "access": tokens_data.access,
                "refresh": tokens_data.refresh,
                "customer": customer_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
