from django.contrib import admin
from django.urls import path, re_path
from django.urls import include
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from Aplicaciones.seguridad.views import Login, Logout

schema_view = get_schema_view(
   openapi.Info(
      title="Documentación de Sistema SIU",
      default_version='v0.1',
      description="Documentación SIU",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="developerpeperu@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('admin/', admin.site.urls),
   path('', include('Aplicaciones.user.urls')),
   path('inventario/', include('Aplicaciones.inventario.api.routers')),
   path('logout/', Logout.as_view(), name = 'logout'),
   path('login/',Login.as_view(), name = 'login'),
]
