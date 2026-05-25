from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import MaintenanceRequest
from .serializers import MaintenanceRequestSerializer


class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all().order_by("-created_at")
    serializer_class = MaintenanceRequestSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "issue_type", "client"]
    search_fields = ["client__first_name", "client__last_name", "description"]
    ordering_fields = ["created_at", "scheduled_date"]
