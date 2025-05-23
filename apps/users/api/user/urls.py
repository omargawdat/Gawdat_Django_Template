from django.urls import path

from apps.users.api.user.views import DocumentedTokenRefreshView
from apps.users.api.user.views import LogoutAllDevicesView
from apps.users.api.user.views import LogoutDeviceView

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
]
