from phonenumbers import PhoneNumber
from requests import Response

from apps.channel.domain.utilities.sms_helpers.base.base_class import OTPSenderBase


class EtisalatSMSUtils(OTPSenderBase):
    @staticmethod
    def send_message(phone_numbers: list[PhoneNumber], message: str) -> Response:
        pass
        # url = env.etisalat_sms_api_url
        #
        # template_id = env.etisalat_sms_template_id
        # api_key = env.etisalat_sms_api_key.get_secret_value()
        # authentication = env.etisalat_sms_authentication.get_secret_value()
        # headers = {
        #     "Authorization": f"Basic {api_key}",
        #     "x-Gateway-APIKey": env.etisalat_x_gateway_api_key.get_secret_value(),
        #     "Content-Type": "application/json",
        # }
        #
        # payload = {
        #     "id": str(uuid.uuid4()),
        #     "messageType": "SMS",
        #     "characteristic": [
        #         {"name": "Authorization", "value": authentication},
        #         {"name": "templateID", "value": template_id},
        #         {"name": "body", "value": message},
        #     ],
        #     "receiver": [
        #         {
        #             "phoneNumber": str(phone_number).replace("+", ""),
        #         }
        #         for phone_number in phone_numbers
        #     ],
        # }
        #
        # cert_file = "certificate.pem"
        # key_file = "private_key.pem"
        #
        # return requests.post(
        #     url, headers=headers, json=payload, cert=(cert_file, key_file), timeout=20
        # )
