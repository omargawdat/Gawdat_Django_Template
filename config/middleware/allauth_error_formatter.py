import json

from django.http import JsonResponse

# HTTP status code constants
HTTP_BAD_REQUEST = 400
HTTP_INTERNAL_SERVER_ERROR = 500


class AllauthErrorFormatterMiddleware:
    """Transform django-allauth headless error responses to drf-standardized-errors format."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only process allauth endpoints
        if not request.path.startswith("/api/_allauth/"):
            return response

        # Only process error responses (4xx, 5xx)
        if response.status_code < HTTP_BAD_REQUEST:
            return response

        # Only process JSON responses
        if not response.get("Content-Type", "").startswith("application/json"):
            return response

        try:
            data = json.loads(response.content)
        except (json.JSONDecodeError, AttributeError):
            return response

        # Check if response has allauth error format
        if not isinstance(data, dict) or "errors" not in data:
            return response

        # Transform to drf-standardized-errors format
        transformed_data = self._transform_errors(data, response.status_code)

        return JsonResponse(transformed_data, status=response.status_code)

    def _transform_errors(self, data: dict, status_code: int) -> dict:
        """Transform allauth error format to drf-standardized-errors format."""
        errors = data.get("errors", [])

        # Map status code to error type
        error_type = self._get_error_type(status_code)

        # Transform each error using list comprehension
        transformed_errors = [
            {
                "code": error.get("code", "error"),
                "detail": error.get("message", "An error occurred"),
                "attr": error.get("param"),
            }
            for error in errors
            if isinstance(error, dict)
        ]

        return {"type": error_type, "errors": transformed_errors}

    def _get_error_type(self, status_code: int) -> str:
        """Determine error type based on HTTP status code."""
        if status_code in (HTTP_BAD_REQUEST, 422):
            return "validation_error"
        elif status_code >= HTTP_INTERNAL_SERVER_ERROR:
            return "server_error"
        else:
            # 401, 403, 404, 405, 406, 415, 429, etc.
            return "client_error"
