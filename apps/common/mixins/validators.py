from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError


class FlexibleValidator:
    def __init__(self, validation_func):
        self.validation_func = validation_func

    def __call__(self, *args, **kwargs):
        is_rest = kwargs.pop("is_rest", False)
        try:
            return self.validation_func(*args, **kwargs)
        except (ValueError, TypeError) as e:
            if is_rest:
                raise DRFValidationError(str(e)) from e
            raise DjangoValidationError(str(e)) from e

    def __get__(self, obj, objtype):
        """Support descriptor protocol to make it work with Django model fields"""
        return self


def flexible_validator(func):
    return FlexibleValidator(func)
