from import_export import resources

from apps.location.models.country import Country


class CountryResource(resources.ModelResource):
    class Meta:
        model = Country
        fields = []
