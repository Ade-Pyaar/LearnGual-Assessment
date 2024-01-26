from django.conf import settings

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator

from rest_framework import permissions


class CoreAPISchemeGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.base_path = "/api/v1/"

        if settings.DEBUG:
            schema.schemes = ["http"]
        else:
            schema.schemes = ["https"]
        return schema


core_schema_view = get_schema_view(
    openapi.Info(
        title="Assessment Core API Documentation",
        default_version="v1",
        description="API documentation for core operations",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="Adebayoibrahim2468@gmail.com"),
        license=openapi.License(name="Leemao"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    urlconf="app.urls",
    generator_class=CoreAPISchemeGenerator,
)
