from rest_framework.routers import DefaultRouter

from Aplicaciones.inventario.api.viewsets.unidad_medida_viewsets import (
    UnidadMedidaViewSet,
)
from Aplicaciones.inventario.api.viewsets.categoria_viewsets import (
    CategoriaViewSet,
)
from Aplicaciones.inventario.api.viewsets.marca_viewsets import (
    MarcaViewSet,
)
from Aplicaciones.inventario.api.viewsets.producto_viewsets import (
    ProductoViewSet,
)
from Aplicaciones.inventario.api.viewsets.imagen_producto_viewsets import (
    ImagenProductoViewSet,
)

router = DefaultRouter()

router.register(r'unidades-medida', UnidadMedidaViewSet, basename='unidades_medida')
router.register(r'categorias', CategoriaViewSet, basename='categorias')
router.register(r'marcas', MarcaViewSet, basename='marcas')
router.register(r'productos', ProductoViewSet, basename='productos')
router.register(r'imagenes-producto', ImagenProductoViewSet, basename='imagenes_producto')

urlpatterns = router.urls