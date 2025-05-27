from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationTests(APITestCase):
    def setUp(self):
        self.url = reverse("register")

        self.valid_payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "StrongPass1@",
            "confirm_password": "StrongPass1@",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "555-1234",
        }

    def test_user_registration_success(self):
        response = self.client.post(self.url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("tokens", response.data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, self.valid_payload["email"])

    def test_password_mismatch(self):
        payload = self.valid_payload.copy()
        payload["confirm_password"] = "WrongPass1@"
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(User.objects.count(), 0)

    def test_weak_password(self):
        payload = self.valid_payload.copy()
        payload["password"] = "weakpass"
        payload["confirm_password"] = "weakpass"
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(User.objects.count(), 0)

    def test_existing_email(self):
        User.objects.create_user(
            email="newuser@example.com",
            username="existinguser",
            password="StrongPass1@",
        )
        response = self.client.post(self.url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(User.objects.count(), 1)

    def test_missing_required_fields(self):
        response = self.client.post(self.url, data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("username", response.data)
        self.assertIn("password", response.data)
        self.assertIn("confirm_password", response.data)


class UserLoginTests(APITestCase):
    def setUp(self):
        self.url = reverse("login")
        self.user = User.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="StrongPass1@",
            first_name="Test",
            last_name="User",
            phone_number="123456789",
        )
        self.user.is_active = True
        self.user.save()

    def test_login_successful(self):
        response = self.client.post(
            self.url,
            data={"email": "testuser@example.com", "password": "StrongPass1@"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_wrong_password(self):
        response = self.client.post(
            self.url,
            data={"email": "testuser@example.com", "password": "WrongPassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(
            response.data["detail"],
            "No active account found with the given credentials",
        )

    def test_login_wrong_email(self):
        response = self.client.post(
            self.url,
            data={"email": "wrong@example.com", "password": "StrongPass1@"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(
            response.data["detail"],
            "No active account found with the given credentials",
        )

    def test_login_missing_fields(self):
        response = self.client.post(
            self.url,
            data={},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)


class UserLogoutTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="logoutuser@example.com",
            username="logoutuser",
            password="LogoutPass123@",
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}"
        )
        self.url = reverse("logout")

    def test_logout_success(self):
        response = self.client.post(
            self.url, data={"refresh_token": str(self.refresh)}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Successfully logged out.")

    def test_logout_invalid_token(self):
        response = self.client.post(
            self.url, data={"refresh_token": "invalidtoken"}, format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("refresh_token", response.data)


class PasswordResetTests(APITestCase):
    def setUp(self):
        self.url = reverse("password_reset")
        self.user = User.objects.create_user(
            email="resetuser@example.com", username="resetuser", password="TestPass123@"
        )

    def test_password_reset_success(self):
        response = self.client.post(
            self.url, data={"email": "resetuser@example.com"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

    def test_password_reset_nonexistent_email(self):
        response = self.client.post(
            self.url, data={"email": "notfound@example.com"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(
            response.data["email"][0], "User with this Email Doesn't exists"
        )

    def test_password_reset_missing_email_field(self):
        response = self.client.post(self.url, data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"][0], "This field is required.")


class PasswordResetConfirmTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="confirmuser@example.com",
            username="confirmuser",
            password="OldPassword123@",
        )
        self.token_generator = PasswordResetTokenGenerator()
        self.token = self.token_generator.make_token(self.user)
        self.uid = str(self.user.pk)
        self.url = reverse("password_reset_confirm")

    def test_password_reset_confirm_success(self):
        data = {
            "uid": self.uid,
            "token": self.token,
            "new_password": "NewStrongPass123@",
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

        login = self.client.post(
            reverse("login"),
            data={"email": self.user.email, "password": "NewStrongPass123@"},
            format="json",
        )
        self.assertEqual(login.status_code, status.HTTP_200_OK)

    def test_password_reset_confirm_invalid_token(self):
        data = {
            "uid": self.uid,
            "token": "invalidtoken",
            "new_password": "NewStrongPass123@",
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertIn(
            "The token is invalid or expired.", response.data["non_field_errors"]
        )

    def test_password_reset_confirm_invalid_uid(self):
        data = {"uid": "9999", "token": self.token, "new_password": "NewStrongPass123@"}
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertIn("user not found.", response.data["non_field_errors"])

    def test_password_reset_confirm_weak_password(self):
        data = {"uid": self.uid, "token": self.token, "new_password": "123"}
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("new_password", response.data)
