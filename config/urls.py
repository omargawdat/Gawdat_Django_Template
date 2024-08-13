from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView

# Core URL patterns
core_patterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("sentry-debug/", lambda request: 1 / 0, name="sentry-debug"),
]

# API URL patterns
api_doc_patterns = [
    path("schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="api-schema"), name="api-docs"),
]

api_core_patterns = [
    path("", include("config.api_router")),
]

api_app_patterns = [
    path("", include("apps.users.api.customer.urls")),
    path("", include("apps.users.api.provider.urls")),
    path("", include("apps.users.api.user.urls")),
]

api_patterns = [
    path("", include(api_core_patterns)),
    path("", include(api_app_patterns)),
    path("", include(api_doc_patterns)),
]

# Main URL patterns
urlpatterns = [
    *core_patterns,
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    path("api/", include(api_patterns)),
]

# Debug toolbar (only in DEBUG mode)
if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns.insert(0, path("__debug__/", include(debug_toolbar.urls)))
