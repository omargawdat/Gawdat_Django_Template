from django.core.exceptions import ValidationError as DjangoValidationError
from drf_standardized_errors.handler import ExceptionHandler
from rest_framework import exceptions
from rest_framework.exceptions import AuthenticationFailed as DRFAuthenticationFailed
from rest_framework.serializers import as_serializer_error
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

        if isinstance(exc, DjangoValidationError):
            exc = exceptions.ValidationError(as_serializer_error(exc))

        return super().convert_known_exceptions(exc)
