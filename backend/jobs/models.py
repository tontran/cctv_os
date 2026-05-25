from django.db import models
from quotes.models import Quote
from clients.models import Client, Location


class Job(models.Model):

    class JobStatus(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
        ON_HOLD = "on_hold", "On Hold"

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="jobs",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="jobs",
        help_text="Which client location this job is at",
    )
    quote = models.OneToOneField(
        Quote,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="job",
    )
    status = models.CharField(
        max_length=20,
        choices=JobStatus.choices,
        default=JobStatus.SCHEDULED,
    )
    scheduled_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    helpers = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Names of helpers e.g. Tung, Minh",
    )
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-scheduled_date"]

    def __str__(self):
        return f"Job #{self.id} — {self.client.full_name} ({self.status})"


class JobPhoto(models.Model):

    class PhotoType(models.TextChoices):
        SITE_VISIT = "site_visit", "Site Visit"
        BEFORE = "before", "Before Installation"
        DURING = "during", "During Installation"
        COMPLETION = "completion", "Completion"
        ISSUE = "issue", "Issue / Problem"

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    photo = models.ImageField(upload_to="job_photos/%Y/%m/")
    photo_type = models.CharField(
        max_length=20,
        choices=PhotoType.choices,
        default=PhotoType.COMPLETION,
    )
    caption = models.CharField(max_length=255, blank=True, default="")
    taken_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-taken_at"]

    def __str__(self):
        return f"{self.job} — {self.photo_type}"
