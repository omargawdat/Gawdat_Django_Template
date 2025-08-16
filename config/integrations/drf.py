from datetime import timedelta

from config.helpers.env import env

# REST Framework settings
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_standardized_errors.openapi.AutoSchema",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "600/day", "user": "2000/day"},
    "COERCE_DECIMAL_TO_STRING": False,
}

DRF_STANDARDIZED_ERRORS = {
    "ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS": True,
    "EXCEPTION_HANDLER_CLASS": "config.helpers.exception_handler.CustomExceptionHandler",
}
CORS_URLS_REGEX = r"^/api/.*$"

# drf-spectacular
SPECTACULAR_SETTINGS = {
    "VERSION": "1.0.0",
    "OAS_VERSION": "3.1.0",
    "TITLE": "projectname API",
    "DESCRIPTION": "Documentation of API endpoints of projectname App",
    "SCHEMA_PATH_PREFIX": "/api/",
    "SORT_OPERATIONS": False,
    "SORT_OPERATION_PARAMETERS": True,
    "CAMELIZE_NAMES": False,
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "COMPONENT_SPLIT_PATCH": True,
    "COMPONENT_SPLIT_RESPONSE": True,
    "ENABLE_DJANGO_DEPLOY_CHECK": True,
    "ENUM_SUFFIX": "Enum",
    "ENUM_NAME_OVERRIDES": {
        "ValidationErrorEnum": "drf_standardized_errors.openapi_serializers.ValidationErrorEnum.choices",
        "ClientErrorEnum": "drf_standardized_errors.openapi_serializers.ClientErrorEnum.choices",
        "ServerErrorEnum": "drf_standardized_errors.openapi_serializers.ServerErrorEnum.choices",
        "ErrorCode401Enum": "drf_standardized_errors.openapi_serializers.ErrorCode401Enum.choices",
        "ErrorCode403Enum": "drf_standardized_errors.openapi_serializers.ErrorCode403Enum.choices",
        "ErrorCode404Enum": "drf_standardized_errors.openapi_serializers.ErrorCode404Enum.choices",
        "ErrorCode405Enum": "drf_standardized_errors.openapi_serializers.ErrorCode405Enum.choices",
        "ErrorCode406Enum": "drf_standardized_errors.openapi_serializers.ErrorCode406Enum.choices",
        "ErrorCode415Enum": "drf_standardized_errors.openapi_serializers.ErrorCode415Enum.choices",
        "ErrorCode429Enum": "drf_standardized_errors.openapi_serializers.ErrorCode429Enum.choices",
        "ErrorCode500Enum": "drf_standardized_errors.openapi_serializers.ErrorCode500Enum.choices",
    },
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields",
        "drf_standardized_errors.openapi_hooks.postprocess_schema_enums",
    ],
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "jwtAuth": {
                "type": "http",
                "scheme": "bearer",
                # No bearerFormat specified # todo: as apidog has bug when the bearerFormat is specified it detect the whole schema as jwt
            }
        }
    },
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=env.django_jwt_access_token_lifetime_minutes
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        minutes=env.django_jwt_refresh_token_lifetime_minutes
    ),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "REUSE_REFRESH_TOKENS": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": env.django_secret_key.get_secret_value(),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}
