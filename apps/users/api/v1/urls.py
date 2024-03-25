# urls.py
from django.urls import path

from .views import LoginView, RegisterView, UserProfileUpdateView

urlpatterns = [
    path("signup/", RegisterView.as_view(), name="signup"),
    path("profile/update/", UserProfileUpdateView.as_view(), name="update-profile"),
    path("login/", LoginView.as_view(), name="login"),
]
