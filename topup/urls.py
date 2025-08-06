"""URL configuration for the top-up application.
This module defines the URL patterns for the top-up API and dashboard views."""

from django.urls import path

from .views import TopUpOrderView, dashboard_view

urlpatterns = [
    path("api/topup/", TopUpOrderView.as_view(), name="topup-api"),
    path("dashboard/", dashboard_view, name="dashboard"),
]
