import logging

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.payment.domain.utilities.payment_gateways.factory import PaymentGatewayFactory
from apps.payment.models.payment import Payment
from config.helpers.env import env

logger = logging.getLogger(__name__)


class PaymentService:
    @staticmethod
    @transaction.atomic
    def initialize_online_payment(payment: Payment) -> str:
        if not payment:
            raise ValidationError("No payments provided")

        customer = payment.customer
        amount_to_be_paid = payment.price_after_discount
        currency = str(amount_to_be_paid.currency)

        payment_gateway = PaymentGatewayFactory.create_payment_gateway(
            currency=currency
        )

        if env.environment in ["local", "development"]:
            currency = "KWD"  # todo: remove this code

        domain_name = env.domain_name
        domain_url = f"https://{domain_name}"
        charge_response = payment_gateway.create_charge(
            amount=amount_to_be_paid.amount,
            currency=currency,
            phone_number=customer.phone_number,
            first_name=customer.username,
            last_name=customer.username,
            order_id=str(payment.id),
            callback_url=f"{domain_url}/api/bank-callback-checkout/",
            redirect_url=f"{domain_url}/api/redirect_url/",
        )

        # Save the payment ID from the gateway response
        payment.payment_charge_id = charge_response.payment_id
        payment.save()

        return charge_response.payment_url

    @staticmethod
    @transaction.atomic
    def mark_payment_session_as_completed(payment: Payment) -> None:
        if payment.is_paid:
            return  # Already completed

        # Mark payment as paid
        payment.is_paid = True
        payment.save(update_fields=["is_paid"])
