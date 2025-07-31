from import_export import resources

from apps.appInfo.models.popup import PopUpBanner


class PopUpBannerResource(resources.ModelResource):
    class Meta:
        model = PopUpBanner
        fields = []
