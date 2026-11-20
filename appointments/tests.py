
from datetime import timedelta, time

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Appointment


User = get_user_model()


class AppointmentTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.resident = User.objects.create_user(
            username="resident_test",
            email="resident_test@example.com",
            password="TestPassword123!",
            role=User.Role.RESIDENT,
        )

        cls.other_resident = User.objects.create_user(
            username="other_resident",
            email="other_resident@example.com",
            password="TestPassword123!",
            role=User.Role.RESIDENT,
        )

        cls.staff = User.objects.create_user(
            username="staff_test",
            email="staff_test@example.com",
            password="TestPassword123!",
            role=User.Role.STAFF,
        )

        cls.admin = User.objects.create_user(
            username="admin_test",
            email="admin_test@example.com",
            password="TestPassword123!",
            role=User.Role.ADMIN,
        )

    def setUp(self):
        self.future_date = timezone.localdate() + timedelta(days=7)

        self.appointment = Appointment.objects.create(
            resident=self.resident,
            service_type=Appointment.ServiceType.GENERAL_CHECKUP,
            appointment_date=self.future_date,
            appointment_time=time(9, 0),
            reason="Routine health checkup.",
            status=Appointment.Status.PENDING,
        )

    # RESIDENT APPOINTMENT TESTS

    def test_resident_can_view_own_appointments(self):
        self.client.force_login(self.resident)

        response = self.client.get(
            reverse("appointments:list")
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "General Checkup",
        )

        self.assertContains(
            response,
            "Pending",
        )

        self.assertContains(
            response,
            reverse(
                "appointments:detail",
                args=[self.appointment.pk],
            ),
        )

    def test_resident_cannot_view_other_resident_appointment(self):
        self.client.force_login(self.other_resident)

        response = self.client.get(
            reverse(
                "appointments:detail",
                args=[self.appointment.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_resident_can_book_appointment(self):
        self.client.force_login(self.resident)

        response = self.client.post(
            reverse("appointments:create"),
            {
                "service_type": Appointment.ServiceType.CONSULTATION,
                "appointment_date": self.future_date.isoformat(),
                "appointment_time": "10:00",
                "reason": "Medical consultation.",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertTrue(
            Appointment.objects.filter(
                resident=self.resident,
                appointment_time=time(10, 0),
            ).exists()
        )

    def test_duplicate_appointment_slot_is_rejected(self):
        self.client.force_login(self.other_resident)

        response = self.client.post(
            reverse("appointments:create"),
            {
                "service_type": Appointment.ServiceType.CONSULTATION,
                "appointment_date": self.future_date.isoformat(),
                "appointment_time": "09:00",
                "reason": "Another checkup.",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            Appointment.objects.filter(
                appointment_date=self.future_date,
                appointment_time=time(9, 0),
            ).count(),
            1,
        )

    def test_resident_can_cancel_pending_appointment(self):
        self.client.force_login(self.resident)

        response = self.client.post(
            reverse(
                "appointments:cancel",
                args=[self.appointment.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.Status.CANCELLED,
        )

    # STAFF APPOINTMENT TESTS

    def test_staff_can_confirm_pending_appointment(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse(
                "appointments:staff_update_status",
                args=[self.appointment.pk],
            ),
            {
                "status": Appointment.Status.CONFIRMED,
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.Status.CONFIRMED,
        )

    def test_staff_can_complete_confirmed_appointment(self):
        self.appointment.status = Appointment.Status.CONFIRMED
        self.appointment.save()

        self.client.force_login(self.staff)

        response = self.client.post(
            reverse(
                "appointments:staff_update_status",
                args=[self.appointment.pk],
            ),
            {
                "status": Appointment.Status.COMPLETED,
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.Status.COMPLETED,
        )

    def test_staff_cannot_complete_pending_appointment(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse(
                "appointments:staff_update_status",
                args=[self.appointment.pk],
            ),
            {
                "status": Appointment.Status.COMPLETED,
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.Status.PENDING,
        )

    # ADMIN APPOINTMENT TESTS

    def test_admin_can_view_appointment_oversight(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("appointments:admin_list")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Healthcare Appointment Oversight",
        )

    def test_resident_cannot_access_admin_oversight(self):
        self.client.force_login(self.resident)

        response = self.client.get(
            reverse("appointments:admin_list")
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_staff_cannot_access_admin_oversight(self):
        self.client.force_login(self.staff)

        response = self.client.get(
            reverse("appointments:admin_list")
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_admin_cannot_access_staff_management(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("appointments:staff_list")
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    # HTTP METHOD VALIDATION TEST

    def test_cancel_requires_post_request(self):
        self.client.force_login(self.resident)

        response = self.client.get(
            reverse(
                "appointments:cancel",
                args=[self.appointment.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            405,
        )

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.Status.PENDING,
        )
