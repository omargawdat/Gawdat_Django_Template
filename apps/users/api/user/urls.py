from django.urls import path

from apps.users.api.user.views import DocumentedTokenRefreshView
from apps.users.api.user.views import LogoutDeviceView
from apps.users.api.user.views import LogoutView

urlpatterns = [
    path(
        "users/refresh-token/",
        DocumentedTokenRefreshView.as_view(),
        name="user-refresh-token",
    ),
    path("users/logout/", LogoutView.as_view(), name="user-logout"),
    path("users/logout-device/", LogoutDeviceView.as_view(), name="user-logout-device"),
]
