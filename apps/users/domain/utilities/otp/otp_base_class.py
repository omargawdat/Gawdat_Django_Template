from abc import ABC
from abc import abstractmethod

from phonenumbers import PhoneNumber


class OTPSenderBase(ABC):
    @staticmethod
    @abstractmethod
    def send_otp(phone_number: PhoneNumber) -> int | None:
        pass

    @staticmethod
    @abstractmethod
    def verify_otp(otp: str, verification_id: int) -> bool:
        pass
