from django.utils.translation import gettext_lazy as _
from unfold.decorators import display

from apps.appInfo.models.banner_group import BannerGroup


class BannerGroupDisplayMixin:
    @display(description=_("Group"), header=True)
    def display_header(self, banner_group: BannerGroup):
        """Display header with image if available."""
        return [
            banner_group.name,
        ]
