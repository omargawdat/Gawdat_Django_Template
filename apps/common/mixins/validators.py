from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from apps.common.helpers.constants import ValidationErrorType


class BaseValidator:
    @staticmethod
    def raise_error(message, error_type: ValidationErrorType):
        if error_type == ValidationErrorType.DRF:
            raise DRFValidationError(message)
        elif error_type == ValidationErrorType.DJANGO:
            raise DjangoValidationError(message)
