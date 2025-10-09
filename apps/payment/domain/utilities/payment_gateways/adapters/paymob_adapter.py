import uuid
from typing import Any

from config.settings.base import env

from ..base import PaymentAdapterBase
from ..data_class import ChargeResponse
from ..data_class import PaymentStatusCallback
from ..data_class import RefundResponse
from ..gateway_types import PaymentGatewayType
from ..Integrations.paymob import PaymobPaymentIntegration


class PaymobPaymentAdapter(PaymentAdapterBase):
    def __init__(self):
        self.secret_token = env("PAYMOB_SECRET_KEY")
        self.public_key = env("PAYMOB_PUBLIC_KEY")
        self.payment_confirmation_key = env("PAYMENT_CONFIRMATION_KEY")
        self.integration = PaymobPaymentIntegration()
        self.card_payment_method = env("PAYMOB_CARD_PAYMENT_METHOD")
        self.wallet_payment_method = env("PAYMOB_WALLET_PAYMENT_METHOD")

    def create_charge(
        self,
        amount: float,
        currency: str,
        phone_number: str,
        order_id: str,
        callback_url: str,
        redirect_url: str,
        first_name: str,
        last_name: str,
        card_token: str | None = None,
    ) -> ChargeResponse:
        amount_cent = amount * 100  # [IMPORTANT]: Convert amount to cents

        # 1) Call the raw integration method (HTTP request)
        raw_response = self.integration.create_charge_raw(
            secret_token=self.secret_token,
            amount_cents=str(float(amount_cent)),
            currency=str(currency),
            special_reference=str(uuid.uuid4())[:8],
            order_id=order_id,
            first_name=first_name,
            last_name=last_name,
            email="omargawdaat@gmail.com",
            phone_number=str(phone_number),
            payment_methods=[
                int(self.card_payment_method),
                int(self.wallet_payment_method),
            ],
            notification_url=callback_url,
            redirection_url=redirect_url,
            payment_confirmation=self.payment_confirmation_key,
            gateway_type=PaymentGatewayType.PAYMOB.value,
        )

        # 2) Build the unified checkout URL per your new requirement
        client_secret = raw_response.get("client_secret")
        payment_url = (
            f"https://accept.paymob.com/unifiedcheckout/"
            f"?publicKey={self.public_key}"
            f"&clientSecret={client_secret}"
        )

        # 4) Return a ChargeResponse
        return ChargeResponse(payment_url=payment_url)

    def extract_payment_callback(self, callback_data: dict) -> PaymentStatusCallback:
        obj = callback_data.get("obj", {})

        confirmation_key = str(
            obj.get("payment_key_claims", {})
            .get("extra", {})
            .get("payment_confirmation", "")
        )

        # Extract the original order ID from the environment-specific ID
        order_id = str(obj.get("payment_key_claims").get("extra").get("payment_id"))

        status = obj.get("data", {}).get("migs_order", {}).get("status", "")
        is_completed = obj.get("success", False)
        payment_gateway_id = str(obj.get("id", ""))

        return PaymentStatusCallback(
            order_id=order_id,  # Return the original order ID without environment prefix
            confirmation_key=confirmation_key,
            status=status,
            is_completed=is_completed,
            gateway_type=PaymentGatewayType.PAYMOB.value,
            payment_gateway_id=payment_gateway_id,
        )

    def refund_payment(
        self, transaction_id: str, amount_cents: int, currency: str
    ) -> RefundResponse:
        # Call the integration's raw refund
        raw_response = self.integration.refund_payment_raw(
            secret_token=self.secret_token,
            transaction_id=transaction_id,
            amount_cents=str(amount_cents),
        )

        return RefundResponse(
            is_success=raw_response.get("success"),
        )

    def get_charge_status(self, charge_id: str) -> Any:
        """
        Future: implement a status check endpoint if needed.
        """
        raise NotImplementedError(
            "Get charge status not implemented yet for PaymobPaymentAdapter."
        )
