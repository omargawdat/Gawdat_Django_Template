from django.utils.translation import gettext_lazy as _
from unfold.decorators import display

from apps.location.models.country import Country


class CountryDisplayMixin:
    @display(description=_("Country"), header=True)
    def display_header(self, country: Country):
        return [
            country,
            _("Currency: {}").format(country.currency),
            "CO",
            {
                "path": country.flag.url if country.flag else "",
                "squared": False,
                "borderless": True,
            },
        ]

    @display(label={"True": "success", "False": "danger"}, description=_("Is Active"))
    def display_is_active_country(self, country: Country) -> str:
        return "True" if country.is_active else "False"
