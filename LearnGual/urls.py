from django.contrib import admin
from django.urls import path, include


from .docs_generator import core_schema_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.urls")),
    path("api/v1/", include("app.urls")),
    # documentation paths
    path(
        "docs/",
        core_schema_view.with_ui("swagger", cache_timeout=0),
        name="core-swagger-ui",
    ),
]


# handler404 = "apps.core.views.handler404"
