from django.urls import path

from .views import ActiveCountryList

urlpatterns = [
    path("countries/", ActiveCountryList.as_view(), name="countries-list"),
]
