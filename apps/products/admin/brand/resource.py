from import_export import resources

from apps.products.models.brand import Brand


class BrandResource(resources.ModelResource):
    class Meta:
        model = Brand
        fields = []
