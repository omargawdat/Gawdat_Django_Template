from django.db import models
from django.utils.translation import gettext_lazy as _


class CountryChoices(models.TextChoices):
    EGYPT = "EG", _("Egypt")
    SAUDI_ARABIA = "SA", _("Saudi Arabia")
    UNITED_ARAB_EMIRATES = "AE", _("United Arab Emirates")
    KUWAIT = "KW", _("Kuwait")
    QATAR = "QA", _("Qatar")
    OMAN = "OM", _("Oman")
    BAHRAIN = "BH", _("Bahrain")
    UNSELECTED = "UN", _("Unselected")


#  todo: move into payment app
class CurrencyCode(models.TextChoices):
    EGP = "EGP", _("Egyptian Pound")
    SAR = "SAR", _("Saudi Riyal")
    AED = "AED", _("Emirati Dirham")
    KWD = "KWD", _("Kuwaiti Dinar")
    QAR = "QAR", _("Qatari Riyal")
    OMR = "OMR", _("Omani Rial")
    BHD = "BHD", _("Bahraini Dinar")


class LocationNameChoices(models.TextChoices):
    Home = "HOME", _("Home")
    Work = "WORK", _("Work")
