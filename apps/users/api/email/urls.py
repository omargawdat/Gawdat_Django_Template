from django.urls import path

from .views import CheckEmailView

urlpatterns = [
    path("users/check-email/", CheckEmailView.as_view(), name="check-email"),
]
