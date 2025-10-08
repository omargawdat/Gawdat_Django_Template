from apps.payment.domain.services.payment import PaymentService
from apps.payment.domain.services.payment_methods.base.base import BasePaymentHandler


class OnlinePaymentHandler(BasePaymentHandler):
    def _handle_payment(self, payment, request=None, **kwargs):
        return PaymentService.initialize_online_payment(payment)
