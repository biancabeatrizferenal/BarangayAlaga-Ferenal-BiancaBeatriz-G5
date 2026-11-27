from django.test import TestCase

# Create your tests here.
from datetime import time, timedelta

from django.db import IntegrityError, transaction
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from .models import Appointment


class AppointmentTests(TestCase):

    def setUp(self):
        self.resident = User.objects.create_user(
            username="resident1",
            email="resident1@example.com",
            password="SecureTestPass2026!",
            role=User.Role.RESIDENT,
        )

        self.other_resident = User.objects.create_user(
            username="resident2",
            email="resident2@example.com",
            password="SecureTestPass2026!",
            role=User.Role.RESIDENT,
        )

        self.staff = User.objects.create_user(
            username="staff1",
            email="staff1@example.com",
            password="SecureTestPass2026!",
            role=User.Role.STAFF,
        )

        self.admin = User.objects.create_user(
            username="admin1",
            email="admin1@example.com",
            password="SecureTestPass2026!",
            role=User.Role.ADMIN,
        )

        self.future_date = (
            timezone.localdate() + timedelta(days=7)
        )

        self.appointment = Appointment.objects.create(
            resident=self.resident,
            service_type=Appointment.ServiceType.GENERAL_CHECKUP,
            appointment_date=self.future_date,
            appointment_time=time(9, 0),
            reason="Routine health checkup",
            status=Appointment.Status.PENDING,
        )

        self.booking_data = {
            "service_type": Appointment.ServiceType.GENERAL_CHECKUP,
            "appointment_date": self.future_date.isoformat(),
            "appointment_time": "10:00",
            "reason": "Follow-up health consultation",
        }

    def test_valid_appointment_booking(self):
        self.client.force_login(self.resident)

        response = self.client.post(
            reverse("appointments:create"),
            self.booking_data,
        )

        appointment = Appointment.objects.get(
            resident=self.resident,
            appointment_time=time(10, 0),
        )

        self.assertRedirects(
            response,
            reverse(
                "appointments:detail",
                args=[appointment.pk],
            ),
        )

        self.assertEqual(
            appointment.status,
            Appointment.Status.PENDING,
        )

    def test_past_appointment_date_rejected(self):
        self.client.force_login(self.resident)

        data = self.booking_data.copy()

        data["appointment_date"] = (
            timezone.localdate() - timedelta(days=1)
        ).isoformat()

        response = self.client.post(
            reverse("appointments:create"),
            data,
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            "appointment_date",
            response.context["form"].errors,
        )

        self.assertEqual(Appointment.objects.count(), 1)

    def test_duplicate_appointment_slot_rejected(self):
        self.client.force_login(self.other_resident)

        data = self.booking_data.copy()
        data["appointment_time"] = "09:00"

        response = self.client.post(
            reverse("appointments:create"),
            data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(Appointment.objects.count(), 1)

    def test_valid_appointment_update(self):
        self.client.force_login(self.resident)

        response = self.client.post(
            reverse(
                "appointments:update",
                args=[self.appointment.pk],
            ),
            self.booking_data,
        )

        self.assertRedirects(
            response,
            reverse(
                "appointments:detail",
                args=[self.appointment.pk],
            ),
        )

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.appointment_time,
            time(10, 0),
        )

        self.assertEqual(
            self.appointment.reason,
            self.booking_data["reason"],
        )

    def test_valid_appointment_cancellation(self):
        self.client.force_login(self.resident)

        response = self.client.post(
            reverse(
                "appointments:cancel",
                args=[self.appointment.pk],
            ),
        )

        self.assertRedirects(
            response,
            reverse(
                "appointments:detail",
                args=[self.appointment.pk],
            ),
        )

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.Status.CANCELLED,
        )

    def test_other_resident_cannot_view_appointment(self):
        self.client.force_login(self.other_resident)

        response = self.client.get(
            reverse(
                "appointments:detail",
                args=[self.appointment.pk],
            ),
        )

        self.assertEqual(response.status_code, 404)

    def test_other_resident_cannot_update_appointment(self):
        self.client.force_login(self.other_resident)

        response = self.client.post(
            reverse(
                "appointments:update",
                args=[self.appointment.pk],
            ),
            self.booking_data,
        )

        self.assertEqual(response.status_code, 404)

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.reason,
            "Routine health checkup",
        )

    def test_other_resident_cannot_cancel_appointment(self):
        self.client.force_login(self.other_resident)

        response = self.client.post(
            reverse(
                "appointments:cancel",
                args=[self.appointment.pk],
            ),
        )

        self.assertEqual(response.status_code, 404)

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.Status.PENDING,
        )

    def test_resident_cannot_access_staff_pages(self):
        self.client.force_login(self.resident)

        response = self.client.get(
            reverse("appointments:staff_list")
        )

        self.assertEqual(response.status_code, 403)

    def test_resident_cannot_access_admin_pages(self):
        self.client.force_login(self.resident)

        response = self.client.get(
            reverse("appointments:admin_list")
        )

        self.assertEqual(response.status_code, 403)

    def test_cancellation_requires_post(self):
        self.client.force_login(self.resident)

        response = self.client.get(
            reverse(
                "appointments:cancel",
                args=[self.appointment.pk],
            ),
        )

        self.assertEqual(response.status_code, 405)

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.Status.PENDING,
        )

    def test_status_update_requires_post(self):
        self.client.force_login(self.staff)

        response = self.client.get(
            reverse(
                "appointments:staff_update_status",
                args=[self.appointment.pk],
            ),
        )

        self.assertEqual(response.status_code, 405)

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.Status.PENDING,
        )

    def test_valid_staff_status_update(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse(
                "appointments:staff_update_status",
                args=[self.appointment.pk],
            ),
            {"status": Appointment.Status.CONFIRMED},
        )

        self.assertRedirects(
            response,
            reverse(
                "appointments:staff_detail",
                args=[self.appointment.pk],
            ),
        )

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.Status.CONFIRMED,
        )

    def test_invalid_status_transition_rejected(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse(
                "appointments:staff_update_status",
                args=[self.appointment.pk],
            ),
            {"status": Appointment.Status.COMPLETED},
        )

        self.assertEqual(response.status_code, 302)

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.Status.PENDING,
        )

    def test_appointment_list_requires_login(self):
        response = self.client.get(
            reverse("appointments:list")
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('appointments:list')}",
        )

    def test_invalid_appointment_id_returns_404(self):
        self.client.force_login(self.resident)

        response = self.client.get(
            reverse(
                "appointments:detail",
                args=[999999999],
            ),
        )

        self.assertEqual(response.status_code, 404)

    def test_appointment_details_displayed(self):
        self.client.force_login(self.resident)

        response = self.client.get(
            reverse(
                "appointments:detail",
                args=[self.appointment.pk],
            ),
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            self.appointment.reason,
        )

    def test_admin_appointment_counts(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("appointments:admin_list")
        )

        self.assertEqual(response.status_code, 200)

        counts = response.context["appointment_counts"]

        self.assertEqual(counts["total"], 1)
        self.assertEqual(counts["pending"], 1)
        self.assertEqual(counts["confirmed"], 0)
        self.assertEqual(counts["completed"], 0)
        self.assertEqual(counts["rejected"], 0)
        self.assertEqual(counts["cancelled"], 0)

    def test_database_prevents_duplicate_active_slot(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Appointment.objects.create(
                    resident=self.other_resident,
                    service_type=(
                        Appointment.ServiceType.GENERAL_CHECKUP
                    ),
                    appointment_date=self.future_date,
                    appointment_time=time(9, 0),
                    reason="Duplicate appointment",
                    status=Appointment.Status.PENDING,
                )

        self.assertEqual(Appointment.objects.count(), 1)

    def test_cancellation_requires_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)

        csrf_client.force_login(self.resident)

        response = csrf_client.post(
            reverse(
                "appointments:cancel",
                args=[self.appointment.pk],
            ),
        )

        self.assertEqual(response.status_code, 403)

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.Status.PENDING,
        )