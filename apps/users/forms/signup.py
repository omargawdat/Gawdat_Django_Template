"""Custom signup form for django-allauth headless API."""

from django import forms


class CustomSignupForm(forms.Form):
    def signup(self, request, user):
        pass
