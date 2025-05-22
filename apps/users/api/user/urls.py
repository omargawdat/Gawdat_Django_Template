from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.api.user.views import LogoutView

urlpatterns = [
    path("users/refresh-token/", TokenRefreshView.as_view(), name="user-refresh-token"),
    path("users/logout/", LogoutView.as_view(), name="user-logout"),
]
