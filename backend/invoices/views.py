from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Invoice
from .serializers import InvoiceSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by("-created_at")
    serializer_class = InvoiceSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "client", "payment_method"]
    search_fields = ["invoice_number", "client__first_name", "client__last_name"]
    ordering_fields = ["created_at", "due_date", "paid_date", "total"]
