from rest_framework import serializers

from apps.payment.models.payment import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "customer",
            "price_before_discount",
            "price_after_discount",
            "payment_type",
            "created_at",
        ]
