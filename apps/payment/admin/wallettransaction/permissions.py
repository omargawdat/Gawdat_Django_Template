from django.http import HttpRequest

from apps.payment.models.wallet_transaction import WalletTransaction
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions

from ...fields.wallet_transaction import WalletTransactionFields


class BaseWalletTransactionPermissions:
    def get_field_rules(
        self, request: HttpRequest, wallet_transaction: WalletTransaction | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            WalletTransactionFields.WALLET: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            WalletTransactionFields.TRANSACTION_TYPE: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            WalletTransactionFields.AMOUNT_CURRENCY: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            WalletTransactionFields.AMOUNT: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            WalletTransactionFields.CREATED_AT: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            WalletTransactionFields.ACTION_BY: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            WalletTransactionFields.TRANSACTION_NOTE: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            WalletTransactionFields.ATTACHMENT: FieldPermissions(
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
