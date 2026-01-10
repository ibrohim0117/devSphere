import uuid
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    about = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    leetcode = models.URLField(blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)

    is_verified = models.BooleanField(default=False)

    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = None

    def __str__(self):
        return self.email



class EmailConfirmation(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Token 24 soat davomida amal qiladi
        if not self.expires_at or not self.pk:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def is_expired(self):
        """Token muddati o'tganligini tekshirish"""
        if not self.expires_at:
            return True
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.user.email} - {self.token}"

    @classmethod
    def cleanup_expired_tokens(cls):
        """Eski tokenlarni tozalash"""
        expired_tokens = cls.objects.filter(expires_at__lt=timezone.now())
        count = expired_tokens.count()
        expired_tokens.delete()
        return count
