from rest_framework.generics import RetrieveAPIView

from apps.appInfo.models.about import AboutUs
from apps.appInfo.models.social import SocialAccount
from apps.appInfo.models.terms import TermsAndConditions

from .serializers import AboutUsSerializer
from .serializers import SocialAccountsSerializer
from .serializers import TermsAndConditionsSerializer


class SocialAccountsAPIView(RetrieveAPIView):
    serializer_class = SocialAccountsSerializer
    permission_classes = []

    def get_object(self):
        return SocialAccount.get_solo()


class AboutUsAPIView(RetrieveAPIView):
    serializer_class = AboutUsSerializer
    permission_classes = []

    @property
    def get_object(self):
        return AboutUs.get_solo()


class TermsAndConditionsAPIView(RetrieveAPIView):
    serializer_class = TermsAndConditionsSerializer
    permission_classes = []

    def get_object(self):
        return TermsAndConditions.get_solo()
