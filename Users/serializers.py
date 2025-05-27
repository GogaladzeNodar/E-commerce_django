from django.contrib.auth import get_user_model
from rest_framework import serializers
import re
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "phone_number",
        ]

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        # Password matching check
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        # Password strength check
        if not re.match(
            r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password
        ):
            raise serializers.ValidationError(
                "Password must be at least 8 characters long and include at least one uppercase letter, one number, and one special character."
            )

        return data

    def validate_email(self, value):
        # Check if email already exists
        if self.Meta.model.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already taken.")
        return value

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        # Using CustomUserManager's create_user method
        return self.Meta.model.objects.create_user(password=password, **validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # Authenticate user
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                {"non_field_errors": ["Invalid email or password"]}
            )

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        return {
            "user": {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone_number": user.phone_number,
            },
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
        }


class UserLogoutSerializer(serializers.Serializer):

    refresh_token = serializers.CharField()

    def validate_refresh_token(self, value):
        try:
            # Check if the token is valid
            RefreshToken(value)
        except Exception as e:
            raise serializers.ValidationError("Invalid refresh token.")
        return value


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = get_user_model().objects.get(email=value)
            self.context["user"] = user

        except User.DoesNotExist:
            raise serializers.ValidationError("User with this Email Doesn't exists")
        return value

    def save(self):
        user = self.context["user"]
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = user.pk

        reset_link = (
            self.context["request"].build_absolute_uri(
                reverse("password_reset_confirm")
            )
            + f"?uid={uid}&token={token}"
        )

        send_mail(
            "Password Reset",
            f"Go to the link to reset your password : {reset_link}",
            "gogaladzenodar9@gmail.com",
            [user.email],
            fail_silently=False,
        )


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        uid = attrs.get("uid")
        token = attrs.get("token")
        new_password = attrs.get("new_password")

        try:
            user = get_user_model().objects.get(pk=uid)
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError("user not found.")

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The token is invalid or expired.")
        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        attrs["user"] = user
        return attrs

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save()
