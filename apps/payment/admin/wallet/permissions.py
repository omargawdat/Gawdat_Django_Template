from django.http import HttpRequest

from apps.payment.models.wallet import Wallet
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions

from ...fields.wallet import WalletFields


class BaseWalletPermissions:
    def get_field_rules(
        self, request: HttpRequest, wallet: Wallet | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            WalletFields.USER: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            WalletFields.BALANCE_CURRENCY: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            WalletFields.BALANCE: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            WalletFields.IS_USE_WALLET_IN_PAYMENT: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            WalletFields.LAST_UPDATE: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
        }


class WalletAdminPermissions(BaseWalletPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return True

    def can_delete(self, request, obj=None):
        return False


class WalletInlinePermissions(BaseWalletPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
