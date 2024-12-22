import os

from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed


class AuthenticationFailedMessages:
    INVALID_API_KEY = "Invalid or missing X-API-Key header"


class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        path = request.path_info.lower()

        # Skip check for paths containing 'web' or 'callback'
        if "web" in path or "callback" in path:
            return

        # pragma: allowlist secret
        api_key = request.headers.get("x-api-key")
        expected_api_key = os.environ.get("API_KEY")

        if not api_key or api_key != expected_api_key:
            raise AuthenticationFailed(AuthenticationFailedMessages.INVALID_API_KEY)

        return
