from rest_framework import viewsets, filters
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job, JobPhoto
from .serializers import JobSerializer, JobListSerializer, JobPhotoSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by("-scheduled_date")
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "client"]
    search_fields = ["client__first_name", "client__last_name", "notes", "helpers"]
    ordering_fields = ["scheduled_date", "completed_date", "created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return JobListSerializer
        return JobSerializer


class JobPhotoViewSet(viewsets.ModelViewSet):
    queryset = JobPhoto.objects.all().order_by("-taken_at")
    serializer_class = JobPhotoSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["job", "photo_type"]
