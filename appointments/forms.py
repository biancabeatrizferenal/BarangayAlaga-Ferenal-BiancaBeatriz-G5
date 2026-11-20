
from datetime import datetime, time, timedelta

from django import forms
from django.utils import timezone

from .models import Appointment


def get_appointment_time_choices():
    choices = [("", "Select Appointment Time")]

    current_hour = 9
    current_minute = 0

    while current_hour < 17 or (
        current_hour == 17 and current_minute == 0
    ):
        appointment_time = time(
            hour=current_hour,
            minute=current_minute,
        )

        if not (
            time(12, 0) <= appointment_time < time(13, 0)
        ):
            value = appointment_time.strftime("%H:%M")
            label = appointment_time.strftime("%I:%M %p")

            choices.append((value, label))

        current_minute += 30

        if current_minute == 60:
            current_hour += 1
            current_minute = 0

    return choices


class AppointmentForm(forms.ModelForm):

    appointment_time = forms.TypedChoiceField(
        label="Preferred Appointment Time",
        choices=get_appointment_time_choices,
        coerce=lambda value: (
            datetime.strptime(value, "%H:%M").time()
            if value
            else None
        ),
        empty_value=None,
        required=True,
        error_messages={
            "required": "Please select an appointment time.",
            "invalid_choice": "Please select a valid appointment time.",
        },
    )

    class Meta:
        model = Appointment

        fields = [
            "service_type",
            "appointment_date",
            "appointment_time",
            "reason",
        ]

        labels = {
            "service_type": "Healthcare Service",
            "appointment_date": "Preferred Appointment Date",
            "reason": "Reason for Appointment",
        }

        widgets = {
            "service_type": forms.Select(),
            "appointment_date": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d",
            ),
            "reason": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": (
                        "Briefly describe the reason for your visit."
                    ),
                }
            ),
        }

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data["appointment_date"]
        today = timezone.localdate()

        if appointment_date < today:
            raise forms.ValidationError(
                "Appointment date cannot be in the past."
            )

        if appointment_date > today + timedelta(days=90):
            raise forms.ValidationError(
                "Appointments can only be booked up to 90 days in advance."
            )

        return appointment_date

    def clean(self):
        cleaned_data = super().clean()

        appointment_date = cleaned_data.get("appointment_date")
        appointment_time = cleaned_data.get("appointment_time")

        if appointment_date and appointment_time:

            appointment_datetime = timezone.make_aware(
                datetime.combine(
                    appointment_date,
                    appointment_time,
                ),
                timezone.get_current_timezone(),
            )

            if appointment_datetime <= timezone.localtime():
                self.add_error(
                    "appointment_time",
                    "Please select a future appointment date and time.",
                )

            existing_appointments = Appointment.objects.filter(
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=[
                    Appointment.Status.PENDING,
                    Appointment.Status.CONFIRMED,
                    Appointment.Status.COMPLETED,
                ],
            )

            if self.instance.pk:
                existing_appointments = existing_appointments.exclude(
                    pk=self.instance.pk
                )

            if existing_appointments.exists():
                self.add_error(
                    "appointment_time",
                    (
                        "This appointment time is already booked. "
                        "Please select another available time."
                    ),
                )

        return cleaned_data
