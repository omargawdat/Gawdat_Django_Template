from unfold.decorators import display

from apps.appInfo.models.onboarding import Onboarding


class OnboardingDisplayMixin:
    @display(description="OnBoarding", header=True)
    def display_header(self, onboarding: Onboarding):
        """Display header with image if available."""
        return [
            onboarding.title,
            "",
            "O",
            {
                "path": onboarding.image.url,
                "squared": True,
                "borderless": True,
                "width": 75,
                "height": 75,
            },
        ]
