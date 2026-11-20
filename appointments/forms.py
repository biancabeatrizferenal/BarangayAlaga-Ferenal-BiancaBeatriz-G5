
from datetime import timedelta

from django import forms
from django.utils import timezone

from .models import Appointment


class AppointmentForm(forms.ModelForm):

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
            "appointment_time": "Preferred Appointment Time",
            "reason": "Reason for Appointment",
        }

        widgets = {
            "service_type": forms.Select(),
            "appointment_date": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d",
            ),
            "appointment_time": forms.TimeInput(
                attrs={"type": "time"},
                format="%H:%M",
            ),
            "reason": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Briefly describe the reason for your visit.",
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
                timezone.datetime.combine(
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

            if appointment_time.hour < 8 or appointment_time.hour >= 17:
                self.add_error(
                    "appointment_time",
                    "Appointments are only available from 8:00 AM to 5:00 PM.",
                )

        return cleaned_data
