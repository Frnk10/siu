
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get("username", "").strip()
        email = attrs.get("email", "").strip()
        password = attrs.get("password")

        # Se debe enviar username o email, pero no ambos.
        if bool(username) == bool(email):
            raise serializers.ValidationError(
                "Ingresa tu username o tu email."
            )

        # Si se ingresa email, buscar el usuario correspondiente.
        if email:
            user_obj = User.objects.filter(email__iexact=email).first()

            if user_obj is None:
                raise serializers.ValidationError(
                    "Credenciales incorrectas."
                )

            username = user_obj.get_username()

        user = authenticate(
            request=self.context.get("request"),
            username=username,
            password=password,
        )

        if user is None:
            raise serializers.ValidationError(
                "Credenciales incorrectas."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "Esta cuenta está desactivada."
            )

        attrs["user"] = user
        return attrs


import re

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from .models import Configuracion, Empresa, EmpresaConfiguracion, Sucursal

Usuario = get_user_model()

TELEFONO_RE = re.compile(r"^\+?\d{7,15}$")
CODIGO_RE = re.compile(r"^[A-Z0-9_]+$")
LOGO_MAX_BYTES = 2 * 1024 * 1024
LOGO_TIPOS = {"image/png", "image/jpeg", "image/webp"}


def limpiar(texto):
    """Quita espacios al inicio/fin y colapsa espacios repetidos."""
    return " ".join((texto or "").split())


class OpcionSerializer(serializers.Serializer):
    """{id, name} para llenar los selects del frontend."""

    id = serializers.ReadOnlyField(source="pk")
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return str(obj)


# =========================================================
# EMPRESA
# =========================================================
class EmpresaSerializer(serializers.ModelSerializer):
    representante = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.filter(is_active=True),
        required=False,
        allow_null=True,
        error_messages={"does_not_exist": "El representante no existe o está inactivo."},
    )
    logotipo = serializers.ImageField(required=False, allow_null=True)
    representante_nombre = serializers.SerializerMethodField()
    localidad_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Empresa
        fields = (
            "codigo", "razon_social", "representante", "representante_nombre",
            "fecha_constitucion", "calle_principal", "calle_secundaria",
            "telefono", "obligado_contabilidad", "facturacion_electronica",
            "logotipo", "localidad", "localidad_nombre", "estado",
        )
        read_only_fields = ("codigo", "estado")

    def get_representante_nombre(self, obj):
        return str(obj.representante) if obj.representante else ""

    def get_localidad_nombre(self, obj):
        return str(obj.localidad) if obj.localidad else ""

    def validate_razon_social(self, value):
        value = limpiar(value)
        if len(value) < 3:
            raise serializers.ValidationError("La razón social debe tener al menos 3 caracteres.")
        existe = Empresa.objects.filter(razon_social__iexact=value, estado="A")
        if self.instance:
            existe = existe.exclude(pk=self.instance.pk)
        if existe.exists():
            raise serializers.ValidationError("Ya existe una empresa con esa razón social.")
        return value

    def validate_telefono(self, value):
        value = value.replace(" ", "").replace("-", "")
        if value and not TELEFONO_RE.match(value):
            raise serializers.ValidationError("Teléfono inválido: use de 7 a 15 dígitos (puede iniciar con +).")
        return value

    def validate_fecha_constitucion(self, value):
        if value and value > timezone.localdate():
            raise serializers.ValidationError("La fecha de constitución no puede ser futura.")
        return value

    def validate_calle_principal(self, value):
        return limpiar(value)

    def validate_calle_secundaria(self, value):
        return limpiar(value)

    def validate_logotipo(self, value):
        if value:
            if value.size > LOGO_MAX_BYTES:
                raise serializers.ValidationError("El logotipo no puede superar los 2 MB.")
            tipo = getattr(value, "content_type", None)
            if tipo and tipo not in LOGO_TIPOS:
                raise serializers.ValidationError("El logotipo debe ser PNG, JPG o WEBP.")
        return value


