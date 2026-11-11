from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets
from rest_framework.exceptions import ValidationError

from usuarios.models import Empresa
from usuarios.views import BaseCrudViewSet
from usuarios.serializers import OpcionSerializer

from .catalogo_utils import empresa_del_empleado, empresas_del_usuario, filtrar_por_empresas
from .models import Categoria, Marca, UnidadMedida
from .serializers import (
    CategoriaAdminSerializer, CategoriaLecturaSerializer,
    MarcaAdminSerializer, MarcaLecturaSerializer,
    UnidadMedidaAdminSerializer, UnidadMedidaLecturaSerializer,
)


# ---------- Opciones: empresas que representa el usuario ----------
class MisEmpresasOpcionesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    serializer_class = OpcionSerializer

    def get_queryset(self):
        return Empresa.objects.filter(representante=self.request.user, estado="A").order_by("razon_social")


# =====================================================
# ADMINISTRADOR (representante): CRUD + asignar empresas
# =====================================================
class AdminCatalogoViewSet(BaseCrudViewSet):
    def get_queryset(self):
        ids = empresas_del_usuario(self.request.user)
        qs = filtrar_por_empresas(super().get_queryset(), ids)
        empresa = self.request.query_params.get("empresa")  # filtro opcional
        if empresa and empresa.isdigit() and int(empresa) in ids:
            qs = filtrar_por_empresas(qs, [int(empresa)])
        return qs


class UnidadMedidaAdminViewSet(AdminCatalogoViewSet):
    queryset = UnidadMedida.objects.all().order_by("estado", "nombre")
    serializer_class = UnidadMedidaAdminSerializer

    def validar_baja(self, instance):
        if instance.unidad_medida.filter(estado="A").exists():
            raise ValidationError({"detail": "No se puede desactivar: hay productos activos con esta unidad."})


class CategoriaAdminViewSet(AdminCatalogoViewSet):
    queryset = Categoria.objects.all().order_by("estado", "nombre")
    serializer_class = CategoriaAdminSerializer

    def validar_baja(self, instance):
        if instance.categoria.filter(estado="A").exists():
            raise ValidationError({"detail": "No se puede desactivar: hay productos activos en esta categoría."})
        if Categoria.objects.filter(codigo_padre=instance.pk, estado="A").exists():
            raise ValidationError({"detail": "No se puede desactivar: tiene subcategorías activas."})


class MarcaAdminViewSet(AdminCatalogoViewSet):
    queryset = Marca.objects.all().order_by("estado", "nombre")
    serializer_class = MarcaAdminSerializer

    def validar_baja(self, instance):
        if instance.marca.filter(estado="A").exists():
            raise ValidationError({"detail": "No se puede desactivar: hay productos activos con esta marca."})


# =====================================================
# EMPLEADO: solo lectura, empresa a la que pertenece
# =====================================================
class EmpleadoCatalogoViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        empresa = empresa_del_empleado(self.request.user)
        qs = super().get_queryset().filter(estado="A")
        return filtrar_por_empresas(qs, [empresa])


class UnidadMedidaEmpleadoViewSet(EmpleadoCatalogoViewSet):
    queryset = UnidadMedida.objects.order_by("nombre")
    serializer_class = UnidadMedidaLecturaSerializer


class CategoriaEmpleadoViewSet(EmpleadoCatalogoViewSet):
    queryset = Categoria.objects.order_by("nombre")
    serializer_class = CategoriaLecturaSerializer


class MarcaEmpleadoViewSet(EmpleadoCatalogoViewSet):
    queryset = Marca.objects.order_by("nombre")
    serializer_class = MarcaLecturaSerializer
