
from django.conf import settings
from django.db import models


class Appointment(models.Model):

    class ServiceType(models.TextChoices):
        GENERAL_CHECKUP = "general_checkup", "General Checkup"
        CONSULTATION = "consultation", "Medical Consultation"
        VACCINATION = "vaccination", "Vaccination"
        MATERNAL_CARE = "maternal_care", "Maternal Care"
        OTHER = "other", "Other Healthcare Service"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed"
        REJECTED = "rejected", "Rejected"
        CANCELLED = "cancelled", "Cancelled"

    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointments",
    )

    service_type = models.CharField(
        max_length=30,
        choices=ServiceType.choices,
    )

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.resident.username} - "
            f"{self.get_service_type_display()} - "
            f"{self.appointment_date}"
        )
