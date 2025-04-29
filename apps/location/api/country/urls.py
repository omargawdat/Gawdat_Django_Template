from django.urls import path

from .views import ActiveCountryList

urlpatterns = [
    path(
        "location/countries/", ActiveCountryList.as_view(), name="active-country-list"
    ),
]
