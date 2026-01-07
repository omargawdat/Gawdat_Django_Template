from import_export import resources
from import_export.widgets import DateTimeWidget

from apps.payment.models.payment import Payment


class PaymentResource(resources.ModelResource):
    id = resources.Field(column_name="Payment ID", attribute="id")
    customer_email = resources.Field(
        column_name="Customer Email", attribute="customer__user__email"
    )
    price_before_discount = resources.Field(
        column_name="Price Before Discount", attribute="price_before_discount"
    )
    price_after_discount = resources.Field(
        column_name="Price After Discount", attribute="price_after_discount"
    )
    payment_type = resources.Field(column_name="Payment Type", attribute="payment_type")
    is_paid = resources.Field(column_name="Is Paid", attribute="is_paid")
    payment_charge_id = resources.Field(
        column_name="Payment Reference", attribute="payment_charge_id"
    )
    created_at = resources.Field(
        column_name="Created At",
        attribute="created_at",
        widget=DateTimeWidget(format="%Y-%m-%d %H:%M:%S"),
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "customer_email",
            "price_before_discount",
            "price_after_discount",
            "payment_type",
            "is_paid",
            "payment_charge_id",
            "created_at",
        ]
