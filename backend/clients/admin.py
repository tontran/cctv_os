from django.contrib import admin
from .models import Client, Lead, Location, CCTVSystem


class LeadInline(admin.TabularInline):
    model = Lead
    extra = 0
    fields = ["status", "follow_up_date", "notes"]

class CCTVSystemInline(admin.TabularInline):
    model = CCTVSystem
    extra = 1
    fields = ['device_name', 'device_id', 'camera_type', 'username', 'password', 'client_port', 'is_active']

class LocationInline(admin.TabularInline):
    model = Location
    extra = 1
    fields = ["name", "address", "city", "contact_name", "contact_phone", "is_active"]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "phone",
        "client_type",
        "city",
        "lead_source",
        "is_active",
        "created_at",
    ]
    list_filter = ["client_type", "lead_source", "city", "is_active"]
    search_fields = ["first_name", "last_name", "phone", "email", "address"]
    inlines = [LocationInline, LeadInline]

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["client", "name", "address", "city", "is_active"]
    list_filter = ["city", "is_active"]
    search_fields = ["client__first_name", "client__last_name", "name", "address"]
    inlines = [CCTVSystemInline]

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ["client", "status", "follow_up_date", "created_at"]
    list_filter = ["status"]
    search_fields = ["client__first_name", "client__last_name"]

@admin.register(CCTVSystem)
class CCTVSystemAdmin(admin.ModelAdmin):
    list_display = ['client', 'location', 'device_name', 'camera_type', 'client_port', 'is_active']
    list_filter = ['camera_type', 'is_active']
    search_fields = ['client__first_name', 'client__last_name', 'device_name', 'device_id']