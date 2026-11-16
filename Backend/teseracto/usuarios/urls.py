from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import * 

router = DefaultRouter()
router.register('login', LoginViewset, basename='login')
router.register("empresas", EmpresaViewSet, basename="empresa")
router.register("sucursales", SucursalViewSet, basename="sucursal")
router.register("configuraciones", ConfiguracionViewSet, basename="configuracion")
router.register("empresa_configuraciones", EmpresaConfiguracionViewSet, basename="empresa_configuracion")
router.register("opciones/usuarios", UsuarioOpcionesViewSet, basename="opciones_usuarios")
router.register("opciones/localidades", LocalidadOpcionesViewSet, basename="opciones_localidades")
router.register("menu", MenuViewSet, basename="menu")
router.register('', ConfigViewSet, basename='config')
router.register("empleados", EmpleadoViewSet, basename="empleado")
router.register("clientes", ClienteViewSet, basename="cliente")
router.register("proveedores", ProveedorViewSet, basename="proveedor")
urlpatterns = router.urls
