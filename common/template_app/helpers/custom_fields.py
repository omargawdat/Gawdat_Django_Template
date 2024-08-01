import re

from django.core.exceptions import ValidationError
from django.db import models


class ArabicCharField(models.CharField):
    description = "A field that accepts only Arabic characters"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if not re.match(r"^[\u0600-\u06FF\s]+$", value):
            raise ValidationError("This field only accepts Arabic characters.")


class EnglishCharField(models.CharField):
    description = "A field that accepts only English characters"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if not re.match(r"^[a-zA-Z\s]+$", value):
            raise ValidationError("This field only accepts English characters.")
