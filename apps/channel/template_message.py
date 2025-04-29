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
}
