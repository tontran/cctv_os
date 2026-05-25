from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Quote, QuoteItem


class QuoteItemInline(admin.TabularInline):
    model = QuoteItem
    extra = 1
    fields = [
        "manufacturer",
        "system_type",
        "camera_shape",
        "camera_color",
        "connection_type",
        "resolution",
        "quantity",
        "unit_price",
        "description",
    ]


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = [
        "quote_number",
        "client",
        "status",
        "total",
        "estimated_days",
        "created_at",
    ]
    list_filter = ["status"]
    search_fields = ["quote_number", "client__first_name", "client__last_name"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [QuoteItemInline]

    fieldsets = (
        (
            "Quote Info",
            {
                "fields": (
                    "client",
                    "quote_number",
                    "status",
                    "visit_date",
                    "valid_until",
                )
            },
        ),
        (
            "Internal Costs (NOT shown to client)",
            {
                "fields": ("labour_cost", "helper_cost", "internal_notes"),
                "classes": ("collapse",),
                "description": "These fields are NEVER shared with the client.",
            },
        ),
        (
            "Client-Facing Costs",
            {"fields": ("accessories_cost", "fuel_charge", "estimated_days", "notes")},
        ),
        (
            "Audit",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(QuoteItem)
class QuoteItemAdmin(admin.ModelAdmin):
    list_display = [
        "quote",
        "manufacturer",
        "system_type",
        "camera_shape",
        "camera_color",
        "quantity",
        "unit_price",
    ]
    list_filter = ["manufacturer", "system_type", "camera_shape", "connection_type"]
