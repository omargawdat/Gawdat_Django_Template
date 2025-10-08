from enum import Enum

from apps.payment.domain.utilities.payment_gateways.adapters.tap_adapter import (
    TapPaymentAdapter,
)
from apps.payment.domain.utilities.payment_gateways.base import PaymentAdapterBase
from apps.payment.domain.utilities.payment_gateways.gateway_types import (
    PaymentGatewayType,
)


class Currency(Enum):
    SAR = "SAR"


class PaymentGatewayFactory:
    TAP_CURRENCIES = [
        Currency.SAR,
    ]

    @staticmethod
    def get_gateway_type_from_currency(currency: str) -> PaymentGatewayType:
        currency = Currency[str(currency).upper()]
        if currency in PaymentGatewayFactory.TAP_CURRENCIES:
            return PaymentGatewayType.TAP
        raise ValueError(f"Unsupported currency: {currency}")

    @staticmethod
    def get_gateway_type_from_callback(callback_data: dict) -> PaymentGatewayType:
        """Determine payment gateway type from callback data."""

        # Check Tap metadata
        if gateway_type := callback_data.get("metadata", {}).get("gateway_type"):
            if gateway_type == PaymentGatewayType.TAP.value:
                return PaymentGatewayType.TAP

        raise ValueError("Unable to determine payment gateway type from callback data")

    @staticmethod
    def create_payment_gateway(
        currency: str | None = None, callback_data: dict | None = None
    ) -> PaymentAdapterBase:
        if callback_data:
            gateway_type = PaymentGatewayFactory.get_gateway_type_from_callback(
                callback_data
            )
        elif currency:
            gateway_type = PaymentGatewayFactory.get_gateway_type_from_currency(
                currency
            )
        else:
            raise ValueError(
                "Data must be either callback data (dict) or currency (str)"
            )

        if gateway_type == PaymentGatewayType.TAP:
            return TapPaymentAdapter()

        else:
            raise ValueError(f"Unsupported payment gateway type: {gateway_type}")
