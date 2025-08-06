"""Serializers for the top-up application.
This module defines serializers for creating and validating top-up orders."""

from django.core.exceptions import MultipleObjectsReturned
from rest_framework import serializers

from .models import Game, TopUpOrder, TopUpProduct


class TopUpOrderSerializer(serializers.Serializer):
    """
    Serializer for creating and validating top-up orders.
    It validates game and product information based on user input,
    ensures data consistency, and handles related object lookup.
    """

    gamename = serializers.CharField()
    game_id = serializers.CharField()
    product_name = serializers.CharField()
    product_id = serializers.IntegerField()
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    user_email = serializers.EmailField()
    payment_status = serializers.ChoiceField(choices=TopUpOrder.STATUS_CHOICES)

    def validate(self, data):

        try:
            game = Game.objects.get(
                name=data["gamename"], game_id=data["game_id"], is_active=True
            )
        except Game.DoesNotExist:
            raise serializers.ValidationError(
                {"game_id": "No active game found with the provided name and ID."}
            )
        except MultipleObjectsReturned:
            raise serializers.ValidationError(
                {
                    "gamename": "Multiple games matched this name and ID. Please contact support."
                }
            )
        except Exception as exc:
            raise serializers.ValidationError("Something went wrong.") from exc

        try:
            product = TopUpProduct.objects.select_related("game").get(
                id=data["product_id"],
                name=data["product_name"],
                price=data["product_price"],
                game=game,
            )
        except TopUpProduct.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "product_id": "No matching product found for the specified game and details."
                }
            )
        except MultipleObjectsReturned:
            raise serializers.ValidationError(
                {"product_id": "Multiple products matched. Please contact support."}
            )
        except Exception as exc:
            raise serializers.ValidationError("Something went wrong.") from exc

        data["product"] = product
        return data

    def create(self, validated_data):
        try:
            return TopUpOrder.objects.create(
                user_email=validated_data["user_email"],
                product=validated_data["product"],
                status=validated_data["payment_status"],
            )
        except Exception:
            raise serializers.ValidationError(
                "Unable to create top-up order. Please try again later."
            )

    def update(self, instance, validated_data):
        pass
