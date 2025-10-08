from typing import Any

import requests


class TapPaymentIntegration:
    def _build_headers(self, secret_key: str) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def create_charge_raw(
        self,
        secret_key: str,
        confirmation_key: str,
        amount: str,
        currency: str,
        phone_country_code: int,
        phone_number: int,
        post_url: str,
        order_id: str,
        redirect_url: str,
        card_token: str,
        email: str,
        gateway_type: str,
        customer_id: str | None = None,
    ) -> dict[str, Any]:
        payload = {
            "amount": amount,
            "currency": currency,
            "customer_initiated": True,
            "threeDSecure": True,
            "save_card": False,
            "metadata": {
                "payment_confirmation": confirmation_key,
                "gateway_type": gateway_type,
            },
            "reference": {
                "order": order_id,
            },
            "source": {"id": card_token},
            "post": {"url": post_url},
            "redirect": {"url": redirect_url},
            "customer": {
                "first_name": "customer",
                "email": email,
                "phone": {"country_code": phone_country_code, "number": phone_number},
            },
        }

        if customer_id:
            payload["customer"]["id"] = customer_id

        response = requests.post(
            "https://api.tap.company/v2/charges/",
            json=payload,
            headers=self._build_headers(secret_key),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def refund_payment_raw(
        self, secret_key: str, charge_id: str, amount: float, currency: str, reason: str
    ) -> dict[str, Any]:
        payload = {
            "charge_id": charge_id,
            "amount": amount,
            "currency": currency,
            "reason": reason,
        }

        response = requests.post(
            "https://api.tap.company/v2/refunds/",
            json=payload,
            headers=self._build_headers(secret_key),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def get_charge_status_raw(self, secret_key: str, charge_id: str) -> dict[str, Any]:
        url = f"https://api.tap.company/v2/charges/{charge_id}/"
        response = requests.get(
            url, headers=self._build_headers(secret_key), timeout=30
        )
        response.raise_for_status()
        return response.json()
