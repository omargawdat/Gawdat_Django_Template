from import_export import resources

from apps.appInfo.models.banner import Banner


class BannerResource(resources.ModelResource):
    class Meta:
        model = Banner
        fields = []
