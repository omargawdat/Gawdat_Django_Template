# Channel App

## What It Provides
- Notification system with SMS and FCM (Firebase Cloud Messaging) delivery
- Template-based notifications customized by user type
- Multiple SMS provider support via factory pattern (Etisalat, OurSMS)
- REST API endpoints for notification management

## Dependencies
This app depends on:

1. **Users App**:
   - `User` model: Used for notification recipients
   - `UserSelector`: Used for grouping users by type and language
   - `UserType` constants: Used for notification templates
   - **Required Fields**:
     - Users must have the `language` field (already defined in the base User model)
     - Users must have `fcm_token` field for FCM notifications
     - Users must have `phone_number` field for SMS notifications

2. **Location App**:
   - `CountrySelector`: Used indirectly through the User app for phone number validation

## How to Use

```python
from apps.channel.domain.services.notification import NotificationService
from apps.channel.constants import NotificationType

# Send notification to users
NotificationService.create_action_notifications(
    users=users,                                    # List of user objects
    notification_type=NotificationType.PRODUCT_ORDERED,
    object_id=order.id,                             # Optional reference ID
    send_fcm=True,                                  # Enable push notification
    send_sms=True,                                  # Enable SMS
    # Template parameters:
    product="Product Name",
    order_id=12345,
)
```

Templates are defined in `constants.py` and use different messages based on user type:
```python
notification_templates = {
    NotificationType.PRODUCT_ORDERED: {
        UserType.CUSTOMER: _("Thank you for ordering {product}! Your order #{order_id} is being processed."),
        UserType.PROVIDER: _("New order #{order_id} for {product} is awaiting your confirmation."),
    },
}
```
