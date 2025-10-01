from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.channel.constants import OTPType
from apps.channel.domain.services.device import DeviceData
from apps.channel.domain.services.device import DeviceService
from apps.channel.domain.services.otp import OTPUtils
from apps.users.api.customer.serializers import CustomerCreateSerializer
from apps.users.api.customer.serializers import CustomerDetailedSerializer
from apps.users.api.customer.serializers import CustomerUpdateSerializer
from apps.users.domain.selectors.customer import CustomerSelector
from apps.users.domain.services.customer import CustomerService
from apps.users.domain.services.token import TokenService
from apps.users.domain.services.user import UserServices


class CustomerAuthView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["User/Auhthentication/PhoneNumber"],
        operation_id="AuthenticateCustomer",
        parameters=[
            OpenApiParameter(
                name="Accept-Language",
                type=OpenApiTypes.STR,
                location="header",
                required=False,
                description="Language preference for the response",
                examples=[
                    OpenApiExample(
                        name="English (US)",
                        value="en",
                        description="English with US locale preference",
                    ),
                ],
            ),
        ],
        request={"application/json": CustomerCreateSerializer},
        examples=[
            OpenApiExample(
                name="Authenticate Customer",
                description="Update all profile fields including image",
                value={
                    "phone_number": "+966511111133",
                    "otp": "00000",
                    "device": {
                        "registrationId": "2",
                        "deviceId": "94",
                        "type": "android",
                    },
                    "referralCustomerId": "1",
                    "language": "en",
                },
                request_only=True,
                media_type="application/json",
            )
        ],
        responses={
            200: inline_serializer(
                name="CustomerResponse",
                fields={
                    "access": serializers.CharField(),
                    "refresh": serializers.CharField(),
                    "customer": CustomerDetailedSerializer(),
                },
            ),
            201: inline_serializer(
                name="CustomerCreatedResponse",
                fields={
                    "access": serializers.CharField(),
                    "refresh": serializers.CharField(),
                    "customer": CustomerDetailedSerializer(),
                },
            ),
        },
    )
    def post(self, request):
        serializer = CustomerCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        otp = serializer.validated_data["otp"]
        language = serializer.validated_data.get("language")
        inviter = serializer.validated_data.get("referral_customer_id")
        country = serializer.validated_data["country"]

        device_dict = serializer.validated_data.get("device")
        device_data = DeviceData(**device_dict) if device_dict else None

        customer = CustomerSelector.get_customer_by_phone(phone_number=phone_number)

        if customer and not customer.is_active:
            raise ValidationError(
                _("This account has been deactivated. Please contact support."),
                code="account_deactivated",
            )

        OTPUtils.validate_correct_otp(
            phone_number=phone_number, code=otp, otp_type=OTPType.CUSTOMER_AUTH
        )
        customer, created = CustomerService.update_or_create_customer(
            phone_number=phone_number,
            language=language,
            inviter=inviter,
            country=country,
        )

        if device_data:
            DeviceService.register_device(user=customer, device_data=device_data)
        token_data = TokenService.generate_token_for_user(customer)
        customer_serializer = CustomerDetailedSerializer(
            customer, context={"request": request}
        )

        return Response(
            {
                "access": token_data.access,
                "refresh": token_data.refresh,
                "customer": customer_serializer.data,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class CustomerUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Profile"],
        operation_id="UpdateCustomer",
        description="Update the authenticated customer's profile information.",
        parameters=[
            OpenApiParameter(
                name="Accept-Language",
                type=OpenApiTypes.STR,
                location="header",
                required=False,
                description="Language preference for the response",
                examples=[
                    OpenApiExample(
                        name="English (US)",
                        value="en",
                        description="English with US locale preference",
                    ),
                ],
            ),
        ],
        request={
            "multipart/form-data": CustomerUpdateSerializer,
        },
        examples=[
            OpenApiExample(
                name="Complete Profile Update",
                description="Update all profile fields including image",
                value={
                    "fullName": "Mezo Doe",
                    "email": "john.doe@example.com",
                    "birthDate": "2011-01-02",
                    "primaryAddress": "1",
                    "gender": "M",
                    "language": "en",
                    "image": "default_image.png",
                },
                request_only=True,
                media_type="multipart/form-data",
            )
        ],
        responses={
            200: CustomerDetailedSerializer,
            400: OpenApiResponse(
                description="Validation Error",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Validation Error",
                        value={
                            "field_name": ["Error message for this field"],
                            "image": ["File size should not exceed 5MB"],
                        },
                        response_only=True,
                    )
                ],
            ),
        },
    )
    def patch(self, request):
        serializer = CustomerUpdateSerializer(
            request.user, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            CustomerDetailedSerializer(request.user, context={"request": request}).data
        )


class CustomerDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Profile"],
        operation_id="GetCustomerDetails",
        responses={
            200: CustomerDetailedSerializer,
        },
    )
    def get(self, request):
        customer = request.user
        serializer = CustomerDetailedSerializer(customer, context={"request": request})
        return Response(serializer.data)


class CustomerDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Profile"],
        operation_id="DeleteCustomer",
        parameters=[
            OpenApiParameter(
                name="Accept-Language",  # todo: it should be for all endpoints
                type=OpenApiTypes.STR,
                location="header",
                required=False,
                description="Language preference for the response",
                examples=[
                    OpenApiExample(
                        name="English (US)",
                        value="en",
                        description="English with US locale preference",
                    ),
                ],
            ),
        ],
        responses={
            204: OpenApiResponse(description="Account successfully deactivated."),
        },
    )
    def delete(self, request):
        customer = request.user
        customer.is_active = False
        UserServices.user_logout_all_devices(customer)
        customer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
