from import_export import resources

from apps.appInfo.models.onboarding import Onboarding


class OnboardingResource(resources.ModelResource):
    class Meta:
        model = Onboarding
        fields = []
