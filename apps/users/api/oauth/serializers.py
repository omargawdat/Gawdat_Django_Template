from dj_rest_auth.registration.serializers import SocialLoginSerializer

from apps.payment.domain.services.wallet import WalletService


class CustomSocialLoginSerializer(SocialLoginSerializer):
    def get_social_login(self, adapter, app, token, response):
        login = super().get_social_login(adapter, app, token, response)
        referral_id = self.context["request"].data.get("referral_customer_id")
        if referral_id:
            login.state["referral_customer_id"] = referral_id
        return login

    def post_signup(self, login, attrs):
        referral_id = login.state.get("referral_customer_id")
        if referral_id:
            customer = login.account.user  # newly created Customer
            customer.referral_customer_id = referral_id
            customer.save(update_fields=["referral_customer_id"])

            # Now award referral points
            WalletService.add_referral_points(
                referral_customer_id=referral_id,
                request_customer=customer,
            )
        return super().post_signup(login, attrs)
