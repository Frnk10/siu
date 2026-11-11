from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import * 

router = DefaultRouter()
# Admin: mismas rutas que ya usa el frontend
router.register("unidades_medida", UnidadMedidaAdminViewSet, basename="unidad_medida_admin")
router.register("categorias", CategoriaAdminViewSet, basename="categoria-admin")
router.register("marcas", MarcaAdminViewSet, basename="marca-admin")

# Empleado
router.register("empleado/unidades_medida", UnidadMedidaEmpleadoViewSet, basename="unidad_medida_empleado")
router.register("empleado/categorias", CategoriaEmpleadoViewSet, basename="categoria_empleado")
router.register("empleado/marcas", MarcaEmpleadoViewSet, basename="marca_empleado")

# Opciones
router.register("opciones/mis_empresas", MisEmpresasOpcionesViewSet, basename="opciones_mis_empresas")

urlpatterns = router.urls
