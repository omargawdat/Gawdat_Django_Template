from django.urls import path

from apps.location.api.region.views import RegionByPointView

urlpatterns = [
    path("regions/", RegionByPointView.as_view(), name="region-by-point"),
]
