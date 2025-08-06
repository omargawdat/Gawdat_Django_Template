from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from drf_spectacular.utils import extend_schema

from apps.users.api.oauth.serialziers import FacebookAccessTokenSerializer
from apps.users.api.oauth.serialziers import GoogleIDTokenSerializer


@extend_schema(
    tags=["User/OAuth"],
    description="Login with Google using ID Token",
    request=GoogleIDTokenSerializer,
)
class GoogleIDTokenLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    serializer_class = GoogleIDTokenSerializer


@extend_schema(
    tags=["User/OAuth"],
    description="Login with Facebook using Access Token",
    request=FacebookAccessTokenSerializer,
)
class FacebookAccessTokenLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    serializer_class = FacebookAccessTokenSerializer


@extend_schema(
    tags=["User/OAuth"],
    description="Login with Apple",
)
class AppleLogin(SocialLoginView):
    adapter_class = AppleOAuth2Adapter
