from rest_framework import generics
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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
from apps.users.models.customer import Customer


class CustomerAuthView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = CustomerCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(
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


class CustomerDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerDetailedSerializer

    def get_object(self):
        return self.request.user


class CustomerUpdateView(APIView):
    permission_classes = []

    def patch(self, request):
        serializer = CustomerUpdateSerializer(
            request.user, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            CustomerDetailedSerializer(request.user, context={"request": request}).data
        )


class CustomerDeleteView(generics.DestroyAPIView):
    permission_classes = []

    def get_object(self):
        return self.request.user

    def perform_destroy(self, customer: Customer):
        customer.is_active = False
        UserServices.user_logout_all_devices(customer)
        customer.save()
