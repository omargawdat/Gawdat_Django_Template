from django.http import HttpRequest

from apps.payment.models.payment import Payment
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions


class BasePaymentPermissions:
    def get_field_config(
        self, request: HttpRequest, payment: Payment | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            "customer": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "price_before_discount_currency": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "price_before_discount": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "price_after_discount_currency": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "price_after_discount": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "payment_type": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "is_paid": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "payment_charge_id": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "bank_transaction_response": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "created_at": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
        }


class PaymentAdminPermissions(BasePaymentPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False


class PaymentInlinePermissions(BasePaymentPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
