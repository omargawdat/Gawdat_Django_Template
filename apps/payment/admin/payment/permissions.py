from django.http import HttpRequest

from apps.payment.models.payment import Payment
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions

from ...fields.payment import PaymentFields


class BasePaymentPermissions:
    def get_field_rules(
        self, request: HttpRequest, payment: Payment | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            PaymentFields.CUSTOMER: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            PaymentFields.PRICE_BEFORE_DISCOUNT_CURRENCY: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            PaymentFields.PRICE_BEFORE_DISCOUNT: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            PaymentFields.PRICE_AFTER_DISCOUNT_CURRENCY: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            PaymentFields.PRICE_AFTER_DISCOUNT: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            PaymentFields.PAYMENT_TYPE: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            PaymentFields.IS_PAID: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            PaymentFields.PAYMENT_CHARGE_ID: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            PaymentFields.BANK_TRANSACTION_RESPONSE: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            PaymentFields.CREATED_AT: FieldPermissions(
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
