import re

from django.core.exceptions import ValidationError
from django.db import models


class ArabicCharField(models.CharField):
    description = "A field that accepts Arabic letters, numbers, and symbols"
    NO_ENGLISH_MESSAGE = "This field does not accept English letters."
    INVALID_CHARS_MESSAGE = (
        "This field only accepts Arabic letters, numbers, and symbols."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if re.search(r"[a-zA-Z]", value):
            raise ValidationError(self.NO_ENGLISH_MESSAGE)
        if not re.match(
            r'^[\u0600-\u06FF\s0-9!@#$%^&*()_+\-=\[\]{};:\'"\\|,.<>/?]+$',
            value,
        ):
            raise ValidationError(self.INVALID_CHARS_MESSAGE)


class EnglishCharField(models.CharField):
    description = "A field that accepts English letters, numbers, and symbols"
    NO_ARABIC_MESSAGE = "This field does not accept Arabic letters."
    INVALID_CHARS_MESSAGE = (
        "This field only accepts English letters, numbers, and symbols."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if re.search(r"[\u0600-\u06FF]", value):
            raise ValidationError(self.NO_ARABIC_MESSAGE)
        if not re.match(r'^[a-zA-Z\s0-9!@#$%^&*()_+\-=\[\]{};:\'"\\|,.<>/?]+$', value):
            raise ValidationError(self.INVALID_CHARS_MESSAGE)
