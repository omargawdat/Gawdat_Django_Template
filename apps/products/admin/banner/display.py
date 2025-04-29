from unfold.decorators import display

from apps.products.models.banner import Banner


class BannerDisplayMixin:
    @display(description="banner", header=True)
    def display_header(self, banner: Banner):
        """Display header with image if available."""
        return [
            banner.pk,
            "",
            "O",
            {
                "path": banner.image.url
                if hasattr(banner, "image") and banner.image
                else None
            },
        ]
