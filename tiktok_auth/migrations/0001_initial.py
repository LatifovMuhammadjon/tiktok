# Generated by Django 5.1.3 on 2024-11-14 11:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TikTokToken",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("access_token", models.CharField(max_length=255)),
                ("refresh_token", models.CharField(max_length=255)),
                ("expires_in", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tiktok_token",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]