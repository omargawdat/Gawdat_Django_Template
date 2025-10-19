"""Custom signup form for django-allauth headless API."""

import logging

from django import forms

logger = logging.getLogger(__name__)


class CustomSignupForm(forms.Form):
    def signup(self, request, user):
        logger.info("Custom signup form called")
