from unfold.decorators import display

from apps.payment.models.wallet import Wallet


class WalletDisplayMixin:
    @display(description="wallet", header=True)
    def display_header(self, wallet: Wallet):
        """Display header with image if available."""
        return [
            wallet.pk,
            "",
            "O",
            {
                "path": wallet.image.url
                if hasattr(wallet, "image") and wallet.image
                else None
            },
        ]
