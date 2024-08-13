from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api.customer.serializers import CustomerLoginSerializer
from apps.users.api.customer.serializers import CustomerOutputSerializer
from apps.users.api.customer.serializers import CustomerRegisterSerializer
from apps.users.api.customer.serializers import CustomerUpdateSerializer
from apps.users.api.customer.swagger import customer_login_swagger
from apps.users.api.customer.swagger import customer_register_swagger
from apps.users.domain.utilities.jwt import JWTUtil
from apps.users.helpers.permissions import IsActiveCustomer
from apps.users.models.customer import Customer


class CustomerRegistrationView(APIView):
    permission_classes = []

    @customer_register_swagger
    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        tokens = JWTUtil.generate_tokens_for_user(customer)
        return Response(
            {
                "refresh": tokens["refresh"],
                "access": tokens["access"],
                "customer": CustomerOutputSerializer(customer).data,
            },
            status=status.HTTP_201_CREATED,
        )


class CustomerLoginView(APIView):
    permission_classes = []

    @customer_login_swagger
    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        password = serializer.validated_data["password"]

        try:
            customer = Customer.objects.get(phone_number=phone_number)
            if customer.check_password(password):
                tokens = JWTUtil.generate_tokens_for_user(customer)
                return Response(
                    {
                        "refresh": tokens["refresh"],
                        "access": tokens["access"],
                        "customer": CustomerOutputSerializer(customer).data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                raise AuthenticationFailed("Invalid credentials")
        except Customer.DoesNotExist as err:
            raise AuthenticationFailed("Invalid credentials") from err


class CustomerDetailView(APIView):
    permission_classes = [IsActiveCustomer]
    serializer_class = CustomerOutputSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user, context={"request": request})
        return Response(serializer.data)

    def put(self, request):
        update_serializer = CustomerUpdateSerializer(request.user, data=request.data, partial=True)
        update_serializer.is_valid(raise_exception=True)
        update_serializer.save()
        output_serializer = self.serializer_class(request.user, context={"request": request})
        return Response(output_serializer.data)
