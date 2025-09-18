from django.utils.translation import gettext_lazy as _

from apps.users.models.customer import Customer


class NotificationChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = []

    fieldsets = (
        (
            _("Notification 📢"),
            {
                "fields": ("notification_type", "title", "message_body"),
            },
        ),
        (
            _("Users 👥"),
            {
                "fields": ("users", "send_sms", "send_fcm"),
            },
        ),
    )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "users":
            kwargs["queryset"] = Customer.objects.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)
