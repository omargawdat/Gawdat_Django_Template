from django.utils.translation import gettext_lazy as _
from unfold.decorators import display

from apps.location.models.region import Region


class RegionDisplayMixin:
    @display(description=_("region"), header=True)
    def display_header(self, region: Region):
        return [
            region.pk,
            "",
            "R",
            {"path": region.country.flag.url},
        ]

    @display(label={"True": "success", "False": "danger"}, description=_("Is Active"))
    def display_is_active_region(self, region: Region):
        return "True" if region.country.is_active else "False"
