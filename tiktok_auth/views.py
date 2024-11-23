from django.shortcuts import redirect
from django.http import JsonResponse, FileResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import TikTokToken  # Update to your actual model import
import os
import requests
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


@csrf_exempt
def tiktok_callback(request):
    # Retrieve code and state from the query parameters
    code = request.GET.get('code')
    state = request.GET.get('state')
    stored_state = request.session.get('csrf_token')

    # Validate state and code
    if not code or not state or state != stored_state:
        return JsonResponse({"error": "Invalid state or missing code"}, status=400)

    # Prepare the payload for the token exchange
    token_url = "https://open.tiktokapis.com/v2/oauth/token/"
    payload = {
        "client_key": settings.TIKTOK_CLIENT_KEY,
        "client_secret": settings.TIKTOK_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.TIKTOK_REDIRECT_URI,
    }

    try:
        # Make a POST request with the correct headers
        headers = {"Content-Type": "application/json"}
        response = requests.post(token_url, json=payload, headers=headers)

        # Ensure the response is successful
        if response.status_code == 200:
            response_data = response.json()
            return JsonResponse(response.json())
        else:
            # Handle non-200 responses
            error_response = response.json()
            return JsonResponse({"error": "Failed to retrieve token", "details": error_response}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        # Handle network-related exceptions
        return JsonResponse({"error": "Request failed", "details": str(e)}, status=500)


def file_download_view(request):
    filename = "tiktokwky1RKcvmi5COrMgUDl7AzhZ4MiVjfva.txt"
    file_path = os.path.join(settings.BASE_DIR, filename)
    
    # Return a FileResponse for file download
    response = FileResponse(open(file_path, 'rb'), as_attachment=True)
    return response
