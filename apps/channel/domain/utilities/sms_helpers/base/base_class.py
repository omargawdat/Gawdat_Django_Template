from abc import ABC
from abc import abstractmethod

from phonenumbers import PhoneNumber
from requests import Response


class OTPSenderBase(ABC):
    @staticmethod
    @abstractmethod
    def send_message(phone_numbers: list[PhoneNumber], message: str) -> Response:
        pass
