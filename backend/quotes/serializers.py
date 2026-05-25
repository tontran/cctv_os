from rest_framework import serializers
from .models import Quote, QuoteItem


class QuoteItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.ReadOnlyField()
    manufacturer_display = serializers.CharField(
        source="get_manufacturer_display", read_only=True
    )
    system_type_display = serializers.CharField(
        source="get_system_type_display", read_only=True
    )
    camera_shape_display = serializers.CharField(
        source="get_camera_shape_display", read_only=True
    )

    class Meta:
        model = QuoteItem
        fields = "__all__"


class QuoteSerializer(serializers.ModelSerializer):
    """Full internal serializer — shows labour + helper breakdown."""

    items = QuoteItemSerializer(many=True, read_only=True)
    camera_total = serializers.ReadOnlyField()
    installation_labour = serializers.ReadOnlyField()
    subtotal = serializers.ReadOnlyField()
    hst = serializers.ReadOnlyField()
    total = serializers.ReadOnlyField()
    client_name = serializers.CharField(source="client.full_name", read_only=True)
    client_address = serializers.CharField(source="client.address", read_only=True)
    client_phone = serializers.CharField(source="client.phone", read_only=True)
    client_type = serializers.CharField(source="client.client_type", read_only=True)

    class Meta:
        model = Quote
        fields = "__all__"


class QuoteClientSerializer(serializers.ModelSerializer):
    """Client-facing serializer — hides labour/helper breakdown."""

    items = QuoteItemSerializer(many=True, read_only=True)
    camera_total = serializers.ReadOnlyField()
    installation_labour = serializers.ReadOnlyField()
    subtotal = serializers.ReadOnlyField()
    hst = serializers.ReadOnlyField()
    total = serializers.ReadOnlyField()
    client_name = serializers.CharField(source="client.full_name", read_only=True)
    client_address = serializers.CharField(source="client.address", read_only=True)
    client_phone = serializers.CharField(source="client.phone", read_only=True)

    class Meta:
        model = Quote
        # Explicitly excludes labour_cost, helper_cost, internal_notes
        fields = [
            "id",
            "client",
            "client_name",
            "client_address",
            "client_phone",
            "quote_number",
            "status",
            "visit_date",
            "valid_until",
            "items",
            "camera_total",
            "installation_labour",
            "accessories_cost",
            "fuel_charge",
            "estimated_days",
            "subtotal",
            "hst",
            "total",
            "notes",
            "created_at",
        ]
