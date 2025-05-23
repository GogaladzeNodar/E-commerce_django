from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["email", "username", "is_active", "is_staff", "date_joined"]
    search_fields = ["email", "username"]
    ordering = ["date_joined"]
