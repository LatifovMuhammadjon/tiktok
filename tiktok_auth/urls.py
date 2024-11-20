from django.urls import path
from . import views

urlpatterns = [
    path('authorize/', views.tiktok_authorize, name='tiktok_authorize'),
    path('callback/', views.tiktok_callback, name='tiktok_callback'),
]
