from django.utils import timezone
from django.utils.timezone import timedelta
from django.db import models
from django.contrib.auth.models import User


class TikTokToken(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="tiktok_token")
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expires_in = models.IntegerField()  # Token expiry time in seconds
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        
        return self.created_at + timedelta(seconds=self.expires_in) < timezone.now()
