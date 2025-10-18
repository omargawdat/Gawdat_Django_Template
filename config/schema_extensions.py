"""
OpenAPI authentication extensions for drf-spectacular.

These extensions tell drf-spectacular how to document custom authentication
classes in the OpenAPI schema. Without these, drf-spectacular will emit warnings
and ignore the authentication classes.
"""

from drf_spectacular.extensions import OpenApiAuthenticationExtension


class XSessionTokenScheme(OpenApiAuthenticationExtension):
    """OpenAPI extension for django-allauth headless XSessionTokenAuthentication."""

    target_class = "allauth.headless.contrib.rest_framework.authentication.XSessionTokenAuthentication"
    name = "XSessionTokenAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "X-Session-Token",
            "description": "Session token from django-allauth headless authentication",
        }


class SessionAuthenticationScheme(OpenApiAuthenticationExtension):
    """OpenAPI extension for Django REST Framework SessionAuthentication."""

    target_class = "rest_framework.authentication.SessionAuthentication"
    name = "SessionAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "cookie",
            "name": "sessionid",
            "description": "Django session cookie",
        }
