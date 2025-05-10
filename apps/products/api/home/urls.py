from django.urls import path

from .views import HomeListView

urlpatterns = [
    path("home/", HomeListView.as_view(), name="home-list"),
]
