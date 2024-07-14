from enum import Enum


class ValidationErrorType(Enum):
    DJANGO = "django"
    DRF = "drf"
