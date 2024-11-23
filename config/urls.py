from django.contrib import admin
from django.urls import path, include
from tiktok_auth.views import file_download_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('tiktok/', include('tiktok_auth.urls')),
    path('tiktokwky1RKcvmi5COrMgUDl7AzhZ4MiVjfva.txt', file_download_view)
]
