from django.contrib import admin
from .models import Job, JobPhoto


class JobPhotoInline(admin.TabularInline):
    model = JobPhoto
    extra = 0
    fields = ["photo", "photo_type", "caption"]
    readonly_fields = ["taken_at"]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "client",
        "status",
        "scheduled_date",
        "completed_date",
        "helpers",
    ]
    list_filter = ["status", "scheduled_date"]
    search_fields = ["client__first_name", "client__last_name", "notes"]
    inlines = [JobPhotoInline]


@admin.register(JobPhoto)
class JobPhotoAdmin(admin.ModelAdmin):
    list_display = ["job", "photo_type", "caption", "taken_at"]
    list_filter = ["photo_type"]
