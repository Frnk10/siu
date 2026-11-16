import json

from django.db.models import ProtectedError
from rest_framework import mixins, permissions, viewsets
from rest_framework.exceptions import ValidationError

from usuarios.models import Empresa
from usuarios.permissions import ModeloPermisos
from usuarios.serializers import OpcionSerializer
from usuarios.views import BaseCrudViewSet

from .catalogo_utils import (
    empresa_del_empleado,
    empresas_del_usuario,
    filtrar_por_empresas,
    obtener_empresas,
)
from .models import Categoria, Marca, UnidadMedida
from .serializers import (
    CategoriaAdminSerializer, CategoriaLecturaSerializer,
    MarcaAdminSerializer, MarcaLecturaSerializer,
    UnidadMedidaAdminSerializer, UnidadMedidaLecturaSerializer,
)


# ---------- Opciones: empresas que representa el usuario (permisos propios) ----------
class MisEmpresasOpcionesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    serializer_class = OpcionSerializer

    def get_queryset(self):
        return Empresa.objects.filter(
            representante=self.request.user, estado="A"
        ).order_by("razon_social")


# =====================================================
# ADMINISTRADOR: CRUD de catálogos
# Hereda ModeloPermisos de BaseCrudViewSet (view/add/change/delete)
# =====================================================
class AdminCatalogoViewSet(BaseCrudViewSet):
    def get_queryset(self):
        ids = empresas_del_usuario(self.request.user)
        qs = filtrar_por_empresas(super().get_queryset(), ids)
        empresa = self.request.query_params.get("empresa")  # filtro opcional
        if empresa and empresa.isdigit() and int(empresa) in ids:
            qs = filtrar_por_empresas(qs, [int(empresa)])
        return qs

    def validar_retiro(self, instance, empresas):
        """Cada viewset revisa si las empresas que se retiran aún lo usan."""
        pass

    def perform_destroy(self, instance):
        permitidas = set(empresas_del_usuario(self.request.user))
        actuales = set(obtener_empresas(instance))

        # Por defecto se retiran todas tus empresas; con ?empresa=<id> solo esa
        retirar = actuales & permitidas
        pedida = self.request.query_params.get("empresa")
        if pedida:
            if not pedida.isdigit() or int(pedida) not in retirar:
                raise ValidationError({"detail": "Este registro no está asignado a esa empresa."})
            retirar = {int(pedida)}
        if not retirar:
            raise ValidationError({"detail": "Este registro no pertenece a tus empresas."})

        self.validar_retiro(instance, retirar)
        restantes = actuales - retirar

        if restantes:
            # Otras empresas lo siguen usando: solo se les quita las tuyas
            instance.id_texto_Empresa = json.dumps(sorted(restantes))
            instance.usuario_actualiza = self.request.user
            instance.save(update_fields=["id_texto_Empresa", "usuario_actualiza", "fecha_actualiza"])
            return

        # Nadie más lo usa: se elimina de la base de datos
        try:
            instance.delete()
        except ProtectedError:
            raise ValidationError({"detail": "No se puede eliminar: todavía está en uso."})


class UnidadMedidaAdminViewSet(AdminCatalogoViewSet):
    queryset = UnidadMedida.objects.all().order_by("nombre")
    serializer_class = UnidadMedidaAdminSerializer

    def validar_retiro(self, instance, empresas):
        if instance.unidad_medida.filter(estado="A", id_empresa__in=empresas).exists():
            raise ValidationError({"detail": "No se puede retirar: hay productos de esa empresa con esta unidad."})


class MarcaAdminViewSet(AdminCatalogoViewSet):
    queryset = Marca.objects.all().order_by("nombre")
    serializer_class = MarcaAdminSerializer

    def validar_retiro(self, instance, empresas):
        if instance.marca.filter(estado="A", id_empresa__in=empresas).exists():
            raise ValidationError({"detail": "No se puede retirar: hay productos de esa empresa con esta marca."})


class CategoriaAdminViewSet(AdminCatalogoViewSet):
    queryset = Categoria.objects.all().order_by("nombre")
    serializer_class = CategoriaAdminSerializer

    def validar_retiro(self, instance, empresas):
        if instance.categoria.filter(estado="A", id_empresa__in=empresas).exists():
            raise ValidationError({"detail": "No se puede retirar: hay productos de esa empresa en esta categoría."})
        # Subcategorías que dependen de esta en las empresas que se retiran
        for hija in Categoria.objects.filter(codigo_padre=instance.pk):
            if set(obtener_empresas(hija)) & set(empresas):
                raise ValidationError({"detail": "No se puede retirar: tiene subcategorías en esa empresa."})


# =====================================================
# EMPLEADO: solo lectura, empresa a la que pertenece
# Solo permite GET, así que exige el permiso view del modelo
# =====================================================
class EmpleadoCatalogoViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [ModeloPermisos]
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
    