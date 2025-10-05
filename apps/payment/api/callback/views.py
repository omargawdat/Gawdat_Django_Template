from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payment.domain.services.payment import PaymentService
from apps.payment.domain.utilities.payment_gateways.adapters.tap_adapter import (
    TapPaymentAdapter,
)
from apps.payment.domain.utilities.payment_gateways.factory import PaymentGatewayFactory
from apps.payment.models.payment import Payment
from config.settings.base import env


@csrf_exempt
@xframe_options_exempt
def redirect_url(request):
    tap_id = request.GET.get("tap_id")
    integration_id = request.GET.get("id")
    is_success = False
    transaction_id = "unknown"

    if tap_id:
        transaction_id = tap_id
        charge_status = TapPaymentAdapter().get_charge_status(tap_id)
        is_success = charge_status.is_paid

    elif integration_id:
        is_success = request.GET.get("success", "false").lower() == "true"
        transaction_id = integration_id

    return HttpResponseRedirect(
        f"status?is_success={str(is_success).lower()}&id={transaction_id}"
    )


@xframe_options_exempt
def status_page(request):
    context = {
        "status": request.GET.get("is_success"),
        "transaction_id": request.GET.get("id"),
    }
    return render(request, "payment/status.html", context)


@extend_schema(exclude=True)
class BankCallbackAPI(APIView):
    permission_classes = []
    authentication_classes = []

    @transaction.atomic
    def post(self, request):
        payment_gateway = PaymentGatewayFactory.create_payment_gateway(
            callback_data=request.data
        )
        payment_status = payment_gateway.extract_payment_callback(request.data)

        if (
            payment_status.confirmation_key
            != env.payment_confirmation_key.get_secret_value()
        ):
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        payment_id = payment_status.order_id
        payment = Payment.objects.select_for_update().get(id=payment_id)

        payment.bank_transaction_response = request.data
        payment.save(update_fields=["bank_transaction_response"])

        if payment_status.is_completed:
            PaymentService.mark_payment_as_completed(payment=payment)

        return Response({}, status=status.HTTP_200_OK)
