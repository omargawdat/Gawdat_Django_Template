from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.domain.services.user import UserServices


@extend_schema(
    tags=["Authentication"],
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
    tags=["Authentication"],
    operation_id="refreshToken",
)
class DocumentedTokenRefreshView(TokenRefreshView):
    pass
