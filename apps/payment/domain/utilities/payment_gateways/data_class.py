from dataclasses import dataclass

from apps.payment.domain.utilities.payment_gateways.gateway_types import (
    PaymentGatewayType,
)


@dataclass
class ChargeResponse:
    payment_url: str
    payment_id: str


@dataclass
class PaymentStatusCallback:
    order_id: str
    confirmation_key: str
    status: str
    is_completed: bool
    payment_gateway_id: str
    gateway_type: PaymentGatewayType


@dataclass
class RefundResponse:
    is_success: bool


@dataclass
class ChargeStatusResponse:
    status: str
    payment_url: str
    is_paid: bool
