from django.test import TestCase, RequestFactory
from rest_framework.test import APITestCase, APIRequestFactory
from Users.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserLogoutSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch
from django.contrib.auth.tokens import PasswordResetTokenGenerator

User = get_user_model()


class UserRegistrationSerializerTest(TestCase):
    def setUp(self):
        self.validate_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Strong@123",
            "confirm_password": "Strong@123",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+995555123456",
        }

    def test_validate_data_create_user(self):
        serializer = UserRegistrationSerializer(data=self.validate_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.email, self.validate_data["email"])
        self.assertTrue(user.check_password(self.validate_data["password"]))

    def test_passwords_do_not_match(self):
        invalid_data = self.validate_data.copy()
        invalid_data["confirm_password"] = "Wrong@123"
        serializer = UserRegistrationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertIn("Passwords do not match.", serializer.errors["non_field_errors"])

    def test_weak_password_fails(self):
        weak_data = self.validate_data.copy()
        weak_data["password"] = "weakpass"
        weak_data["confirm_password"] = "weakpass"
        serializer = UserRegistrationSerializer(data=weak_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertIn(
            "Password must be at least 8 characters long",
            serializer.errors["non_field_errors"][0],
        )

    def test_email_already_exists(self):
        User.objects.create_user(
            username="another", email="test@example.com", password="Another@123"
        )
        serializer = UserRegistrationSerializer(data=self.validate_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.assertIn("This email is already taken.", serializer.errors["email"])


#     რა უნდა დავტესტოთ ამ UserLoginSerializer-ისთვის:


# სწორი მონაცემები → დააბრუნოს user info + access/refresh ტოკენები.
# არასწორი პაროლი → დაბრუნდეს ValidationError.
# არარსებული იმეილი → დაბრუნდეს ValidationError.
class UserLoginSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="Strong@123",
            first_name="Test",
            last_name="User",
            phone_number="+995555123456",
        )
        self.valid_data = {"email": "testuser@example.com", "password": "Strong@123"}

    def test_login_with_valid_credentials(self):
        serializer = UserLoginSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        data = serializer.validated_data

        self.assertIn("user", data)
        self.assertEqual(data["user"]["email"], self.user.email)
        self.assertIn("tokens", data)
        self.assertIn("access", data["tokens"])
        self.assertIn("refresh", data["tokens"])

    def test_login_with_invalid_password(self):
        invalid_data = {"email": "testuser@example.com", "password": "WrongPassword123"}
        serializer = UserLoginSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual
        (serializer.errors["non_field_errors"][0], "invalid email or password")

    def test_login_with_nonexistent_email(self):
        invalid_data = {"email": "notfound@example.com", "password": "Whatever@123"}
        serializer = UserLoginSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(
            serializer.errors["non_field_errors"][0], "Invalid email or password"
        )


# ვალიდური refresh_token → უნდა გაიაროს ვალიდაცია.
# არასწორი (invalid / random string) token → უნდა დააბრუნოს ValidationError.
class UserLogoutSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="logoutuser", email="logout@example.com", password="Strong@123"
        )
        self.refresh = str(RefreshToken.for_user(self.user))

    def test_valid_refresh_token(self):
        serializer = UserLogoutSerializer(data={"refresh_token": self.refresh})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["refresh_token"], self.refresh)

    def test_invalid_refresh_token(self):
        invalid_token = "notarealtoken123"
        serializer = UserLogoutSerializer(data={"refresh_token": invalid_token})
        self.assertFalse(serializer.is_valid())
        self.assertIn("refresh_token", serializer.errors)
        self.assertEqual(
            str(serializer.errors["refresh_token"][0]), "Invalid refresh token."
        )


# ვალიდური ემეილი — თუ ბაზაში არსებობს, უნდა გაიაროს ვალიდაცია და შეინახოს context-ში user.
# არარსებული ემეილი — უნდა დაბრუნდეს ValidationError.
# save() მეთოდი — ანუ იმიტაცია იმისა, რომ ეგ იმეილი გაიგზავნა სწორად და reset_link სწორად აგენერირდა.


class PasswordResetSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="resetuser", email="reset@example.com", password="Strong@123"
        )
        self.factory = RequestFactory()
        self.request = self.factory.post("/fake_url/")

    def test_valid_email(self):
        serializer = PasswordResetSerializer(
            data={"email": self.user.email}, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["email"], self.user.email)
        self.assertEqual(serializer.context["user"], self.user)

    def test_invalid_email(self):
        serializer = PasswordResetSerializer(
            data={"email": "notfound@example.com"}, context={"request": self.request}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    @patch("Users.serializers.send_mail")
    def test_save_sends_email(self, mock_send_mail):
        serializer = PasswordResetSerializer(
            data={"email": "reset@example.com"}, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertTrue(mock_send_mail.called)


class PasswordResetConfirmSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="OldPassword123!"
        )
        self.token_generator = PasswordResetTokenGenerator()
        self.token = self.token_generator.make_token(self.user)
        self.uid = str(self.user.pk)

    def test_valid_data_resets_password(self):
        data = {
            "uid": self.uid,
            "token": self.token,
            "new_password": "NewStrong@123",
        }
        serializer = PasswordResetConfirmSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        serializer.save()
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewStrong@123"))

    def test_invalid_uid_raises_error(self):
        data = {
            "uid": "999999",  # არასწორი იუზერის ID
            "token": self.token,
            "new_password": "AnotherStrong123!",
        }
        serializer = PasswordResetConfirmSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("user not found.", str(serializer.errors))

    def test_invalid_token_raises_error(self):
        data = {
            "uid": self.uid,
            "token": "invalid-token",
            "new_password": "AnotherStrong123!",
        }
        serializer = PasswordResetConfirmSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("The token is invalid or expired.", str(serializer.errors))

    def test_weak_password_fails_validation(self):
        data = {"uid": self.uid, "token": self.token, "new_password": "12345678"}
        serializer = PasswordResetConfirmSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("new_password", serializer.errors)
