from django.utils.translation import gettext_lazy as _
from unfold.decorators import display

from apps.appInfo.models.banner import Banner


class BannerDisplayMixin:
    @display(description=_("banner"), header=True)
    def display_header(self, banner: Banner):
        """Display header with image if available."""
        return [
            "",
            "",
            "O",
            {
                "path": banner.image.url,
                "squared": True,
                "borderless": True,
                "width": 75,
                "height": 75,
            },
        ]
