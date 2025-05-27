from django.test import TestCase
from Users.models import CustomUser
from datetime import date


class CustomUserModelTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            password="password123",
            phone_number="+995555123456",
            address="Tbilisi, Georgia",
            profile_picture=None,
            birthdate=date(2000, 1, 1),
            gender="Male",
            newsletter_subscription=True,
            loyalty_points=100,
            is_active=True,
            is_staff=False,
        )

    def test_user_created_successfully(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(self.user.phone_number, "+995555123456")
        self.assertEqual(self.user.address, "Tbilisi, Georgia")
        self.assertEqual(self.user.birthdate.isoformat(), "2000-01-01")
        self.assertEqual(self.user.gender, "Male")
        self.assertTrue(self.user.newsletter_subscription)
        self.assertEqual(self.user.loyalty_points, 100)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

    def test_user_check_password(self):
        self.assertTrue(self.user.check_password("password123"))

    def test_email_is_unique(self):
        with self.assertRaises(Exception):
            CustomUser.objects.create_user(
                username="anotheruser",
                email="testuser@example.com",
                first_name="Test",
                last_name="User",
                password="password123",
            )

    def test_username_is_unique(self):
        with self.assertRaises(Exception):
            CustomUser.objects.create_user(
                username="anotheruser",
                email="testuser@example.com",
                first_name="Test",
                last_name="User",
                password="password123",
            )

    def test_default_values(self):
        user = CustomUser.objects.create_user(
            username="defaultuser",
            email="defaultuser@example.com",
            first_name="Default",
            last_name="User",
            password="password123",
        )
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.newsletter_subscription)
        self.assertEqual(user.loyalty_points, 0)

    def test_user_profile_picture_upload_path(self):
        self.assertEqual(self.user.profile_picture, None)
