from django.contrib import admin
from django.urls import path, include
from tiktok_auth.views import file_download_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('tiktok/', include('tiktok_auth.urls')),
    path('tiktok2sUpCBBU3l1n44Sg9gHI1XRuZxjG67Wt.txt', file_download_view)
]
