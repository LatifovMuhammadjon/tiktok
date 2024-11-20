from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings
import requests
from .models import TikTokToken
import random
import string

def generate_csrf_token():
    """Generate a random CSRF token"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=30))

def tiktok_authorize(request):
    csrf_token = generate_csrf_token()
    request.session['csrf_token'] = csrf_token

    auth_url = (
        "https://www.tiktok.com/v2/auth/authorize/"
        f"?client_key={settings.TIKTOK_CLIENT_KEY}"
        "&scope=user.info.basic"
        "&response_type=code"
        f"&redirect_uri={settings.TIKTOK_REDIRECT_URI}"
        f"&state={csrf_token}"
    )
    return redirect(auth_url)



def tiktok_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    stored_state = request.session.get('csrf_token')

    if not code or state != stored_state:
        return JsonResponse({"error": "Invalid state or missing code"}, status=400)

    token_url = "https://open.tiktokapis.com/v2/oauth/token/"
    payload = {
        "client_key": settings.TIKTOK_CLIENT_KEY,
        "client_secret": settings.TIKTOK_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.TIKTOK_REDIRECT_URI,
    }

    response = requests.post(token_url, json=payload)
    if response.status_code == 200:
        data = response.json().get("data")
        if data:
            TikTokToken.objects.update_or_create(
                user=request.user,  # Assuming the user is authenticated
                defaults={
                    "access_token": data["access_token"],
                    "refresh_token": data.get("refresh_token"),
                    "scopes": ','.join(data.get("scope", [])),
                    "expires_in": data["expires_in"],
                }
            )
            return JsonResponse({"message": "TikTok token saved successfully!"})
    return JsonResponse({"error": response.json()}, status=400)
