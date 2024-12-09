from drf_standardized_errors.handler import ExceptionHandler
from rest_framework.exceptions import AuthenticationFailed as DRFAuthenticationFailed
from rest_framework_simplejwt.exceptions import (
    AuthenticationFailed as SimpleAuthenticationFailed,
)
from rest_framework_simplejwt.exceptions import InvalidToken


class CustomExceptionHandler(ExceptionHandler):
    def convert_known_exceptions(self, exc: Exception) -> Exception:
        if isinstance(exc, (SimpleAuthenticationFailed, InvalidToken)):
            detail = (
                exc.detail["detail"] if isinstance(exc.detail, dict) else exc.detail
            )
            code = (
                exc.detail.get("code")
                if isinstance(exc.detail, dict)
                else exc.default_code
            )
            return DRFAuthenticationFailed(detail, code=code)
        return super().convert_known_exceptions(exc)
