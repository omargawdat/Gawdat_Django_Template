import requests
from phonenumbers.phonenumber import PhoneNumber
from requests import Response

from apps.channel.domain.utilities.sms_helpers.base.base_class import OTPSenderBase
from config.settings.base import env


class OurSMSUtils(OTPSenderBase):
    @staticmethod
    def send_message(phone_numbers: list[PhoneNumber], message: str) -> Response:
        url = "https://api.oursms.com/msgs/sms/"
        headers = {
            "Authorization": f"Bearer {env.our_sms_api_key.get_secret_value()}",
            "Content-Type": "application/json",
        }

        payload = {
            "src": env.our_sms_src,
            "dests": [str(phone_number) for phone_number in phone_numbers],
            "body": message,
            "priority": 1,
            "validity": 3,
            "msgClass": "transactional",
        }

        return requests.post(url, headers=headers, json=payload, timeout=10)
