import os

from django.http import JsonResponse


class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.admin_url = os.environ.get("DJANGO_ADMIN_URL", "admin")
        self.api_key = os.environ.get("API_KEY")

    def __call__(self, request):
        api_key = request.headers.get("X-API-Key")

        if request.path.startswith(f"/{self.admin_url}/"):
            return self.get_response(request)

        if not api_key or api_key != self.api_key:
            return JsonResponse({"error": "Invalid API key"}, status=403)

        return self.get_response(request)
