import re

from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from .models import Configuracion, Empresa, EmpresaConfiguracion, Sucursal
from validaciones.validaciones_serializers import (
    validar_fecha_rango,
    validar_logotipo,
    validar_reactivacion,
    validar_telefono,
    validar_texto,
    validar_codigo,
    validar_nombre,
    validar_unico,
)

User = get_user_model()
Usuario = User

CODIGO_RE = re.compile(r"^[A-Z0-9_]+$")


def limpiar(texto):
    """Quita espacios al inicio/fin y colapsa espacios repetidos."""
    return " ".join((texto or "").split())


from .models import Localidad


def _campo_padre():
    """Nombre del campo FK de Localidad hacia sí misma (el nivel superior)."""
    for f in Localidad._meta.get_fields():
        if f.is_relation and f.many_to_one and f.related_model is Localidad:
            return f.name
    return None


class LocalidadJerarquiaMixin(serializers.Serializer):
    localidad_canton = serializers.SerializerMethodField()
    localidad_provincia = serializers.SerializerMethodField()

    def _cadena(self, obj):
        """[parroquia, cantón, provincia] según lo que exista."""
        campo = _campo_padre()
        cadena, loc = [], obj.localidad
        while loc and len(cadena) < 3:
            cadena.append(loc)
            loc = getattr(loc, campo) if campo else None
        return cadena

    def get_localidad_canton(self, obj):
        c = self._cadena(obj)
        return c[1].pk if len(c) > 1 else None

    def get_localidad_provincia(self, obj):
        c = self._cadena(obj)
        return c[2].pk if len(c) > 2 else None
    
# =========================================================
# LOGIN
# =========================================================
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get("username", "").strip()
        email = attrs.get("email", "").strip()
        password = attrs.get("password")

        # Se debe enviar username o email, pero no ambos.
        if bool(username) == bool(email):
            raise serializers.ValidationError("Ingresa tu username o tu email.")

        # Si se ingresa email, buscar el usuario correspondiente.
        if email:
            user_obj = User.objects.filter(email__iexact=email).first()
            if user_obj is None:
                raise serializers.ValidationError("Credenciales incorrectas.")
            username = user_obj.get_username()

        user = authenticate(
            request=self.context.get("request"),
            username=username,
            password=password,
        )
        if user is None:
            raise serializers.ValidationError("Credenciales incorrectas.")
        if not user.is_active:
            raise serializers.ValidationError("Esta cuenta está desactivada.")

        attrs["user"] = user
        return attrs


class OpcionSerializer(serializers.Serializer):
    """{id, name} para llenar los selects del frontend."""

    id = serializers.ReadOnlyField(source="pk")
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return str(obj)


# =========================================================
# EMPRESA
# =========================================================
class EmpresaSerializer(LocalidadJerarquiaMixin, serializers.ModelSerializer):
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
            "logotipo", "localidad", "localidad_nombre", "localidad_canton", "localidad_provincia", "estado",
        )
        read_only_fields = ("codigo",)

    def get_representante_nombre(self, obj):
        return str(obj.representante) if obj.representante else ""

    
    def validate_razon_social(self, value):
        value = validar_texto(limpiar(value), "La razón social", minimo=3, maximo=200)
        existe = Empresa.objects.filter(razon_social__iexact=value, estado="A")
        if self.instance:
            existe = existe.exclude(pk=self.instance.pk)
        if existe.exists():
            raise serializers.ValidationError("Ya existe una empresa con esa razón social.")
        return value

    def validate_telefono(self, value):
        return validar_telefono(value)

    def validate_fecha_constitucion(self, value):
        return validar_fecha_rango(value)

    def validate_calle_principal(self, value):
        return validar_texto(limpiar(value), "La calle principal", maximo=100)

    def validate_calle_secundaria(self, value):
        return validar_texto(limpiar(value), "La calle secundaria", maximo=100)

    def validate_logotipo(self, value):
        return validar_logotipo(value)

    def validate_estado(self, value):
        return validar_reactivacion(value, self.instance, Empresa, "razon_social", "una empresa")

    def get_localidad_nombre(self, obj):
        return obj.localidad.ruta_completa() if obj.localidad else ""

