from collections import defaultdict

from drf_standardized_errors.handler import exception_handler as drf_exception_handler
from rest_framework.views import exception_handler as drf_default_handler


def custom_exception_handler(exc, context):
    # First, get the response from drf_standardized_errors
    response = drf_exception_handler(exc, context)

    # If no response, fall back to DRF's default exception handler
    if response is None:
        response = drf_default_handler(exc, context)

    if response is not None and "errors" in response.data:
        # Group errors by code
        error_groups = defaultdict(list)
        for error in response.data["errors"]:
            error_groups[error["code"]].append(error)

        # Process each group of errors
        unique_errors = []
        for errors in error_groups.values():
            if len(errors) > 1:
                # If there are multiple errors with the same code, keep the most informative one
                most_informative = max(errors, key=lambda x: len(x.get("detail", "")))
                unique_errors.append(most_informative)
            else:
                # If there's only one error with this code, keep it
                unique_errors.append(errors[0])

        # Update the response with the processed errors
        response.data["errors"] = unique_errors

    return response
