from django.db import models
from clients.models import Client, Location
from jobs.models import Job
from decimal import Decimal


class MaintenanceRequest(models.Model):

    class MaintenanceStatus(models.TextChoices):
        REQUESTED = "requested", "Requested"
        SCHEDULED = "scheduled", "Scheduled"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    class IssueType(models.TextChoices):
        CAMERA_DOWN = "camera_down", "Camera Not Working"
        POOR_IMAGE = "poor_image", "Poor Image Quality"
        OFFLINE = "offline", "System Offline"
        CABLE = "cable", "Cable Issue"
        NVR_DVR = "nvr_dvr", "NVR/DVR Issue"
        UPGRADE = "upgrade", "Upgrade Request"
        OTHER = "other", "Other"

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="maintenance_requests",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenance_requests",
        help_text="Which location needs maintenance",
    )
    original_job = models.ForeignKey(
        Job,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenance_requests",
        help_text="Original installation job",
    )
    issue_type = models.CharField(
        max_length=20,
        choices=IssueType.choices,
        default=IssueType.OTHER,
    )
    status = models.CharField(
        max_length=20,
        choices=MaintenanceStatus.choices,
        default=MaintenanceStatus.REQUESTED,
    )
    description = models.TextField()
    scheduled_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    labour_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client.full_name} — {self.issue_type} ({self.status})"
