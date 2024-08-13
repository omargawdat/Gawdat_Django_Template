from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api.provider.serializers import ProviderLoginSerializer
from apps.users.api.provider.serializers import ProviderOutputSerializer
from apps.users.api.provider.serializers import ProviderRegisterSerializer
from apps.users.api.provider.serializers import ProviderUpdateSerializer
from apps.users.api.provider.swagger import provider_login_swagger
from apps.users.api.provider.swagger import provider_register_swagger
from apps.users.domain.utilities.jwt import JWTUtil
from apps.users.helpers.permissions import IsActiveProvider
from apps.users.models.provider import Provider


class ProviderRegistrationView(APIView):
    permission_classes = []

    @provider_register_swagger
    def post(self, request):
        serializer = ProviderRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.save()
        tokens = JWTUtil.generate_tokens_for_user(provider)
        return Response(
            {
                "refresh": tokens["refresh"],
                "access": tokens["access"],
                "provider": ProviderOutputSerializer(provider).data,
            },
            status=status.HTTP_201_CREATED,
        )


class ProviderLoginView(APIView):
    permission_classes = []

    @provider_login_swagger
    def post(self, request):
        serializer = ProviderLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        password = serializer.validated_data["password"]

        try:
            provider = Provider.objects.get(phone_number=phone_number)
            if provider.check_password(password):
                tokens = JWTUtil.generate_tokens_for_user(provider)
                return Response(
                    {
                        "refresh": tokens["refresh"],
                        "access": tokens["access"],
                        "user": ProviderOutputSerializer(provider).data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                raise AuthenticationFailed("Invalid credentials")
        except Provider.DoesNotExist as err:
            raise AuthenticationFailed("Invalid credentials") from err


class ProviderDetailView(APIView):
    permission_classes = [IsActiveProvider]
    serializer_class = ProviderOutputSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user, context={"request": request})
        return Response(serializer.data)

    def put(self, request):
        serializer = ProviderUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ProviderOutputSerializer(request.user, context={"request": request}).data)
