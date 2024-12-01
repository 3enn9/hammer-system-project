from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Укажите описание вашего API
schema_view = get_schema_view(
   openapi.Info(
      title="My API",
      default_version='v1',
      description="Описание API вашего проекта",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myapi.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hammersite.urls')),


    # Путь для документации с использованием ReDoc
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
