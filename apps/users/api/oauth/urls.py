from django.urls import include
from django.urls import path

from .views import FacebookAccessTokenLogin
from .views import GoogleIDTokenLogin

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("oauth/facebook/", FacebookAccessTokenLogin.as_view(), name="facebook"),
    path("oauth/google/", GoogleIDTokenLogin.as_view(), name="google"),
]
