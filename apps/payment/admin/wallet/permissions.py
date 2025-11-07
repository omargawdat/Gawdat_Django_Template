from django.http import HttpRequest

from apps.payment.models.wallet import Wallet
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions


class BaseWalletPermissions:
    def get_field_config(
        self, request: HttpRequest, wallet: Wallet | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            "user": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "balance_currency": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "balance": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "is_use_wallet_in_payment": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "last_update": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
        }


class WalletAdminPermissions(BaseWalletPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False


class WalletInlinePermissions(BaseWalletPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
