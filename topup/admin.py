"""Admin interface for managing games and top-up products.
This module registers the Game and TopUpProduct models with the Django admin site,"""

from django.contrib import admin

from .models import Game, TopUpProduct


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Admin interface for managing games."""

    list_display = ("name", "game_id", "is_active")
    search_fields = ("name", "game_id")


@admin.register(TopUpProduct)
class TopUpProductAdmin(admin.ModelAdmin):
    """Admin interface for managing top-up products."""

    list_display = ("name", "price", "game")
    search_fields = ("name",)
