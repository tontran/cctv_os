from django.contrib import admin
from .models import MaintenanceRequest


@admin.register(MaintenanceRequest)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = [
        "client",
        "issue_type",
        "status",
        "scheduled_date",
        "completed_date",
        "labour_cost",
    ]
    list_filter = ["status", "issue_type"]
    search_fields = ["client__first_name", "client__last_name", "description"]
    readonly_fields = ["created_at", "updated_at"]
