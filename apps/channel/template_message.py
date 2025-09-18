from django.utils.translation import gettext_lazy as _

from apps.channel.constants import NotificationType
from apps.users.constants import UserType

notification_templates = {
    NotificationType.PRODUCT_ORDERED: {
        UserType.CUSTOMER: _(
            "Thank you for ordering {product}! Your order #{order_id} is being processed."
        ),
        UserType.PROVIDER: _(
            "New order #{order_id} for {product} is awaiting your confirmation."
        ),
    },
    NotificationType.REFERRAL_APP_INSTALL: {
        UserType.CUSTOMER: _(
            "Congratulations! You've earned {amount} for successfully referring a friend to our app. The money has been added to your wallet."
        ),
        UserType.PROVIDER: _(
            "A new customer has joined through your referral! You've earned {amount} which has been added to your wallet."
        ),
    },
    NotificationType.REFERRAL_FIRST_ORDER: {
        UserType.CUSTOMER: _(
            "Great news! Your referred friend has placed their first order. You've earned {amount} as a referral bonus!"
        ),
        UserType.PROVIDER: _(
            "Your referred customer has completed their first order! You've been rewarded {amount} for the successful referral."
        ),
    },
}
