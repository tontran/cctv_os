from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Client, Lead, Location, CCTVSystem
from .serializers import (
    ClientSerializer, ClientListSerializer,
    LeadSerializer, LocationSerializer, CCTVSystemSerializer
)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by("-created_at")
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["client_type", "lead_source", "is_active", "city"]
    search_fields = ["first_name", "last_name", "phone", "email", "address"]
    ordering_fields = ["created_at", "first_name", "last_name"]

    def get_serializer_class(self):
        if self.action == "list":
            return ClientListSerializer
        return ClientSerializer

    @action(detail=True, methods=["get"])
    def jobs(self, request, pk=None):
        from jobs.serializers import JobListSerializer

        client = self.get_object()
        jobs = client.jobs.all().order_by("-scheduled_date")
        serializer = JobListSerializer(jobs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def quotes(self, request, pk=None):
        from quotes.serializers import QuoteSerializer

        client = self.get_object()
        quotes = client.quotes.all().order_by("-created_at")
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by("client", "name")
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["client", "is_active", "city"]
    search_fields = ["name", "address", "client__first_name", "client__last_name"]


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by("-created_at")
    serializer_class = LeadSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["status", "client"]
    ordering_fields = ["created_at", "follow_up_date"]


class CCTVSystemViewSet(viewsets.ModelViewSet):
    queryset = CCTVSystem.objects.all().order_by('client', 'location', 'device_name')
    serializer_class = CCTVSystemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['client', 'location', 'camera_type', 'is_active']
    search_fields = ['device_name', 'device_id', 'client__first_name', 'client__last_name']