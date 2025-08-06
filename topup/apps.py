"""Configuration for the top-up application.
This module defines the application configuration for the top-up app,"""

from django.apps import AppConfig


class TopupConfig(AppConfig):
    """Configuration for the top-up application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "topup"
