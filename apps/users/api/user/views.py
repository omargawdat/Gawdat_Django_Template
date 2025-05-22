from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.api.user.serializers import DeviceLogoutSerializer
from apps.users.domain.services.user import UserServices


@extend_schema(
    tags=["User/Authentication"],
    operation_id="logoutUser",
    description="Log out the current user from all devices by invalidating their refresh tokens.",
    responses={
        204: OpenApiResponse(description="Successfully logged out from all devices"),
        401: OpenApiResponse(
            description="Authentication credentials were not provided or are invalid"
        ),
    },
)
class LogoutView(GenericAPIView):
    def post(self, request):
        user = request.user
        UserServices.user_logout_all_devices(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["User/Authentication"],
    operation_id="refreshToken",
)
class DocumentedTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(
    tags=["User/Authentication"],
    operation_id="logoutDevice",
    request=DeviceLogoutSerializer,
    responses={
        204: OpenApiResponse(description="Successfully logged out from the device"),
    },
)
class LogoutDeviceView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceLogoutSerializer
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        UserServices.user_logout_specific_device(
            user=request.user,
            refresh_token=serializer.validated_data["refresh_token"],
            registration_id=serializer.validated_data["registration_id"],
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