# =========================================================
# SUCURSAL
# =========================================================
class SucursalSerializer(serializers.ModelSerializer):
    empresa = serializers.PrimaryKeyRelatedField(
        queryset=Empresa.objects.filter(estado="A"),
        error_messages={"does_not_exist": "La empresa no existe o está inactiva."},
    )
    empresa_nombre = serializers.CharField(source="empresa.razon_social", read_only=True)
    localidad_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Sucursal
        fields = (
            "codigo", "empresa", "empresa_nombre", "localidad", "localidad_nombre",
            "nombre", "calle_principal", "calle_secundaria", "estado",
        )
        read_only_fields = ("codigo", "estado")

    def get_localidad_nombre(self, obj):
        return str(obj.localidad) if obj.localidad else ""

    def validate_nombre(self, value):
        value = limpiar(value)
        if len(value) < 2:
            raise serializers.ValidationError("El nombre debe tener al menos 2 caracteres.")
        return value

    def validate_calle_principal(self, value):
        return limpiar(value)

    def validate_calle_secundaria(self, value):
        return limpiar(value)

    def validate(self, attrs):
        empresa = attrs.get("empresa") or getattr(self.instance, "empresa", None)
        nombre = attrs.get("nombre") or getattr(self.instance, "nombre", None)
        existe = Sucursal.objects.filter(empresa=empresa, nombre__iexact=nombre, estado="A")
        if self.instance:
            existe = existe.exclude(pk=self.instance.pk)
        if existe.exists():
            raise serializers.ValidationError(
                {"nombre": "Ya existe una sucursal con ese nombre en esta empresa."}
            )
        return attrs


# =========================================================
# CONFIGURACIÓN
# =========================================================
class ConfiguracionSerializer(serializers.ModelSerializer):
    # Se declara sin el UniqueValidator automático para dar un mensaje propio
    codigo_auxiliar = serializers.CharField(max_length=30)

    class Meta:
        model = Configuracion
        fields = ("codigo", "codigo_auxiliar", "nombre", "descripcion", "grupo", "estado")
        read_only_fields = ("codigo", "estado")

    def validate_codigo_auxiliar(self, value):
        value = value.strip().upper()
        if not CODIGO_RE.match(value):
            raise serializers.ValidationError("Solo letras mayúsculas, números y guion bajo (sin espacios).")
        existe = Configuracion.objects.filter(codigo_auxiliar__iexact=value)
        if self.instance:
            existe = existe.exclude(pk=self.instance.pk)
        if existe.exists():
            raise serializers.ValidationError("Ya existe una configuración con ese código (puede estar inactiva).")
        return value

    def validate_nombre(self, value):
        return limpiar(value)

    def validate_grupo(self, value):
        value = limpiar(value)
        if not value:
            raise serializers.ValidationError("El grupo es obligatorio.")
        return value

    def validate_descripcion(self, value):
        return limpiar(value)


# =========================================================
# EMPRESA - CONFIGURACIÓN
# =========================================================
class EmpresaConfiguracionSerializer(serializers.ModelSerializer):
    empresa = serializers.PrimaryKeyRelatedField(
        queryset=Empresa.objects.filter(estado="A"),
        error_messages={"does_not_exist": "La empresa no existe o está inactiva."},
    )
    configuracion = serializers.PrimaryKeyRelatedField(
        queryset=Configuracion.objects.filter(estado="A"),
        error_messages={"does_not_exist": "La configuración no existe o está inactiva."},
    )
    empresa_nombre = serializers.CharField(source="empresa.razon_social", read_only=True)
    configuracion_nombre = serializers.CharField(source="configuracion.nombre", read_only=True)
    configuracion_grupo = serializers.CharField(source="configuracion.grupo", read_only=True)

    class Meta:
        model = EmpresaConfiguracion
        fields = (
            "id", "empresa", "empresa_nombre", "configuracion", "configuracion_nombre",
            "configuracion_grupo", "valor", "estado",
        )
        read_only_fields = ("id", "estado")
        validators = []  # el control de duplicados se hace abajo con mensaje propio

    def validate_valor(self, value):
        return value.strip()

    def validate(self, attrs):
        empresa = attrs.get("empresa") or getattr(self.instance, "empresa", None)
        configuracion = attrs.get("configuracion") or getattr(self.instance, "configuracion", None)
        existe = EmpresaConfiguracion.objects.filter(empresa=empresa, configuracion=configuracion)
        if self.instance:
            existe = existe.exclude(pk=self.instance.pk)
        if existe.exists():
            raise serializers.ValidationError(
                {"configuracion": "Esta empresa ya tiene un valor para esa configuración."}
            )
        return attrs

