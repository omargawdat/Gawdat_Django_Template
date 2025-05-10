from django.db import models
from djmoney.models.fields import MoneyField
from simple_history.models import HistoricalRecords

from apps.users.models import User


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = MoneyField(max_digits=14, decimal_places=2)
    is_use_wallet_in_payment = models.BooleanField(default=True)
    last_update = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.user}'s Wallet"
