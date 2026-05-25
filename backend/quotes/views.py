from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Quote, QuoteItem
from .serializers import QuoteSerializer, QuoteItemSerializer, QuoteClientSerializer


class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all().order_by("-created_at")
    serializer_class = QuoteSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "client"]
    search_fields = ["quote_number", "client__first_name", "client__last_name"]
    ordering_fields = ["created_at", "visit_date"]

    @action(detail=True, methods=["get"])
    def client_view(self, request, pk=None):
        """Client-safe view — hides labour and helper cost breakdown."""
        quote = self.get_object()
        serializer = QuoteClientSerializer(quote)
        return Response(serializer.data)


class QuoteItemViewSet(viewsets.ModelViewSet):
    queryset = QuoteItem.objects.all()
    serializer_class = QuoteItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "quote",
        "system_type",
        "camera_shape",
        "manufacturer",
        "connection_type",
    ]
