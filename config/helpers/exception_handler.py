try:
    from psycopg.errors import UniqueViolation
except ImportError:
    UniqueViolation = None

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from drf_standardized_errors.handler import ExceptionHandler
from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error


class CustomExceptionHandler(ExceptionHandler):
    def convert_known_exceptions(self, exc: Exception) -> Exception:
        if isinstance(exc, DjangoValidationError):
            exc = exceptions.ValidationError(as_serializer_error(exc))

        if isinstance(exc, IntegrityError) or (
            UniqueViolation and isinstance(exc, UniqueViolation)
        ):
            return exceptions.ValidationError({"non_field_errors": [str(exc)]})

        return super().convert_known_exceptions(exc)
