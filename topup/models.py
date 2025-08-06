"""Models for the top-up system, including games, products, and orders.
These models define the structure of the database tables used in the application."""

from django.db import models


class Game(models.Model):
    """Model representing a game in the top-up system."""

    name = models.CharField(max_length=100)
    game_id = models.CharField(max_length=100, db_index=True, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)  


class TopUpProduct(models.Model):
    """Model representing a top-up product for a game."""

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_game_currency = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)  


class TopUpOrder(models.Model):
    """Model representing a top-up order."""

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    )

    user_email = models.EmailField(db_index=True)
    product = models.ForeignKey(TopUpProduct, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_email} - {self.product.name}"
