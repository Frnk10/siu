from django.urls import path
from Aplicaciones.user.api import *
from Aplicaciones.inventario.api.views.general_views import *
from Aplicaciones.inventario.api.views.imagenes_views import *
from Aplicaciones.inventario.api.views.producto_views import *
from Aplicaciones.inventario.api.views.CategoriaView import *

urlpatterns = [
    path('categoria/listarTodos/', CategoriaListarTodosView.as_view(), name='categoria_listar_todos'),
    path('categoria/listar/<str:estado>/', CategoriaListarView.as_view(), name='categoria_listar'),
    path('categoria/crear/', CategoriaCrearView.as_view(), name='categoria_crear'),
    path('categoria/detallar/<int:pk>/', CategoriaDetallarView.as_view(), name='categoria_detallar'),
    path('categoria/actualizar/<int:pk>/', CategoriaActualizarView.as_view(), name='categoria_actualizar'),
    path('categoria/cambiarEstado/<int:codigo>/<str:estado>/', CategoriaCambiarEstadoView.as_view(), name='genero_cambiar_estado'),

    path('unidades_medida/', UnidadMedidaListarAPI.as_view(), name='unidad_medida_list'),
    path('marcas/', MarcaListarAPI.as_view(), name='marca_list'),
    path('productos/', ProductoListarAPI.as_view(), name='producto_list'),
    path('productos/crear/', ProductoCrearAPI.as_view(), name='producto_create'),
    path('productos/detallar/<int:codigo>/', ProductoDetallarAPI.as_view(), name='producto_detalle'),
    path('productos/cambiarestado/<int:codigo>/',ProductoCambiarEstadoAPI.as_view(), name='producto_delete'),
    path('imagenes/', ImagenProductoListarAPI.as_view(), name='imagen_producto_list'),
]