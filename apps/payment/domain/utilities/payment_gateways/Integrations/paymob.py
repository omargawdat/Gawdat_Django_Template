from typing import Any

import requests


class PaymobPaymentIntegration:
    def _build_headers(self, secret_token: str) -> dict[str, str]:
        return {
            "Authorization": f"Token {secret_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def create_charge_raw(
        self,
        secret_token: str,
        amount_cents: str,
        currency: str,
        special_reference: str,
        order_id: str,
        notification_url: str,
        redirection_url: str,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        gateway_type: str,
        payment_confirmation: str,
        payment_methods: list[int],
    ) -> dict[str, Any]:
        billing_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
        }

        payload = {
            "amount": amount_cents,
            "payment_methods": payment_methods,
            "currency": currency,
            "special_reference": special_reference,
            "billing_data": billing_data,
            "notification_url": notification_url,
            "redirection_url": redirection_url,
            "extras": {
                "payment_id": order_id,
                "payment_confirmation": payment_confirmation,
                "gateway_type": gateway_type,
            },
        }

        response = requests.post(
            "https://accept.paymob.com/v1/intention/",
            json=payload,
            headers=self._build_headers(secret_token),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def refund_payment_raw(
        self,
        secret_token: str,
        transaction_id: str,
        amount_cents: str,
    ) -> dict[str, Any]:
        payload = {"transaction_id": transaction_id, "amount_cents": amount_cents}

        response = requests.post(
            "https://accept.paymob.com/api/acceptance/void_refund/refund",
            json=payload,
            headers=self._build_headers(secret_token),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
