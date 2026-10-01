from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Meta:
        verbose_name = "Customized user"
        verbose_name_plural = "Customized users"
