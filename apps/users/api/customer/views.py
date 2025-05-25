from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.parser import CamelCaseMultiPartParser
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
from apps.users.domain.services.customer import CustomerService
from apps.users.domain.services.token import TokenService
from apps.users.domain.services.user import UserServices


class CustomerAuthView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [CamelCaseJSONParser]

    @extend_schema(
        tags=["User/Customer"],
        operation_id="AuthenticateCustomer",
        description="Authenticate a customer using phone number and OTP. Creates a new customer if one doesn't exist.",
        request=CustomerCreateSerializer,
        responses={
            200: inline_serializer(
                name="CustomerAuthResponse",
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
        device_dict = serializer.validated_data.get("device", {})
        device_data = DeviceData(**device_dict)

        OTPUtils.validate_correct_otp(
            phone_number=phone_number, code=otp, otp_type=OTPType.CUSTOMER_AUTH
        )
        customer, created = CustomerService.update_or_create_customer(
            phone_number=phone_number, language=language
        )

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
    parser_classes = [CamelCaseMultiPartParser, CamelCaseJSONParser]

    @extend_schema(
        tags=["User/Customer"],
        operation_id="UpdateCustomer",
        description="Update the authenticated customer's profile information.",
        request=CustomerUpdateSerializer,
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
            200: CustomerDetailedSerializer,
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
        tags=["User/Customer"],
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
        tags=["User/Customer"],
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
