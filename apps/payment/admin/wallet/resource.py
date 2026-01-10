from import_export import resources
from import_export.widgets import DateTimeWidget

from apps.payment.models.wallet import Wallet


class WalletResource(resources.ModelResource):
    id = resources.Field(column_name="Wallet ID", attribute="id")
    user_email = resources.Field(column_name="User Email", attribute="user__email")
    balance = resources.Field(column_name="Balance", attribute="balance")
    is_use_wallet_in_payment = resources.Field(
        column_name="Use Wallet in Payment", attribute="is_use_wallet_in_payment"
    )
    last_update = resources.Field(
        column_name="Last Update",
        attribute="last_update",
        widget=DateTimeWidget(format="%Y-%m-%d %H:%M:%S"),
    )

    class Meta:
        model = Wallet
        fields = [
            "id",
            "user_email",
            "balance",
            "is_use_wallet_in_payment",
            "last_update",
        ]
