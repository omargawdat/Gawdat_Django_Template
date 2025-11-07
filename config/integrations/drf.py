# REST Framework settings
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "allauth.headless.contrib.rest_framework.authentication.XSessionTokenAuthentication",
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
        # DRF Standardized Errors
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
        # App-specific Type fields (to avoid enum naming collisions)
        "WalletTransactionTypeEnum": "apps.payment.constants.WalletTransactionType",
        "PaymentTypeEnum": "apps.payment.constants.PaymentType",
        "NotificationTypeEnum": "apps.channel.constants.NotificationType",
        "DeviceTypeEnum": "apps.channel.constants.DeviceType",
        "UserTypeEnum": "apps.users.constants.UserType",
    },
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields",
        "drf_standardized_errors.openapi_hooks.postprocess_schema_enums",
        "config.schema_hooks.merge_allauth_spec",  # Merge django-allauth headless endpoints
    ],
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    "EXTERNAL_DOCS": {"description": "allauth", "url": "/_allauth/openapi.html"},
}
