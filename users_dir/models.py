from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(blank=False, max_length=255, verbose_name="email")
    whatsapp_id = models.CharField(blank=True, null=True, max_length=255, verbose_name="whatsapp")

    EMAIL_FIELD = "email"
