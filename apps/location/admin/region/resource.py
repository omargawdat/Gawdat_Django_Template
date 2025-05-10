from import_export import resources

from apps.location.models.region import Region


class RegionResource(resources.ModelResource):
    class Meta:
        model = Region
        fields = []
