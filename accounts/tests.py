from django.test import TestCase
from django.urls import reverse

from .models import User, ResidentProfile


class AccountTests(TestCase):

    def setUp(self):
        self.password = "SecureTestPass2026!"

        self.user = User.objects.create_user(
            username="testresident",
            email="resident@example.com",
            password=self.password,
            first_name="Test",
            last_name="Resident",
            phone="09123456789",
            role=User.Role.RESIDENT,
        )

        ResidentProfile.objects.create(
            user=self.user,
            phone="09123456789",
            address="Cebu City",
            birth_date="2000-01-01",
        )

        self.registration_data = {
            "username": "newresident",
            "first_name": "New",
            "last_name": "Resident",
            "email": "newresident@example.com",
            "phone": "09987654321",
            "address": "Cebu City",
            "birth_date": "2000-01-01",
            "password1": self.password,
            "password2": self.password,
        }

    def test_valid_resident_registration(self):
        response = self.client.post(
            reverse("register"),
            self.registration_data,
        )

        self.assertRedirects(response, reverse("login"))

        user = User.objects.get(username="newresident")

        self.assertEqual(user.role, User.Role.RESIDENT)

        self.assertTrue(
            ResidentProfile.objects.filter(user=user).exists()
        )

    def test_duplicate_email_registration(self):
        data = self.registration_data.copy()
        data["email"] = self.user.email

        response = self.client.post(
            reverse("register"),
            data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("email", response.context["form"].errors)

        self.assertFalse(
            User.objects.filter(username="newresident").exists()
        )

    def test_underage_registration(self):
        data = self.registration_data.copy()
        data["birth_date"] = "2020-01-01"

        response = self.client.post(
            reverse("register"),
            data,
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            "birth_date",
            response.context["form"].errors,
        )

        self.assertFalse(
            User.objects.filter(username="newresident").exists()
        )

    def test_invalid_phone_registration(self):
        data = self.registration_data.copy()
        data["phone"] = "abc123"

        response = self.client.post(
            reverse("register"),
            data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("phone", response.context["form"].errors)

        self.assertFalse(
            User.objects.filter(username="newresident").exists()
        )

    def test_valid_login(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": self.user.username,
                "password": self.password,
            },
        )

        self.assertRedirects(response, reverse("dashboard"))

        self.assertIn(
            "_auth_user_id",
            self.client.session,
        )

    def test_invalid_login(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": self.user.username,
                "password": "incorrect-password",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertNotIn(
            "_auth_user_id",
            self.client.session,
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('dashboard')}",
        )

    def test_valid_profile_update(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("profile"),
            {
                "first_name": "Updated",
                "last_name": "Resident",
                "email": self.user.email,
                "phone": "09999999999",
                "address": "Updated Cebu City Address",
                "birth_date": "2000-01-01",
            },
        )

        self.assertRedirects(response, reverse("profile"))

        self.user.refresh_from_db()

        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.phone, "09999999999")

        profile = ResidentProfile.objects.get(user=self.user)

        self.assertEqual(
            profile.address,
            "Updated Cebu City Address",
        )

        self.assertEqual(profile.phone, self.user.phone)

    def test_logout_requires_post(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("logout"))

        self.assertEqual(response.status_code, 405)

        self.assertIn(
            "_auth_user_id",
            self.client.session,
        )

    def test_valid_logout(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("login"))

        self.assertNotIn(
            "_auth_user_id",
            self.client.session,
        )