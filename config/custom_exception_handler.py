import re

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.utils import IntegrityError
from drf_standardized_errors.handler import ExceptionHandler
from rest_framework.exceptions import AuthenticationFailed as DRFAuthenticationFailed
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import (
    AuthenticationFailed as SimpleAuthenticationFailed,
)
from rest_framework_simplejwt.exceptions import InvalidToken

from common.error_codes import ApplicationError


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
            if hasattr(exc, "error_dict"):
                field = next(iter(exc.error_dict))
                validation_error = exc.error_dict[field][0]
                code = (
                    validation_error.code
                    if hasattr(validation_error, "code")
                    else "overlapping_events"
                )
            else:
                code = exc.code if hasattr(exc, "code") else "overlapping_events"

            error_message = ApplicationError.get_message(code)
            if error_message:
                detail = {"error": error_message}
            elif hasattr(exc, "message_dict"):
                detail = exc.message_dict
            else:
                detail = {"error": exc.messages[0] if exc.messages else str(exc)}

            return ValidationError(detail=detail, code=code)

        if isinstance(exc, IntegrityError):
            error_message = str(exc)
            constraint_match = re.search(r'"([^"]+)"', error_message)
            code = constraint_match.group(1) if constraint_match else "integrity_error"

            error_message = ApplicationError.get_message(code)
            detail = {"error": error_message}

            return ValidationError(detail=detail, code=code)

        return super().convert_known_exceptions(exc)
