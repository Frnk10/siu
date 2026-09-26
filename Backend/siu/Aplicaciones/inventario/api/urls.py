from django.urls import path
from Aplicaciones.user.api import *
from Aplicaciones.inventario.api.views.general_views import *
from Aplicaciones.inventario.api.views.imagenes_views import *
from Aplicaciones.inventario.api.views.producto_views import *
urlpatterns = [
    path('unidades_medida/', UnidadMedidaListAPIView.as_view(), name='unidad_medida_list'),
    path('categorias/', CategoriaListAPIView.as_view(), name='categoria_list'),
    path('marcas/', MarcaListAPIView.as_view(), name='marca_list'),
    path('productos/', ProductoListAPIView.as_view(), name='producto_list'),
    path('productos/crear/', ProductoCreateAPIView.as_view(), name='producto_create'),
    path('imagenes/', ImagenProductoListAPIView.as_view(), name='imagen_producto_list'),
]