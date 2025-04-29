from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView

from apps.appInfo.api.info.serializers import AppInfoSerializer
from apps.appInfo.api.info.serializers import FAQSerializer
from apps.appInfo.api.info.serializers import SocialAccountsSerializer
from apps.appInfo.models.app_info import AppInfo
from apps.appInfo.models.faq import FAQ
from apps.appInfo.models.social import SocialAccount


class SocialAccountsAPIView(RetrieveAPIView):
    serializer_class = SocialAccountsSerializer
    permission_classes = []

    def get_object(self):
        return SocialAccount.get_solo()


class AppInfoAPIView(RetrieveAPIView):
    serializer_class = AppInfoSerializer
    permission_classes = []

    def get_object(self):
        return AppInfo.get_solo()


class FAQListView(ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = []
    authentication_classes = []
