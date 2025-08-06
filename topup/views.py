"""Views for the top-up application.
This module handles the creation of top-up orders and provides a dashboard view for analytics.
"""

from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.http import HttpResponseServerError
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TopUpOrder, TopUpProduct
from .serializers import TopUpOrderSerializer


class TopUpOrderView(APIView):
    """Handles creation of top-up orders."""

    def post(self, request):
        """Handle POST request to create an order."""
        try:
            serializer = TopUpOrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Top-up order created successfully"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {
                    "error": f"An unexpected error occurred,{str(e)}. Please try again later."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@staff_member_required
def dashboard_view(request):
    """Render the dashboard with analytics data."""
    """Displays top products, daily revenue, and failed payments."""

    try:
        top_products = (
            TopUpProduct.objects.select_related("game")
            .annotate(purchase_count=Count("topuporder"))
            .order_by("-purchase_count")[:5]
        )

        today = timezone.now().date()
        last_7_days = today - timedelta(days=6)
        daily_revenue = (
            TopUpOrder.objects.filter(
                status="success", created_at__date__gte=last_7_days
            )
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(revenue=Sum("product__price"))
            .order_by("day")
        )

        # Failed payments this month
        now = timezone.now()
        failed_payments = TopUpOrder.objects.filter(
            status="failed", created_at__year=now.year, created_at__month=now.month
        ).count()

        return render(
            request,
            "topup/dashboard.html",
            {
                "top_products": top_products,
                "daily_revenue": daily_revenue,
                "failed_payments": failed_payments,
            },
        )

    except Exception:
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )
