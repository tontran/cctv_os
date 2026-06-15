from django.db import models


class Client(models.Model):

    class ClientType(models.TextChoices):
        RESIDENTIAL = "residential", "Residential"
        COMMERCIAL = "commercial", "Commercial"

    class LeadSource(models.TextChoices):
        REFERRAL = "referral", "Referral"
        GOOGLE = "google", "Google"
        FACEBOOK = "facebook", "Facebook"
        KIJIJI = "kijiji", "Kijiji"
        RETURNING = "returning", "Returning Customer"
        OTHER = "other", "Other"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, default="")
    client_type = models.CharField(
        max_length=20,
        choices=ClientType.choices,
        default=ClientType.RESIDENTIAL,
    )
    address = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=100, default="Kitchener")
    province = models.CharField(max_length=50, default="ON")
    postal_code = models.CharField(max_length=10, blank=True, default="")
    lead_source = models.CharField(
        max_length=20,
        choices=LeadSource.choices,
        default=LeadSource.OTHER,
    )
    notes = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.phone}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Location(models.Model):
    """
    A physical address belonging to a client.
    Residential clients typically have 1 location.
    Commercial clients can have many store locations.
    """

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="locations",
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Store or location name e.g. 'Downtown Branch', 'Main Office'",
    )
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, default="Kitchener")
    province = models.CharField(max_length=50, default="ON")
    postal_code = models.CharField(max_length=10, blank=True, default="")
    contact_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="On-site contact person if different from main client",
    )
    contact_phone = models.CharField(max_length=20, blank=True, default="")
    notes = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["client", "name"]

    def __str__(self):
        if self.name:
            return f"{self.client.full_name} — {self.name} ({self.address})"
        return f"{self.client.full_name} — {self.address}"

    @property
    def display_name(self):
        return self.name if self.name else self.address


class Lead(models.Model):

    class LeadStatus(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        QUOTE_SENT = "quote_sent", "Quote Sent"
        FOLLOW_UP = "follow_up", "Follow Up"
        WON = "won", "Won"
        LOST = "lost", "Lost"

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="leads",
    )
    status = models.CharField(
        max_length=20,
        choices=LeadStatus.choices,
        default=LeadStatus.NEW,
    )
    follow_up_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client.full_name} — {self.status}"

class CCTVSystem(models.Model):

    class CameraType(models.TextChoices):
        IP = "ip", "IP / Network"
        ANALOG = "analog", "Analog / HD"
        UNKNOWN = "unknown", "Unknown"

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="systems",
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="systems",
    )
    device_name = models.CharField(
        max_length=255,
        help_text="e.g. 'Main NVR', 'Outdoor DVR', 'Back Camera System'"
    )
    device_id = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Serial number or device ID"
    )
    username = models.CharField(max_length=100, blank=True, default="")
    password = models.CharField(max_length=100, blank=True, default="")
    camera_type = models.CharField(
        max_length=10,
        choices=CameraType.choices,
        default=CameraType.UNKNOWN,
    )
    client_port = models.CharField(
        max_length=10,
        blank=True,
        default="",
        help_text="e.g. 8080, 554, 80"
    )
    notes = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['location', 'device_name']

    def __str__(self):
        return f"{self.client.full_name} — {self.location.display_name} — {self.device_name}"