from django.http import HttpRequest

from apps.payment.models.wallet_transaction import WalletTransaction
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions


class BaseWalletTransactionPermissions:
    def get_field_config(
        self, request: HttpRequest, wallet_transaction: WalletTransaction | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            "wallet": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "transaction_type": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "amount_currency": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "amount": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "created_at": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "action_by": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "transaction_note": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "attachment": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
        }


class WalletTransactionAdminPermissions(BaseWalletTransactionPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False


class WalletTransactionInlinePermissions(BaseWalletTransactionPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
