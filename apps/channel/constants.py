from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationType(models.TextChoices):
    PRODUCT_ORDERED = "product_ordered", _("Product Ordered")  # New type
    OTHER = "other", _("Other")
    REFERRAL_APP_INSTALL = "referral_app_install", _("Referral App Install")
    REFERRAL_FIRST_ORDER = "referral_first_order", _("Referral First Order")
    MONEY_ADDED = "money_added", _("Money Added")


class Language(models.TextChoices):
    ENGLISH = "en", "English"
    ARABIC = "ar", "Arabic"


class OTPType(models.TextChoices):
    CUSTOMER_AUTH = "customer_auth", "Customer Authentication"
    PROVIDER_AUTH = "provider_auth", "Provider Authentication"
    PASSWORD_RESET = "password_reset", "Password Reset"  # pragma: allowlist secret
    PHONE_VERIFICATION = "phone_verification", "Phone Verification"
