from abc import ABC
from abc import abstractmethod
from typing import Any

from apps.payment.domain.utilities.payment_gateways.data_class import ChargeResponse
from apps.payment.domain.utilities.payment_gateways.data_class import (
    PaymentStatusCallback,
)
from apps.payment.domain.utilities.payment_gateways.data_class import RefundResponse


class PaymentAdapterBase(ABC):
    """Defines the interface for any payment adapter."""

    @abstractmethod
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
        pass

    @abstractmethod
    def extract_payment_callback(self, callback_data: dict) -> PaymentStatusCallback:
        pass

    @abstractmethod
    def refund_payment(
        self,
        transaction_id: str,
        amount_cents: int,
        currency: str,
    ) -> RefundResponse:
        pass

    @abstractmethod
    def get_charge_status(self, charge_id: str) -> Any:
        pass
