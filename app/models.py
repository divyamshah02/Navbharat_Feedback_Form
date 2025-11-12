# app/models.py
from django.db import models
from django.utils import timezone
import os

def qr_upload_path(instance, filename):
    return os.path.join("qrs", filename)

class OTPVerification(models.Model):
    mobile = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    attempt_count = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.mobile} - {self.otp}"

class UserInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=15, unique=True)
    qr_image = models.ImageField(upload_to=qr_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
