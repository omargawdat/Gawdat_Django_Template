from django.urls import path

from apps.authentication.views import SendOtpView, VerifyOTPView

urlpatterns = [
    path('auth/send-otp/', SendOtpView.as_view(), name='send-otp'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='authenticate-user'),
]
