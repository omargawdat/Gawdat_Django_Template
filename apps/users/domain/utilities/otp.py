import secrets
import string


class OTPUtility:
    @staticmethod
    def generate_otp(length: str = 5) -> str:
        otp = "".join(secrets.choice(string.digits) for _ in range(length))
        return otp
