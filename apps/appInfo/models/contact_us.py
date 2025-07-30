from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.appInfo.other.constants import ContactCategory
from apps.users.models.customer import Customer


class ContactUs(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name=_("Customer"),
        help_text=_("Select the customer who is making this contact."),
    )
    contact_type = models.CharField(
        max_length=50,
        choices=ContactCategory.choices,
        verbose_name=_("Contact Type"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Please provide a detailed description of your issue or inquiry."),
    )
    has_checked = models.BooleanField(default=False, verbose_name=_("Has Checked"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    def __str__(self):
        return self.contact_type
