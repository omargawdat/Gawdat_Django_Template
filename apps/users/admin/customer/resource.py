from import_export import resources

from apps.users.models.customer import Customer


class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer
        fields = []
