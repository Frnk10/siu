import json

from rest_framework import serializers
from django.db import transaction
from .models import Categoria, Marca, UnidadMedida
from .catalogo_utils import empresas_del_usuario, obtener_empresas, parse_empresas
from usuarios.models import Empresa
from validaciones.validaciones_serializers import validar_codigo, validar_nombre


# =====================================================
# CAMPO "empresas" (lista de ids <-> id_texto_Empresa)
# =====================================================
class EmpresasField(serializers.Field):
    def to_representation(self, value):
        return parse_empresas(value)

    def to_internal_value(self, data):
        if not isinstance(data, list) or not data:
            raise serializers.ValidationError("Selecciona al menos una empresa.")
        try:
            return sorted({int(x) for x in data})
        except (ValueError, TypeError):
            raise serializers.ValidationError("Lista de empresas inválida.")

class AdminCatalogoMixin(serializers.Serializer):
    modelo = None
    etiqueta = "registro"

    empresas = EmpresasField(source="id_texto_Empresa")
    empresas_nombres = serializers.SerializerMethodField()

    def get_empresas_nombres(self, obj):
        if not hasattr(self, "_nombres"):
            ids = empresas_del_usuario(self.context["request"].user)
            self._nombres = dict(
                Empresa.objects.filter(codigo__in=ids).values_list("codigo", "razon_social")
            )
        return ", ".join(self._nombres[i] for i in obtener_empresas(obj) if i in self._nombres)

    def validate_nombre(self, value):
        return validar_nombre(value.strip().upper(), "El nombre", minimo=3, maximo=100)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        permitidas = set(empresas_del_usuario(self.context["request"].user))

        if self.instance:
            actuales = set(obtener_empresas(self.instance))
            if not actuales <= permitidas:
                raise serializers.ValidationError(
                    {"detail": f"No puedes modificar esta {self.etiqueta}: está compartida con empresas que no representas."}
                )
        else:
            actuales = set()

        ids = attrs.get("id_texto_Empresa")
        if ids is not None and not set(ids) <= permitidas:
            raise serializers.ValidationError(
                {"empresas": "Solo puedes asignar empresas activas que representas."}
            )
        ids = ids if ids is not None else sorted(actuales)
        self._ids = ids

        nombre = attrs.get("nombre", getattr(self.instance, "nombre", None))
        estado = attrs.get("estado", getattr(self.instance, "estado", "A"))

        # Al EDITAR no se puede tomar el nombre de otro registro activo.
        # Al CREAR no se valida aquí: si existe, se fusiona en create().
        if self.instance and nombre and estado == "A":
            repetido = (
                self.modelo.objects.filter(nombre__iexact=nombre, estado="A")
                .exclude(pk=self.instance.pk)
                .exists()
            )
            if repetido:
                raise serializers.ValidationError(
                    {"nombre": f"Ya existe otra {self.etiqueta} activa con ese nombre."}
                )

        if "id_texto_Empresa" in attrs:
            attrs["id_texto_Empresa"] = json.dumps(ids)
        return attrs

    def validar_compatible(self, existente, validated_data):
        """Los serializers hijos revisan otros campos antes de compartir un registro."""
        pass

    def create(self, validated_data):
        nuevos = set(parse_empresas(validated_data["id_texto_Empresa"]))
        nombre = validated_data["nombre"]

        with transaction.atomic():
            existente = (
                self.modelo.objects.select_for_update()
                .filter(nombre__iexact=nombre)
                .first()
            )

            if existente is None:
                return super().create(validated_data)

            if existente.estado != "A":
                raise serializers.ValidationError(
                    {"nombre": f"Ya existe una {self.etiqueta} con ese nombre, pero está inactiva."}
                )

            self.validar_compatible(existente, validated_data)

            union = sorted(set(obtener_empresas(existente)) | nuevos)
            existente.id_texto_Empresa = json.dumps(union)
            existente.usuario_actualiza = validated_data.get("usuario_actualiza")
            existente.save(update_fields=["id_texto_Empresa", "usuario_actualiza", "fecha_actualiza"])
            return existente


