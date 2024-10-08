# middleware.py
from django.shortcuts import HttpResponse

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Token or cookie value to check
        allowed_token = "!dTtjQpGDnWG3P9D4oLH8NAF#WM4fyunG%*Z7^kqc&7bpJwPx&6BuHm#pw!5rAjh8UgAYKzR4zXu%a$$t4$hvd9ZW"  # Replace with your secure token

        # Check if the token cookie is set and correct
        token = request.COOKIES.get('auth_token')
        if token != allowed_token:
            return HttpResponse("Unauthorized", status=401)

        response = self.get_response(request)
        return response
