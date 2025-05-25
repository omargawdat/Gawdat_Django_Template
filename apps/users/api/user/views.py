from djangorestframework_camel_case.parser import CamelCaseJSONParser
from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.api.user.serializers import DeviceLogoutSerializer
from apps.users.domain.services.user import UserServices


@extend_schema(
    tags=["User/Authentication"],
)
class DocumentedTokenRefreshView(TokenRefreshView):
    pass


class LogoutAllDevicesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["User/Authentication"],
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
        tags=["User/Authentication"],
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
