from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path('api/v1/wallets/', include('wallets.urls')),
    path('admin/', admin.site.urls),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Bank API",
        default_version='v1',
        description="REST приложения для работы с электронными кошельками",
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ]
)

urlpatterns += [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
