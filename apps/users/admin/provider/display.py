from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _
from unfold.decorators import display

from apps.users.models.provider import Provider


class ProviderDisplayMixin:
    @display(description=_("Provider"), header=True)
    def display_provider_info(self, provider: Provider):
        return [
            provider.company_name or provider.email,
            _("Email: %s") % provider.email,
            "PR",
            None,  # No image for provider
        ]

    @display(
        label={"True": "success", "False": "danger"},
        description=_("Is Active"),
        ordering="user__is_active",
    )
    def display_is_active_provider(self, provider: Provider) -> str:
        return _("True") if provider.is_active else _("False")

    @display(description=_("Date joined ago"), label="info")
    def display_date_joined_time(self, provider: Provider):
        return f"{timesince(provider.user.date_joined, timezone.now())}"
