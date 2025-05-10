import logging
from typing import TYPE_CHECKING

from phonenumbers import PhoneNumber

from apps.channel.domain.utilities.sms_helpers.base.factory import SMSProviderFactory
from config.helpers.env import env

if TYPE_CHECKING:
    from apps.channel.domain.utilities.sms_helpers.base.base_class import OTPSenderBase

logger = logging.getLogger(__name__)


class SMSUtils:
    @staticmethod
    def send_bulk_message(phone_numbers: list[PhoneNumber], message: str):
        """takes phone numbers and message and sends it to the appropriate provider"""
        if env.is_testing_sms:  # todo must be false to send a real otp
            logger.info("SMS sending is disabled in local environment.")
            return

        provider_to_phones: dict[OTPSenderBase, list[PhoneNumber]] = {}
        for phone in phone_numbers:
            provider = SMSProviderFactory.get_sms_provider_by_country(phone)
            if provider not in provider_to_phones:
                provider_to_phones[provider] = []
            provider_to_phones[provider].append(phone)

        for provider, phones in provider_to_phones.items():
            provider_name = provider.__class__.__name__
            try:
                provider.send_message(phones, message)
            except Exception:
                logger.exception(f"Failed to send message via {provider_name}")
