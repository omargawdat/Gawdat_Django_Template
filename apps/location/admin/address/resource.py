from import_export import resources

from apps.location.models.address import Address


class AddressResource(resources.ModelResource):
    class Meta:
        model = Address
        fields = []
