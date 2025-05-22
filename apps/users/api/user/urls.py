from django.urls import path
from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.api.user.views import LogoutDeviceView
from apps.users.api.user.views import LogoutView


@extend_schema(
    tags=["Authentication"],
    operation_id="RefreshToken",
    description="Refresh an expired access token using a valid refresh token.",
    responses={
        200: TokenRefreshSerializer,
        401: OpenApiResponse(description="Invalid refresh token"),
    },
)
class DocumentedTokenRefreshView(TokenRefreshView):
    pass


urlpatterns = [
    path(
        "users/refresh-token/",
        DocumentedTokenRefreshView.as_view(),
        name="user-refresh-token",
    ),
    path("users/logout/", LogoutView.as_view(), name="user-logout"),
    path("users/logout-device/", LogoutDeviceView.as_view(), name="user-logout-device"),
]
