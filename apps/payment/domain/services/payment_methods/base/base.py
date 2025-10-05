from abc import ABC
from abc import abstractmethod


class BasePaymentHandler(ABC):
    def process_payment(self, payment, request=None, **kwargs):
        return self._handle_payment(payment, request=request, **kwargs)

    @abstractmethod
    def _handle_payment(self, payment, **kwargs):
        pass
