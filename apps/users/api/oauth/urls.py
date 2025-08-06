from django.urls import include
from django.urls import path

from .views import AppleLogin
from .views import FacebookAccessTokenLogin
from .views import GoogleIDTokenLogin

urlpatterns = [
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path("accounts", include("allauth.urls")),
    # Facebook
    path("oauth/facebook/", FacebookAccessTokenLogin.as_view(), name="facebook"),
    # Google
    path("oauth/google/", GoogleIDTokenLogin.as_view(), name="google"),
    # Apple
    path("oauth/apple/", AppleLogin.as_view(), name="apple"),
]
