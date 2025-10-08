from import_export import resources

from apps.payment.models.payment import Payment


class PaymentResource(resources.ModelResource):
    class Meta:
        model = Payment
        fields = []
