from rest_framework import serializers
from .models import Client, Lead, Location


class LocationSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="client.full_name", read_only=True)

    class Meta:
        model = Location
        fields = "__all__"


class LeadSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="client.full_name", read_only=True)

    class Meta:
        model = Lead
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    locations = LocationSerializer(many=True, read_only=True)
    leads = LeadSerializer(many=True, read_only=True)
    total_jobs = serializers.SerializerMethodField()
    total_quotes = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = "__all__"

    def get_total_jobs(self, obj):
        return obj.jobs.count()

    def get_total_quotes(self, obj):
        return obj.quotes.count()


class ClientListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Client
        fields = [
            "id",
            "full_name",
            "first_name",
            "last_name",
            "phone",
            "client_type",
            "city",
            "is_active",
            "created_at",
        ]
