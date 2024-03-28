from django.contrib.auth.models import AbstractUser, AbstractBaseUser


class CustomUser(AbstractUser):
    pass

    class Meta:
        verbose_name = "Customized user"
        verbose_name_plural = "Customized users"
