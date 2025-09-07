from django.urls import path

from .views import CheckEmailView
from .views import RegisterView

urlpatterns = [
    path("users/check-email/", CheckEmailView.as_view(), name="check-email"),
    path("users/register/", RegisterView.as_view(), name="register"),
]
