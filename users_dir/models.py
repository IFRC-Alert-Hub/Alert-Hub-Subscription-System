from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, max_length=254, verbose_name="email")
    whatsAppId = models.CharField(null=True, max_length=254, verbose_name="whatsAppId")

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    REQUIRED_FIELDS = []
