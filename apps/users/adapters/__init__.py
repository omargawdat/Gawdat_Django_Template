"""Custom adapters for django-allauth."""

from .account import CustomAccountAdapter
from .headless import CustomHeadlessAdapter

__all__ = ["CustomAccountAdapter", "CustomHeadlessAdapter"]
