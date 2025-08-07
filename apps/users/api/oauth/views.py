from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response

from apps.users.api.oauth.serialziers import FacebookAccessTokenSerializer
from apps.users.api.oauth.serialziers import GoogleIDTokenSerializer
from apps.users.domain.services.token import TokenService


@extend_schema(
    tags=["User/OAuth"],
    description="Login with Google using ID Token",
    request=GoogleIDTokenSerializer,
)
class GoogleIDTokenLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    serializer_class = GoogleIDTokenSerializer

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user = self.request.user
        token_data = TokenService.generate_token_for_user(user)

        return Response(
            {
                "access": token_data.access,
                "refresh": token_data.refresh,
                "customer": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                },
            }
        )


@extend_schema(
    tags=["User/OAuth"],
    description="Login with Facebook using Access Token",
    request=FacebookAccessTokenSerializer,
)
class FacebookAccessTokenLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    serializer_class = FacebookAccessTokenSerializer

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user = self.request.user
        token_data = TokenService.generate_token_for_user(user)

        return Response(
            {
                "access": token_data.access,
                "refresh": token_data.refresh,
                "customer": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                },
            }
        )


@extend_schema(
    tags=["User/OAuth"],
    description="Login with Apple",
)
class AppleLogin(SocialLoginView):
    adapter_class = AppleOAuth2Adapter
