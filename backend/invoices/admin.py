from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "invoice_number",
        "client",
        "status",
        "total",
        "due_date",
        "paid_date",
        "payment_method",
    ]
    list_filter = ["status", "payment_method"]
    search_fields = ["invoice_number", "client__first_name", "client__last_name"]
    readonly_fields = ["created_at", "updated_at"]