# =========================================================
# SUCURSAL
# =========================================================
from rest_framework.exceptions import ValidationError

class SucursalSerializer(LocalidadJerarquiaMixin, serializers.ModelSerializer):
    empresa_nombre = serializers.CharField(source="empresa.razon_social", read_only=True)
    localidad_nombre = serializers.SerializerMethodField() 

    class Meta:
        model = Sucursal
        fields = (
            "codigo", "empresa", "empresa_nombre", "nombre", "telefono",
            "calle_principal", "calle_secundaria", "localidad",
            "localidad_nombre",  "localidad_canton", "localidad_provincia", "estado",
        )
        read_only_fields = ("codigo",)

    def validate_empresa(self, value):
        if value.estado != "A":
            raise serializers.ValidationError("La empresa seleccionada está inactiva.")
        return value

    def validate_nombre(self, value):
        return validar_nombre(value, "El nombre", minimo=3, maximo=100)

    def validate_telefono(self, value):
        return validar_telefono(value)

    def validate_calle_principal(self, value):
        return validar_texto(value, "La calle principal", maximo=100)

    def validate_calle_secundaria(self, value):
        return validar_texto(value, "La calle secundaria", maximo=100)

    def validate(self, attrs):
        # El nombre no se repite entre sucursales activas de la misma empresa
        empresa = attrs.get("empresa") or getattr(self.instance, "empresa", None)
        nombre = attrs.get("nombre") or getattr(self.instance, "nombre", None)
        if empresa and nombre:
            validar_unico(
                nombre, self.instance, Sucursal, "nombre",
                "Ya existe una sucursal activa con ese nombre en esta empresa.",
                solo_activos=True, empresa=empresa,
            )
        return attrs

    def validate_estado(self, value):
        return validar_reactivacion(value, self.instance, Sucursal, "nombre", "una sucursal")

    def get_localidad_nombre(self, obj):
            return obj.localidad.ruta_completa() if obj.localidad else ""

    def validate_estado(self, value):
        if value == "A" and self.instance and self.instance.empresa.estado != "A":
            raise serializers.ValidationError("No se puede activar: la empresa está inactiva.")
        return validar_reactivacion(value, self.instance, Sucursal, "nombre", "una sucursal")
    
    

class ConfiguracionSerializer(serializers.ModelSerializer):
    codigo_auxiliar = serializers.CharField(
        max_length=30,
        error_messages={
            "required": "El código auxiliar es obligatorio.",
            "blank": "El código auxiliar es obligatorio.",
            "max_length": "El código auxiliar no puede superar los 30 caracteres.",
        },
    )

    class Meta:
        model = Configuracion
        fields = ("codigo", "codigo_auxiliar", "nombre", "descripcion", "estado")
        read_only_fields = ("codigo",)  # "estado" editable para poder reactivar

    def validate_codigo_auxiliar(self, value):
        value = validar_codigo(value, "El código auxiliar")
        return validar_unico(
            value, self.instance, Configuracion, "codigo_auxiliar",
            "Ya existe una configuración con ese código (puede estar inactiva).",
        )

    def validate_nombre(self, value):
        value = validar_nombre(value, "El nombre", minimo=3, maximo=100)
        return validar_unico(
            value, self.instance, Configuracion, "nombre",
            "Ya existe una configuración activa con ese nombre.",
            solo_activos=True,
        )
    
    def validate_descripcion(self, value):
        return validar_texto(value, "La descripción", maximo=250)

    def validate_estado(self, value):
        return validar_reactivacion(value, self.instance, Configuracion, "nombre", "una configuración")

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


    class Meta:
        model = EmpresaConfiguracion
        fields = (
            "id", "empresa", "empresa_nombre", "configuracion", "configuracion_nombre", "valor", "estado",
        )
        read_only_fields = ("id",)  # "estado" editable para poder reactivar
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

    def validate_estado(self, value):
        if value == "A" and self.instance:
            if self.instance.empresa.estado != "A":
                raise serializers.ValidationError("No se puede activar: la empresa está inactiva.")
            if self.instance.configuracion.estado != "A":
                raise serializers.ValidationError("No se puede activar: la configuración está inactiva.")
        return value