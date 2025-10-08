import phonenumbers

from apps.payment.domain.utilities.payment_gateways.base import PaymentAdapterBase
from apps.payment.domain.utilities.payment_gateways.data_class import ChargeResponse
from apps.payment.domain.utilities.payment_gateways.data_class import (
    ChargeStatusResponse,
)
from apps.payment.domain.utilities.payment_gateways.data_class import (
    PaymentStatusCallback,
)
from apps.payment.domain.utilities.payment_gateways.data_class import RefundResponse
from apps.payment.domain.utilities.payment_gateways.gateway_types import (
    PaymentGatewayType,
)
from apps.payment.domain.utilities.payment_gateways.Integrations.tap import (
    TapPaymentIntegration,
)
from config.settings.base import env


class TapPaymentAdapter(PaymentAdapterBase):
    def __init__(self):
        self.integration = TapPaymentIntegration()
        self.secret_key = env.taps_secret_key.get_secret_value()
        self.confirmation_key = env.payment_confirmation_key.get_secret_value()

    def create_charge(
        self,
        amount: str,
        currency: str,
        phone_number: str,
        callback_url: str,
        redirect_url: str,
        order_id: str,
        first_name: str = "N/A",
        last_name: str = "N/A",
        customer_id: str | None = None,
        card_token: str = "src_all",  # noqa: S107
    ) -> ChargeResponse:
        phone_parsed = phonenumbers.parse(str(phone_number))

        raw_response = self.integration.create_charge_raw(
            secret_key=self.secret_key,
            confirmation_key=self.confirmation_key,
            amount=str(float(amount)),
            currency=currency,
            phone_country_code=phone_parsed.country_code,
            phone_number=phone_parsed.national_number,
            post_url=callback_url,
            order_id=order_id,
            redirect_url=redirect_url,
            card_token=card_token,
            email="omargawdaat@gmail.com",
            customer_id=customer_id,
            gateway_type=PaymentGatewayType.TAP.value,
        )

        payment_url = raw_response.get("transaction", {}).get("url", "")
        payment_id = raw_response.get("id")
        return ChargeResponse(payment_url=payment_url, payment_id=payment_id)

    def extract_payment_callback(self, callback_data: dict) -> PaymentStatusCallback:
        return PaymentStatusCallback(
            order_id=callback_data.get("reference", {}).get("order"),
            confirmation_key=callback_data.get("metadata", {}).get(
                "payment_confirmation"
            ),
            status=callback_data.get("status"),
            is_completed=callback_data.get("status", "").upper() == "CAPTURED",
            payment_gateway_id=callback_data.get("id"),
            gateway_type=PaymentGatewayType.TAP.value,
        )

    def refund_payment(
        self, transaction_id: str, amount: float, currency: str
    ) -> RefundResponse:
        raw_response = self.integration.refund_payment_raw(
            secret_key=self.secret_key,
            charge_id=transaction_id,
            amount=amount,
            currency=currency,
            reason="Refund requested",
        )
        status = raw_response.get("status", "FAILED")
        return RefundResponse(is_success=status in ["REFUNDED", "ACCEPTED"])

    def get_charge_status(self, charge_id: str) -> ChargeStatusResponse:
        raw_data = self.integration.get_charge_status_raw(
            secret_key=self.secret_key, charge_id=charge_id
        )
        return ChargeStatusResponse(
            status=raw_data.get("status", ""),
            payment_url=raw_data.get("transaction", {}).get("url", ""),
            is_paid=raw_data.get("status", "").upper() == "CAPTURED",
        )
