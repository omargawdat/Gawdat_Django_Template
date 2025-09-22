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

GoogleIDTokenRequest = inline_serializer(
    name="GoogleIDTokenRequest",
    fields={
        "access_token": serializers.CharField(
            help_text="The Google access token (JWT) obtained on the client.",
        )
    },
)


class GoogleIDTokenLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["User/Authentication/OAuth"],
        operation_id="googleAuthentication",
        description=(
            "Login using a **Google access token** (e.g. from Google One Tap / GIS). "
            "Returns JWT access/refresh tokens and the customer profile."
        ),
        request=GoogleIDTokenRequest,
        examples=[
            OpenApiExample(
                name="access token login",
                value={"access_token": "REDACTED"},
                request_only=True,
                media_type="application/json",
            ),
        ],
        responses={200: CustomerDetailedSerializer},
    )
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user = self.request.user

        user.is_verified = True
        user.save(update_fields=["is_verified"])

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


FacebookIDTokenRequest = inline_serializer(
    name="FacebookIDTokenRequest",
    fields={
        "access_token": serializers.CharField(
            help_text="The Facebook access token (JWT) obtained on the client.",
        )
    },
)


class FacebookAccessTokenLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["User/Authentication/OAuth"],
        operation_id="facebookAuthentication",
        description="Login with Facebook using an access token. Returns JWT access/refresh tokens and the customer profile.",
        request=FacebookIDTokenRequest,
        examples=[
            OpenApiExample(
                name="access token login",
                value={"access_token": "REDACTED"},
                request_only=True,
                media_type="application/json",
            ),
        ],
        responses={200: CustomerDetailedSerializer},
    )
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user = self.request.user

        user.is_verified = True
        user.save(update_fields=["is_verified"])

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
