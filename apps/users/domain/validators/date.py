from common.helpers.constants import ValidationErrorType
from common.mixins.validators import BaseValidator


class DateValidator(BaseValidator):
    @staticmethod
    def validate_date_format(date_format="%Y-%m-%d", use_drf=ValidationErrorType.DRF):
        DateValidator.raise_error(
            f"Invalid date format, should be {date_format}", use_drf
        )
