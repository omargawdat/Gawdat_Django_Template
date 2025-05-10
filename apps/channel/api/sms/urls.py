from django.urls import path

from apps.channel.api.sms.views import OTPSendView

urlpatterns = [
    path("send-auth-otp/", OTPSendView.as_view(), name="send-otp"),
]
