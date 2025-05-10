from modeltranslation.translator import TranslationOptions
from modeltranslation.translator import register

from apps.channel.models.notification import Notification


@register(Notification)
class NotificationTranslationOptions(TranslationOptions):
    fields = ("title", "message_body")
