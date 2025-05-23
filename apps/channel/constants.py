from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationType(models.TextChoices):
    PRODUCT_ORDERED = "product_ordered", _("Product Ordered")  # New type
    OTHER = "other", _("Other")


class Language(models.TextChoices):
    ENGLISH = "en", "English"
    ARABIC = "ar", "Arabic"


class OTPType(models.TextChoices):
    CUSTOMER_AUTH = "customer_auth", "Customer Authentication"
    PROVIDER_AUTH = "provider_auth", "Provider Authentication"
    PASSWORD_RESET = "password_reset", "Password Reset"  # pragma: allowlist secret
