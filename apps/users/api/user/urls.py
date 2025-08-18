from django.urls import path

from apps.users.api.user.views import DocumentedTokenRefreshView
from apps.users.api.user.views import LogoutAllDevicesView
from apps.users.api.user.views import LogoutDeviceView
from apps.users.api.user.views import SendOTPView
from apps.users.api.user.views import SetPasswordView

urlpatterns = [
    path(
        "refresh-token/",
        DocumentedTokenRefreshView.as_view(),
        name="user-refresh-token",
    ),
    path(
        "users/logout-all-devices/", LogoutAllDevicesView.as_view(), name="user-logout"
    ),
    path("users/logout-device/", LogoutDeviceView.as_view(), name="user-logout-device"),
    path("users/reset-password/", SendOTPView.as_view(), name="reset-password"),
    path("users/confirm/password", SetPasswordView.as_view(), name="verify_otp"),
]
