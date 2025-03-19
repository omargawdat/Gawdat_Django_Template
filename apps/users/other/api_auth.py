from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from config.helpers.env import env


class AuthenticationFailedMessages:
    INVALID_API_KEY = "Invalid or missing X-API-Key header"  # pragma: allowlist secret


class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get("x-api-key")
        expected_api_key = env.api_key

        if not api_key or api_key != expected_api_key:
            raise AuthenticationFailed(AuthenticationFailedMessages.INVALID_API_KEY)
