from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):  # type: ignore[type-arg]
    class Meta:
        model = CustomUser
        fields = ("username", "email")
