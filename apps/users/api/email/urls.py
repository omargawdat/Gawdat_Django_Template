from django.urls import path

from .views import ChangePasswordView
from .views import CheckEmailView
from .views import LoginView
from .views import RegisterView
from .views import VerifyCustomerEmailView

urlpatterns = [
    path("users/check-email/", CheckEmailView.as_view(), name="check-email"),
    path("users/register/", RegisterView.as_view(), name="register"),
    path("users/verify-email/", VerifyCustomerEmailView.as_view(), name="verify-email"),
    path("users/login/", LoginView.as_view(), name="login"),
    path(
        "users/change-password/", ChangePasswordView.as_view(), name="change-password"
    ),
]
