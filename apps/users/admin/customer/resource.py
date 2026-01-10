from import_export import resources
from import_export.widgets import DateTimeWidget

from apps.users.models.customer import Customer


class CustomerResource(resources.ModelResource):
    user_id = resources.Field(column_name="User ID", attribute="user")

    full_name = resources.Field(column_name="Full Name", attribute="full_name")
    gender = resources.Field(column_name="Gender", attribute="gender")
    birth_date = resources.Field(column_name="Birth Date", attribute="birth_date")
    country = resources.Field(column_name="Country", attribute="country")
    date_joined = resources.Field(
        column_name="Date Joined", attribute="user__date_joined"
    )
    email = resources.Field(column_name="E-mail", attribute="email")
    created_at = resources.Field(
        column_name="Created At",
        attribute="user__date_joined",
        widget=DateTimeWidget(format="%Y-%m-%d %H:%M:%S"),
    )

    class Meta:
        model = Customer
        fields = [
            "user_id",
            "email",
            "full_name",
            "gender",
            "birth_date",
            "country",
            "created_at",
        ]
