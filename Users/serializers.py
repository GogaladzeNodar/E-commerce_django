from django.contrib.auth import get_user_model
from rest_framework import serializers
import re
from .models import CustomUser


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
        if not re.match(
            r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password
        ):
            raise serializers.ValidationError(
                {
                    "password": "Password must be at least 8 characters long and include at least one uppercase letter, one number, and one special character."
                }
            )

        if password != data.get("confirm_password"):
            raise serializers.ValidationError({"password": "Passwords do not match."})

        return data

    def validate_email(self, value):

        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Invalid email format.")

        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already taken.")

        return value

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        return self.Meta.model.objects.create_user(password=password, **validated_data)
