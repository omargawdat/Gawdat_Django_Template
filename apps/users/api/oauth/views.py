from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from rest_framework.response import Response

from apps.users.api.customer.serializers import CustomerDetailedSerializer
from apps.users.domain.services.token import TokenService

GoogleIdTokenRequest = inline_serializer(
    name="GoogleIdTokenRequest",
    fields={
        "access_token": serializers.CharField(
            help_text="Google ID token (JWT) from Google Sign-In"
        )  # pragma: allowlist secret
    },
)


class GoogleIDTokenLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["User/Customer/Authentication/OAuth"],
        operation_id="googleAuthentication",
        description="Login using a Google ID token. Returns JWT access/refresh tokens and the customer profile.",
        request={"application/json": GoogleIdTokenRequest},
        examples=[
            OpenApiExample(
                name="Valid Google ID token",
                value={
                    "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6..."
                },  # pragma: allowlist secret
                request_only=True,
                media_type="application/json",
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user = self.request.user
        token_data = TokenService.generate_token_for_user(user)

        customer_serializer = CustomerDetailedSerializer(
            user, context={"request": request}
        )

        return Response(
            {
                "access": token_data.access,
                "refresh": token_data.refresh,
                "customer": customer_serializer.data,
            }
        )


FacebookAccessTokenRequest = inline_serializer(
    name="FacebookAccessTokenRequest",
    fields={
        "access_token": serializers.CharField(
            help_text="Facebook access token obtained from the Facebook SDK / Graph API login flow"
        )  # pragma: allowlist secret
    },
)


class FacebookAccessTokenLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["User/Customer/Authentication/OAuth"],
        operation_id="facebookAuthentication",
        description="Login with Facebook using an access token. Returns JWT access/refresh tokens and the customer profile.",
        request={"application/json": FacebookAccessTokenRequest},
        examples=[
            OpenApiExample(
                name="Valid Facebook access token",
                value={
                    "access_token": "EAAGm0PX4ZCpsBAKZC..."
                },  # pragma: allowlist secret
                request_only=True,
                media_type="application/json",
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user = self.request.user
        token_data = TokenService.generate_token_for_user(user)
        customer_serializer = CustomerDetailedSerializer(
            user, context={"request": request}
        )

        return Response(
            {
                "access": token_data.access,
                "refresh": token_data.refresh,
                "customer": customer_serializer.data,
            }
        )
