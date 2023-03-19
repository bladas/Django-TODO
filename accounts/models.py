from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField("email address", unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email
