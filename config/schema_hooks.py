"""
Schema postprocessing hooks for merging Django-Allauth Headless OpenAPI spec.

This module merges allauth endpoints into the main API schema and transforms
error response schemas to match drf-standardized-errors format.
"""

import hashlib

from django.test import Client

HTTP_METHODS = {"get", "post", "put", "patch", "delete", "options", "head", "trace"}
HTTP_OK = 200  # HTTP 200 OK status code


def _transform_error_item_properties(item_props: dict) -> dict:
    """Transform error item properties from allauth to drf-standardized-errors format."""
    field_mapping = {"message": "detail", "param": "attr", "code": "code"}
    return {field_mapping.get(key, key): value for key, value in item_props.items()}


def _update_required_fields(required: list) -> None:
    """Update required fields list with new field names."""
    if "message" in required:
        required.remove("message")
        required.append("detail")
    if "param" in required:
        required.remove("param")
        required.append("attr")


def _transform_error_items(errors_prop: dict) -> None:
    """Transform error items in the errors array."""
    if "items" not in errors_prop:
        return

    items = errors_prop["items"]
    item_props = items.get("properties", {})

    # Check if it's allauth format
    if "message" not in item_props and "param" not in item_props:
        return

    # Transform properties
    items["properties"] = _transform_error_item_properties(item_props)

    # Update required fields
    if "required" in items:
        _update_required_fields(items["required"])


def _add_type_field(schema: dict, properties: dict) -> None:
    """Add 'type' field and remove 'status' field from schema."""
    properties.pop("status", None)

    if "type" not in properties:
        properties["type"] = {
            "type": "string",
            "enum": ["validation_error", "client_error", "server_error"],
            "description": "Error type based on status code",
        }

        # Update schema required fields
        if "required" in schema:
            if "status" in schema["required"]:
                schema["required"].remove("status")
            if "type" not in schema["required"]:
                schema["required"].append("type")


def _transform_error_schemas(schemas: dict) -> None:
    """Transform allauth error schemas to drf-standardized-errors format."""
    for schema in schemas.values():
        if not isinstance(schema, dict):
            continue

        properties = schema.get("properties", {})

        # Only transform schemas with errors and status fields (allauth format)
        if "errors" not in properties or "status" not in properties:
            continue

        # Transform error items
        _transform_error_items(properties.get("errors", {}))

        # Add type field and remove status
        _add_type_field(schema, properties)


def merge_allauth_spec(result, generator=None, request=None, public=False, **kwargs):
    """
    Merge Django-Allauth Headless OpenAPI specification into main schema.

    This hook:
    1. Fetches allauth's OpenAPI spec
    2. Adds operation IDs to allauth endpoints
    3. Prefixes allauth tags with "Authentication /"
    4. Transforms error response schemas to drf-standardized-errors format
    5. Merges paths and components into main schema
    6. Adds top-level "Authentication" tag
    """
    # Step 1: Fetch allauth's OpenAPI schema
    c = Client()
    resp = c.get("/api/_allauth/openapi.json")

    # If allauth schema is not available, return original schema
    if resp.status_code != HTTP_OK:
        return result

    ext = resp.json()

    # Step 2: Process allauth paths and operations
    for path, item in (ext.get("paths") or {}).items():
        for method, op in list(item.items()):
            # Skip non-HTTP methods
            if method.lower() not in HTTP_METHODS or not isinstance(op, dict):
                continue

            # Add missing operationId (required for client generation)
            # Format: allauth_post_a1b2c3d4
            # Note: MD5 is used for hashing only, not for security
            op.setdefault(
                "operationId",
                f"allauth_{method}_{hashlib.md5(path.encode('utf-8'), usedforsecurity=False).hexdigest()[:8]}",
            )

            # Prefix tags for better organization in Swagger UI
            # Only add prefix if tag doesn't already start with "Authentication"
            old_tags = op.get("tags") or ["Other"]
            new_tags = []
            for tag in old_tags:
                if tag.startswith("Authentication"):
                    # Replace colon with slash for consistency: "Authentication: Account" -> "Authentication / Account"
                    new_tags.append(tag.replace("Authentication:", "Authentication /"))
                else:
                    # Add prefix to non-authentication tags
                    new_tags.append(f"Authentication / {tag}")
            op["tags"] = new_tags

    # Step 3: Transform error schemas to match drf-standardized-errors format
    ext_schemas = ext.get("components", {}).get("schemas", {})
    _transform_error_schemas(ext_schemas)

    # Step 4: Merge paths from allauth into main schema
    result.setdefault("paths", {}).update(ext.get("paths", {}) or {})

    # Step 5: Merge components (schemas, securitySchemes, etc.)
    base_comps = result.setdefault("components", {})
    for section, items in (ext.get("components") or {}).items():
        base_comps.setdefault(section, {}).update(items or {})

    # Step 6: Add top-level "Authentication" tag for better Swagger UI organization
    tags = result.setdefault("tags", [])
    if not any(t.get("name") == "Authentication" for t in tags):
        tags.insert(
            0,
            {
                "name": "Authentication",
                "description": (
                    "Authentication endpoints powered by Django-Allauth Headless. "
                    "Includes signup, login, logout, password reset, email verification, "
                    "and session management. All error responses use the standardized format."
                ),
            },
        )

    return result
