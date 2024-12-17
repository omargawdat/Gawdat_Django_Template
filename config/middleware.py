import os

from django.http import JsonResponse


class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.api_key = os.environ.get("API_KEY")

        # Get protected paths from env or use default
        self.default_protected_pattern = ["api"]
        self.excluded_paths = []
        self.excluded_patterns = ["docs", "callback", "schema"]

    def __call__(self, request):
        path_lower = request.path.lower()

        # Skip if path is excluded
        if any(request.path.startswith(path) for path in self.excluded_paths) or any(
            pattern in path_lower for pattern in self.excluded_patterns
        ):
            return self.get_response(request)

        # Validate API key for protected paths
        if any(path in path_lower for path in self.default_protected_pattern):
            api_key = request.headers.get("X-API-Key")
            if not api_key or api_key != self.api_key:
                return JsonResponse({"error": "Invalid API key"}, status=403)

        return self.get_response(request)
