from django.apps import AppConfig


class ChannelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.channel"

    def ready(self):
        import apps.channel.signals  # noqa
