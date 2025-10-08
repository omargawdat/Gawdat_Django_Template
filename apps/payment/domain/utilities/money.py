from djmoney.money import Money


class WalletUtilities:
    @staticmethod
    def to_money_obj(amount, currency):
        return Money(amount, currency)
