from django.db import models
from clients.models import Client, Location
from decimal import Decimal


class Quote(models.Model):

    class QuoteStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        SENT = "sent", "Sent to Client"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        EXPIRED = "expired", "Expired"

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="quotes",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quotes",
        help_text="Which client location this quote is for",
    )
    quote_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        max_length=20,
        choices=QuoteStatus.choices,
        default=QuoteStatus.DRAFT,
    )
    visit_date = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)

    # INTERNAL ONLY — never expose to client
    labour_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    helper_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    # Shared costs — visible to client
    accessories_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    fuel_charge = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    estimated_days = models.DecimalField(
        max_digits=4, decimal_places=1, default=Decimal("1.0")
    )

    notes = models.TextField(blank=True, default="")
    internal_notes = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def camera_total(self):
        return sum(item.subtotal for item in self.items.all()) or Decimal("0.00")

    @property
    def installation_labour(self):
        """Combined labour shown to client — hides breakdown."""
        return self.labour_cost + self.helper_cost

    @property
    def subtotal(self):
        return (
            self.camera_total
            + self.installation_labour
            + self.accessories_cost
            + self.fuel_charge
        )

    @property
    def hst(self):
        return round(self.subtotal * Decimal("0.13"), 2)

    @property
    def total(self):
        return round(self.subtotal + self.hst, 2)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Quote #{self.quote_number} — {self.client.full_name}"


class QuoteItem(models.Model):

    class Manufacturer(models.TextChoices):
        LOREX = "lorex", "Lorex"
        REOLINK = "reolink", "Reolink"
        HIKVISION = "hikvision", "Hikvision"
        DAHUA = "dahua", "Dahua"
        AXIS = "axis", "Axis"
        HANWHA = "hanwha", "Hanwha"
        UNIVIEW = "uniview", "Uniview"
        OTHER = "other", "Other"

    class SystemType(models.TextChoices):
        IP = "ip", "IP / Network"
        ANALOG = "analog", "Analog / HD"

    class CameraShape(models.TextChoices):
        BULLET = "bullet", "Bullet"
        DOME = "dome", "Dome"
        TURRET = "turret", "Turret"
        PTZ = "ptz", "PTZ"

    class CameraColor(models.TextChoices):
        BLACK = "black", "Black"
        WHITE = "white", "White"

    class ConnectionType(models.TextChoices):
        WIRED = "wired", "Wired"
        WIRELESS = "wireless", "Wireless"

    quote = models.ForeignKey(
        Quote,
        on_delete=models.CASCADE,
        related_name="items",
    )
    manufacturer = models.CharField(
        max_length=20,
        choices=Manufacturer.choices,
        default=Manufacturer.OTHER,
    )
    system_type = models.CharField(
        max_length=10,
        choices=SystemType.choices,
        default=SystemType.IP,
    )
    camera_shape = models.CharField(
        max_length=10,
        choices=CameraShape.choices,
        default=CameraShape.BULLET,
    )
    camera_color = models.CharField(
        max_length=10,
        choices=CameraColor.choices,
        default=CameraColor.WHITE,
    )
    connection_type = models.CharField(
        max_length=10,
        choices=ConnectionType.choices,
        default=ConnectionType.WIRED,
    )
    resolution = models.CharField(max_length=20, blank=True, default="4MP")
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, default="")

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.quantity}x {self.manufacturer} {self.camera_color} {self.camera_shape} ({self.system_type})"
