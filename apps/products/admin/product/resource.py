from import_export import resources

from apps.products.models.product import Product


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = []
