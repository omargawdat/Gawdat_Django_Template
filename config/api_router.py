from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from template.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()
app_name = "api"
urlpatterns = router.urls
