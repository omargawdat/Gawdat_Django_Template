from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactCategory(models.TextChoices):
    GENERAL = "GENERAL", _("General")
    SUPPORT = "SUPPORT", _("Support")
    FEEDBACK = "FEEDBACK", _("Feedback")
    OTHER = "OTHER", _("Other")
    COMPLAINT = "COMPLAINT", _("Complaint")
