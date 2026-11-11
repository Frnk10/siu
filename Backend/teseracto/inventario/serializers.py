import json

from rest_framework import serializers

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


# =====================================================
# ADMIN: mixin común
# =====================================================
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

    def _duplicado(self, campo, valor, ids, mensaje):
        """Error si otro registro activo con el mismo valor comparte alguna empresa."""
        qs = self.modelo.objects.filter(**{f"{campo}__iexact": valor}, estado="A")
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        for r in qs:
            if set(obtener_empresas(r)) & set(ids):
                raise serializers.ValidationError({campo: mensaje})

    def validate(self, attrs):
        attrs = super().validate(attrs)
        permitidas = set(empresas_del_usuario(self.context["request"].user))

        if self.instance:
            actuales = set(obtener_empresas(self.instance))
            if not actuales <= permitidas:
                raise serializers.ValidationError(
                    {"detail": f"No puedes modificar esta {self.etiqueta}: incluye empresas que no representas."}
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
        if nombre and estado == "A":
            self._duplicado(
                "nombre", nombre, ids,
                f"Ya existe una {self.etiqueta} activa con ese nombre en alguna de las empresas elegidas.",
            )

        if "id_texto_Empresa" in attrs:
            attrs["id_texto_Empresa"] = json.dumps(ids)
        return attrs


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