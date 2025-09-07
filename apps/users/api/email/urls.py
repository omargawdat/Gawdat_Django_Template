from django.urls import path

from .views import CheckEmailView
from .views import RegisterView
from .views import VerifyCustomerEmailView

urlpatterns = [
    path("users/check-email/", CheckEmailView.as_view(), name="check-email"),
    path("users/register/", RegisterView.as_view(), name="register"),
    path("users/verify-email/", VerifyCustomerEmailView.as_view(), name="verify-email"),
]
