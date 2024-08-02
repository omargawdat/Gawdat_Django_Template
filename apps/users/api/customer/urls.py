from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("v1/refresh-token/", TokenRefreshView.as_view(), name="token_refresh"),
]
