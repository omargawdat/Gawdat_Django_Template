import secrets
from datetime import UTC
from datetime import datetime
from datetime import timedelta


class GenerateOTP:
    @staticmethod
    def generate_otp(length: int = 6) -> str:
        return "".join([str(secrets.randbelow(10)) for _ in range(length)])

    @staticmethod
    def store_otp_in_session(session, email, otp, expiry_minutes=10):
        session["otp_data"] = {
            "email": email,
            "otp": otp,
            "expires_at": (
                datetime.now(UTC) + timedelta(minutes=expiry_minutes)
            ).isoformat(),
            "attempts": 0,
        }
        session.modified = True

    @staticmethod
    def validate_otp(session, email, otp, max_attempts=5):
        otp_data = session.get("otp_data")
        if not otp_data:
            return False, "No OTP code stored"

        if otp_data["email"] != email:
            return False, "Email does not match"

        if otp_data["attempts"] >= max_attempts:
            return False, "Maximum attempts exceeded"

        expires_at = datetime.fromisoformat(otp_data["expires_at"])
        if datetime.now(UTC) > expires_at:
            return False, "Code has expired"

        # Increment attempts counter
        otp_data["attempts"] += 1
        session["otp_data"] = otp_data
        session.modified = True

        if otp_data["otp"] != otp:
            return False, "Invalid code"

        return True, "Verification successful"
