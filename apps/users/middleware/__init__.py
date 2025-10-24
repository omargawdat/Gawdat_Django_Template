"""Middleware for user profile management."""

from .profile_check import ProfileCompletionMiddleware

__all__ = ["ProfileCompletionMiddleware"]
