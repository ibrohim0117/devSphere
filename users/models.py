from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    about = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
