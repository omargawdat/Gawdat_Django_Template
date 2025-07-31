from import_export import resources

from apps.appInfo.models.banner_group import BannerGroup


class BannerGroupResource(resources.ModelResource):
    class Meta:
        model = BannerGroup
        fields = []
