from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.api.user.views import LogoutView

urlpatterns = [
    path("user/refresh-token/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user/logout/", LogoutView.as_view(), name="logout"),
]
