from import_export import resources
from import_export.widgets import DateTimeWidget

from apps.users.models.provider import Provider


class ProviderResource(resources.ModelResource):
    user_id = resources.Field(column_name="User ID", attribute="user")
    email = resources.Field(column_name="E-mail", attribute="email")
    company_name = resources.Field(column_name="Company Name", attribute="company_name")
    created_at = resources.Field(
        column_name="Created At",
        attribute="user__date_joined",
        widget=DateTimeWidget(format="%Y-%m-%d %H:%M:%S"),
    )

    class Meta:
        model = Provider
        fields = [
            "user_id",
            "email",
            "company_name",
            "created_at",
        ]
