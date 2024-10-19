# middleware.py
from django.shortcuts import HttpResponse
from leaderboard_app import settings


class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Token or cookie value to check
        allowed_token = settings.AUTH_TOKEN_SECRET

        # Check if the token cookie is set and correct
        token = request.COOKIES.get('auth_token')
        if token != allowed_token:
            return HttpResponse("Unauthorized", status=401)

        response = self.get_response(request)
        return response
