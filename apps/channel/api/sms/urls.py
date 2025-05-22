from django.urls import path

from apps.channel.api.sms.views import OTPSendView

urlpatterns = [
    path("sms/send-auth-otp/", OTPSendView.as_view(), name="sms-send-auth-otp"),
]
