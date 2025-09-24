from datetime import timedelta

from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from apps.appInfo.models.social import SocialAccount
from apps.users.api.customer.serializers import CustomerDetailedSerializer
from apps.users.api.email.serializers import ChangePasswordSerializer
from apps.users.api.email.serializers import CheckEmailSerializer
from apps.users.api.email.serializers import LoginSerializer
from apps.users.api.email.serializers import RegisterSerializer
from apps.users.api.email.serializers import VerifyCustomerEmailSerializer
from apps.users.domain.selectors.customer import CustomerSelector
from apps.users.domain.services.customer import CustomerService
from apps.users.domain.services.email import EmailService
from apps.users.domain.services.token import TokenService
from apps.users.domain.utilities.otp import OTPUtility
from apps.users.domain.validators.customer import CustomerValidator
from apps.users.models.customer import Customer
from config.helpers.env import env
from config.settings.base import OTP_EMAIL_SECONDS


class CheckEmailView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CheckEmailSerializer

    @extend_schema(
        tags=["User/Authentication/Mail"],
        operation_id="checkEmail",
        description="Check if an email is registered, verified, and has a password set.",
        request={"application/json": CheckEmailSerializer},
        responses={
            200: inline_serializer(
                name="CheckEmailResponse",
                fields={
                    "is_registered": serializers.BooleanField(),
                    "is_verified": serializers.BooleanField(),
                    "has_password": serializers.BooleanField(),
                },
            )
        },
        examples=[
            OpenApiExample(
                name="Registered user",
                description="An email that exists in the system",
                value={"email": "user@gmail.com"},
                request_only=True,
                media_type="application/json",
            ),
            OpenApiExample(
                name="Unregistered user",
                description="An email that does not exist",
                value={"email": "nobody@gmail.com"},
                request_only=True,
                media_type="application/json",
            ),
        ],
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
        tags=["User/Authentication/Mail"],
        operation_id="registerUser",
        description="Register a new user with email, phone number, and password. Returns auth tokens and the customer profile.",
        request={"application/json": RegisterSerializer},
        examples=[
            OpenApiExample(
                name="Minimal registration",
                value={
                    "email": "user@example.com",
                    "password": "Str0ngP@ssw0rd!",  # pragma: allowlist secret
                },
                request_only=True,
                media_type="application/json",
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="RegisterResponse200",
                    fields={
                        "is_verified": serializers.BooleanField(),
                        "access": serializers.CharField(),
                        "refresh": serializers.CharField(),
                        "customer": CustomerDetailedSerializer(),
                    },
                )
            ),
            201: OpenApiResponse(
                response=inline_serializer(
                    name="RegisterResponse201",
                    fields={
                        "is_verified": serializers.BooleanField(),
                        "access": serializers.CharField(),
                        "refresh": serializers.CharField(),
                        "customer": CustomerDetailedSerializer(),
                    },
                )
            ),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        username = email.split("@")[0]
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
            subject="Verify your account - Dars App",
            message=f"Your OTP is {otp}",
            recipient_list=[email],
            template_name="emails/verify_email.html",
            context={
                "user": username,
                "otp_code": otp,
                "expires_at": expires_at,
                "app_name": env.domain_name,
                "social_links": SocialAccount.get_solo(),
            },
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
            status=status.HTTP_200_OK,
        )


class VerifyCustomerEmailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VerifyCustomerEmailSerializer

    @extend_schema(
        tags=["User/Authentication/Mail"],
        operation_id="verifyCustomerEmail",
        description="Verify a customer's email using an OTP code. Requires a valid Bearer access token.",
        request={"application/json": VerifyCustomerEmailSerializer},
        examples=[
            OpenApiExample(
                name="Valid OTP",
                value={"otp": "123456"},
                request_only=True,
                media_type="application/json",
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="VerifyCustomerEmailResponse",
                    fields={
                        "isVerified": serializers.BooleanField(),
                        "access": serializers.CharField(),
                        "refresh": serializers.CharField(),
                        "customer": CustomerDetailedSerializer(),
                    },
                )
            )
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


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer

    @extend_schema(
        tags=["User/Authentication/Mail"],
        operation_id="loginUser",
        description="Authenticate a user and return JWT tokens. If the email is not verified, an OTP is sent.",
        request={"application/json": LoginSerializer},
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="LoginResponse",
                    fields={
                        "isVerified": serializers.BooleanField(),
                        "access": serializers.CharField(),
                        "refresh": serializers.CharField(),
                        "customer": CustomerDetailedSerializer(),
                    },
                )
            )
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"].strip().lower()
        password = serializer.validated_data["password"]

        try:
            customer = CustomerValidator.authenticate(email=email, password=password)
        except ValueError:
            raise AuthenticationFailed("Invalid email or password.") from None

        tokens_data = TokenService.generate_token_for_user(customer)

        if not customer.is_verified:
            otp = OTPUtility.generate_otp()

            expires_at = timezone.now() + timedelta(seconds=OTP_EMAIL_SECONDS)
            cache.set(
                f"otp_{email}",
                {"otp": otp, "attempts": 0, "expires_at": expires_at.isoformat()},
                timeout=OTP_EMAIL_SECONDS,
            )

            EmailService().send_email(
                subject="Verify your account - E-Learning Platform",
                message=f"Your OTP is {otp}",
                recipient_list=[customer.email],
                template_name="emails/verify_email.html",
                context={
                    "user": customer.email,
                    "otp_code": otp,
                    "expires_at": expires_at,
                },
            )
            return Response(
                {
                    "message": "Email is not verified. An OTP has been sent to your email.",
                }
            )

        customer_data = CustomerDetailedSerializer(
            customer, context={"request": request}
        ).data
        return Response(
            {
                "is_verified": customer.is_verified,
                "access": tokens_data.access,
                "refresh": tokens_data.refresh,
                "customer": customer_data,
            },
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    @extend_schema(
        tags=["User/Authentication/Mail"],
        operation_id="changePassword",
        description="Change the password of an authenticated user. Requires a valid Bearer access token.",
        request={"application/json": ChangePasswordSerializer},
        responses={204: OpenApiResponse(description="Password changed successfully.")},
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]

        CustomerService.change_password(
            customer=user, old_password=old_password, new_password=new_password
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
