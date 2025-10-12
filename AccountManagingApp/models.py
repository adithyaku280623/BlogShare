from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    contact_number = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.username