# =====================================================
# ADMIN: serializers
# =====================================================
class UnidadMedidaAdminSerializer(AdminCatalogoMixin, serializers.ModelSerializer):
    modelo = UnidadMedida
    etiqueta = "unidad de medida"

    class Meta:
        model = UnidadMedida
        fields = ("codigo", "abreviatura", "nombre", "empresas", "empresas_nombres", "estado")
        read_only_fields = ("codigo",)

    def validate_abreviatura(self, value):
        return validar_codigo(value.strip().upper(), "La abreviatura", minimo=1, maximo=10)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        abrev = attrs.get("abreviatura", getattr(self.instance, "abreviatura", None))
        estado = attrs.get("estado", getattr(self.instance, "estado", "A"))
        if abrev and estado == "A":
            self._duplicado(
                "abreviatura", abrev, self._ids,
                "Ya existe una unidad activa con esa abreviatura en alguna de las empresas elegidas.",
            )
        return attrs
    
    def validar_compatible(self, existente, validated_data):
        abrev = validated_data.get("abreviatura")
        if abrev and existente.abreviatura.upper() != abrev.upper():
            raise serializers.ValidationError({
                "abreviatura": f"La unidad {existente.nombre} ya existe con la abreviatura {existente.abreviatura}."
            })


class MarcaAdminSerializer(AdminCatalogoMixin, serializers.ModelSerializer):
    modelo = Marca
    etiqueta = "marca"

    class Meta:
        model = Marca
        fields = ("codigo", "nombre", "empresas", "empresas_nombres", "estado")
        read_only_fields = ("codigo",)


class CategoriaAdminSerializer(AdminCatalogoMixin, serializers.ModelSerializer):
    modelo = Categoria
    etiqueta = "categoría"
    padre_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = ("codigo", "codigo_padre", "padre_nombre", "nombre", "empresas", "empresas_nombres", "estado")
        read_only_fields = ("codigo",)

    def get_padre_nombre(self, obj):
        if not obj.codigo_padre:
            return ""
        return Categoria.objects.filter(pk=obj.codigo_padre).values_list("nombre", flat=True).first() or ""

    def validate(self, attrs):
        attrs = super().validate(attrs)
        padre_id = attrs.get("codigo_padre", getattr(self.instance, "codigo_padre", None))
        if padre_id is None:
            return attrs

        padre = Categoria.objects.filter(pk=padre_id).first()
        if not padre:
            raise serializers.ValidationError({"codigo_padre": "La categoría padre no existe."})
        if padre.estado != "A":
            raise serializers.ValidationError({"codigo_padre": "La categoría padre está inactiva."})
        # El padre debe estar disponible en todas las empresas de la hija
        if not set(self._ids) <= set(obtener_empresas(padre)):
            raise serializers.ValidationError(
                {"codigo_padre": "La categoría padre no está asignada a todas las empresas elegidas."}
            )

        if self.instance:  # evita ciclos
            actual, vistos = padre, set()
            while actual and actual.pk not in vistos:
                if actual.pk == self.instance.pk:
                    raise serializers.ValidationError({"codigo_padre": "No puedes crear ciclos entre categorías."})
                vistos.add(actual.pk)
                actual = Categoria.objects.filter(pk=actual.codigo_padre).first() if actual.codigo_padre else None
        return attrs

    def validar_compatible(self, existente, validated_data):
        if existente.codigo_padre != validated_data.get("codigo_padre"):
            raise serializers.ValidationError({
                "codigo_padre": "Esta categoría ya existe con otra categoría padre."
            })


# =====================================================
# LECTURA: empleados y catálogo público (sin datos internos)
# =====================================================
class UnidadMedidaLecturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadMedida
        fields = ("codigo", "abreviatura", "nombre")


class MarcaLecturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ("codigo", "nombre")


class CategoriaLecturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ("codigo", "codigo_padre", "nombre")