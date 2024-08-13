from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.api.user.views import ChangePasswordView
from apps.users.api.user.views import SendOtpView
from apps.users.api.user.views import UserDeactivateView
from apps.users.api.user.views import VerifyPasswordForgetView
from apps.users.api.user.views import VerifyPhoneView

urlpatterns = [
    path("v1/refresh-token/", TokenRefreshView.as_view(), name="token_refresh"),
    path("v1/send-otp/", SendOtpView.as_view(), name="send-otp"),
    path("v1/verify-phone-number/", VerifyPhoneView.as_view(), name="verify-phone-number"),
    path("v1/user/deactivate/", UserDeactivateView.as_view(), name="user-deactivate"),
    path(
        "v1/verify-password-forget/",
        VerifyPasswordForgetView.as_view(),
        name="verify-otp-for-password-forget",
    ),
    path("v1/change-password/", ChangePasswordView.as_view(), name="change-password"),
]
