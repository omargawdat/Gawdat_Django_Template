import json

import requests
from phonenumbers import PhoneNumber
from requests import Response

from apps.channel.domain.utilities.sms_helpers.base.base_class import OTPSenderBase
from config.settings.base import env


class SMSMisrUtils(OTPSenderBase):
    @staticmethod
    def send_message(phone_numbers: list[PhoneNumber], message: str) -> Response:
        url = "https://smsmisr.com/api/SMS/"
        headers = {
            "Content-Type": "application/json",
        }

        payload = json.dumps(
            {
                "environment": "1",
                "username": env.sms_misr_username,
                "password": env.sms_misr_password.get_secret_value(),
                "sender": env.sms_misr_sender,
                "mobile": ", ".join(str(n) for n in phone_numbers),
                "language": "2",
                "message": message,
            }
        )
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        return response
