from import_export import resources

from apps.users.models.provider import Provider


class ProviderResource(resources.ModelResource):
    class Meta:
        model = Provider
        fields = []
