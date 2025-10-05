from django.utils import translation
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        auth_result = super().authenticate(request)
        if auth_result:
            user, _token = auth_result
            user_language = user.language
            translation.activate(user_language)
            request.LANGUAGE_CODE = user_language
            request.META["HTTP_ACCEPT_LANGUAGE"] = user_language
        return auth_result
