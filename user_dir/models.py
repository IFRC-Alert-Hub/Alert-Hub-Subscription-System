from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, max_length=255, verbose_name="email")
    phoneNumber = models.CharField(unique=True, null=True, max_length=255, verbose_name="phone")
    avatar = models.CharField(null=True, blank=True, max_length=255)
    country = models.CharField(null=True, blank=True, max_length=255)
    city = models.CharField(null=True, blank=True, max_length=255)
    verified = models.BooleanField(default=False)
    username = models.CharField(null=True, unique=True, max_length=255, verbose_name="username")

    email_verification_token = models.UUIDField(null=True, blank=True)
    email_verification_token_expires_at = models.DateTimeField(null=True, blank=True)
    password_reset_token = models.UUIDField(null=True, blank=True)
    password_reset_token_expires_at = models.DateTimeField(null=True, blank=True)
    email_reset_token = models.UUIDField(null=True, blank=True)
    email_reset_token_expires_at = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []