from django.utils import timezone
from django.utils.timezone import timedelta
from django.db import models
from django.contrib.auth.models import User


class TikTokToken(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="tiktok_token")
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expires_in = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.created_at + timedelta(seconds=self.expires_in) < timezone.now()


class VideoObject(models.Model):
    id = models.CharField(max_length=255, primary_key=True, verbose_name="Unique Identifier")
    create_time = models.BigIntegerField(verbose_name="Creation Time (UTC Unix Epoch in seconds)")
    cover_image_url = models.URLField(max_length=2048, verbose_name="Cover Image URL")
    share_url = models.URLField(max_length=2048, verbose_name="Shareable Link")
    video_description = models.CharField(max_length=150, verbose_name="Video Description")
    duration = models.IntegerField(verbose_name="Duration (in seconds)")
    height = models.IntegerField(verbose_name="Video Height")
    width = models.IntegerField(verbose_name="Video Width")
    title = models.CharField(max_length=150, verbose_name="Video Title")
    embed_html = models.TextField(verbose_name="Embed HTML Code")
    embed_link = models.URLField(max_length=2048, verbose_name="Embed Link")
    like_count = models.IntegerField(null=True, blank=True, verbose_name="Like Count")
    comment_count = models.IntegerField(null=True, blank=True, verbose_name="Comment Count")
    share_count = models.IntegerField(null=True, blank=True, verbose_name="Share Count")
    view_count = models.BigIntegerField(null=True, blank=True, verbose_name="View Count")

    class Meta:
        verbose_name = "Video Object"
        verbose_name_plural = "Video Objects"

    def __str__(self):
        return f"Video ID: {self.id} | Title: {self.title}"


class UserObject(models.Model):
    open_id = models.CharField(max_length=255, primary_key=True, verbose_name="Open ID")
    union_id = models.CharField(max_length=255, unique=True, verbose_name="Union ID")
    avatar_url = models.URLField(max_length=2048, verbose_name="Avatar URL")
    avatar_url_100 = models.URLField(max_length=2048, verbose_name="Avatar URL (100x100)")
    avatar_large_url = models.URLField(max_length=2048, verbose_name="Large Avatar URL")
    display_name = models.CharField(max_length=255, verbose_name="Display Name")
    bio_description = models.TextField(null=True, blank=True, verbose_name="Bio Description")
    profile_deep_link = models.URLField(max_length=2048, verbose_name="Profile Deep Link")
    is_verified = models.BooleanField(default=False, verbose_name="Verified User")
    username = models.CharField(max_length=255, verbose_name="Username")
    follower_count = models.BigIntegerField(null=True, blank=True, verbose_name="Follower Count")
    following_count = models.BigIntegerField(null=True, blank=True, verbose_name="Following Count")
    likes_count = models.BigIntegerField(null=True, blank=True, verbose_name="Likes Count")
    video_count = models.BigIntegerField(null=True, blank=True, verbose_name="Video Count")

    class Meta:
        verbose_name = "User Object"
        verbose_name_plural = "User Objects"

    def __str__(self):
        return f"User: {self.display_name} | Username: {self.username}"