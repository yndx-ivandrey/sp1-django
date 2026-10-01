from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):  # type: ignore[type-arg]
    list_display = ("username", "email", "is_superuser")
