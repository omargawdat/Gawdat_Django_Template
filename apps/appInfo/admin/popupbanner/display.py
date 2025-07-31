from unfold.decorators import display

from apps.appInfo.models.popup import PopUpBanner
from apps.appInfo.models.popup import PopUpTracking


class PopUpBannerDisplayMixin:
    @display(description="PopUp Banner", header=True)
    def display_header(self, pop_up_banner: PopUpBanner):
        """Display header with image if available."""
        return [
            "",
            "",
            "O",
            {
                "path": pop_up_banner.image.url,
                "squared": True,
                "borderless": True,
                "width": 75,
                "height": 75,
            },
        ]

    @display(description="Views", label="info")
    def display_views(self, popup_banner: PopUpBanner):
        return PopUpTracking.objects.filter(popup_id=popup_banner.id).count()
