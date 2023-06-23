from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, max_length=255, verbose_name="email")

    phoneNumber = models.CharField(unique=True, null=True, max_length=255, verbose_name="phone")

    avatar = models.CharField(null=True, max_length=255)
    country = models.CharField(null=True, max_length=255)
    city = models.CharField(null=True, max_length=255)

    username = models.CharField(null=True, unique=True, max_length=255, verbose_name="username")

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    REQUIRED_FIELDS = []
