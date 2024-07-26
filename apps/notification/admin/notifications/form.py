from django.forms import ModelForm

from apps.notification.models.notification import Notification


class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = "__all__"
