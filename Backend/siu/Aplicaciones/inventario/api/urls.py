from django.urls import path
from Aplicaciones.user.api import *
from Aplicaciones.inventario.api.views.general_views import *
from Aplicaciones.inventario.api.views.imagenes_views import *
from Aplicaciones.inventario.api.views.producto_views import *
urlpatterns = [
    path('unidades_medida/', UnidadMedidaListarAPI.as_view(), name='unidad_medida_list'),
    path('categorias/', CategoriaListarAPI.as_view(), name='categoria_list'),
    path('marcas/', MarcaListarAPI.as_view(), name='marca_list'),
    path('productos/', ProductoListarAPI.as_view(), name='producto_list'),
    path('productos/crear/', ProductoCrearAPI.as_view(), name='producto_create'),
    path('productos/detallar/<int:codigo>/', ProductoDetallarAPI.as_view(), name='producto_detalle'),
    path('productos/cambiarestado/<int:codigo>/',ProductoCambiarEstadoAPI.as_view(), name='producto_delete'),
    path('imagenes/', ImagenProductoListarAPI.as_view(), name='imagen_producto_list'),
]