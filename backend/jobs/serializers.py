from rest_framework import serializers
from .models import Job, JobPhoto


class JobPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPhoto
        fields = "__all__"


class JobSerializer(serializers.ModelSerializer):
    photos = JobPhotoSerializer(many=True, read_only=True)
    client_name = serializers.CharField(source="client.full_name", read_only=True)
    client_address = serializers.CharField(source="client.address", read_only=True)
    client_phone = serializers.CharField(source="client.phone", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    photo_count = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = "__all__"

    def get_photo_count(self, obj):
        return obj.photos.count()


class JobListSerializer(serializers.ModelSerializer):
    """Lightweight for list views."""

    client_name = serializers.CharField(source="client.full_name", read_only=True)
    client_phone = serializers.CharField(source="client.phone", read_only=True)
    client_address = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    photo_count = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            "id",
            "client",
            "client_name",
            "client_phone",
            "client_address",
            "status",
            "status_display",
            "scheduled_date",
            "completed_date",
            "helpers",
            "photo_count",
            "created_at",
        ]

    def get_photo_count(self, obj):
        return obj.photos.count()

    def get_client_address(self, obj):
        if obj.location:
            return obj.location.address
        return ""
