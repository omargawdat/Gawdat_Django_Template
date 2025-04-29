from import_export import resources

from apps.products.models.banner import Banner


class BannerResource(resources.ModelResource):
    class Meta:
        model = Banner
        fields = []
