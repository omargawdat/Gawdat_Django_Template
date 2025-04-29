from django.urls import path

from apps.location.api.region.views import RegionByPointView

urlpatterns = [
    path("region_by_point/", RegionByPointView.as_view(), name="region_by_point"),
]
