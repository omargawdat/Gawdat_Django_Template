from import_export import resources

from apps.products.models.category import Category


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = []
