import re

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password as validar_clave
from django.db import transaction
from rest_framework import serializers

from validaciones.validaciones_serializers import (
    validar_codigo,
    validar_fecha_rango,
    validar_logotipo,
    validar_nombre,
    validar_reactivacion,
    validar_telefono,
    validar_texto,
    validar_unico,
)

from .acceso import empresas_permitidas
from .models import (
    Cliente,
    ClienteEmpresa,
    Configuracion,
    Empleado,
    Empresa,
    EmpresaConfiguracion,
    Localidad,
    Proveedor,
    ProveedorEmpresa,
    Sucursal,
)

User = get_user_model()
Usuario = User

CODIGO_RE = re.compile(r"^[A-Z0-9_]+$")


def limpiar(texto):
    """Quita espacios al inicio/fin y colapsa espacios repetidos."""
    return " ".join((texto or "").split())


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
            "logotipo", "localidad", "localidad_nombre", "localidad_canton",
            "localidad_provincia", "estado",
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
class SucursalSerializer(LocalidadJerarquiaMixin, serializers.ModelSerializer):
    empresa_nombre = serializers.CharField(source="empresa.razon_social", read_only=True)
    localidad_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Sucursal
        fields = (
            "codigo", "empresa", "empresa_nombre", "nombre", "telefono",
            "calle_principal", "calle_secundaria", "localidad",
            "localidad_nombre", "localidad_canton", "localidad_provincia", "estado",
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
        if value == "A" and self.instance and self.instance.empresa.estado != "A":
            raise serializers.ValidationError("No se puede activar: la empresa está inactiva.")
        return validar_reactivacion(value, self.instance, Sucursal, "nombre", "una sucursal")

    def get_localidad_nombre(self, obj):
        return obj.localidad.ruta_completa() if obj.localidad else ""


# =========================================================
# CONFIGURACIÓN
# =========================================================
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
            "id", "empresa", "empresa_nombre", "configuracion",
            "configuracion_nombre", "valor", "estado",
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


# =========================================================
# UTILIDADES PARA PERSONAS (usan validaciones/validaciones_serializers.py)
# =========================================================
def _nombre_mayus(value, etiqueta):
    return validar_nombre(limpiar(value), etiqueta, minimo=2, maximo=150).upper()


def _validar_identificacion(value):
    value = (value or "").strip()
    if not re.match(r"^\d{10}(\d{3})?$", value):
        raise serializers.ValidationError("La identificación debe tener 10 o 13 dígitos.")
    return value


class _TextosLimpiosMixin:
    """
    Validaciones de texto compartidas por cliente, proveedor y empleado.
    DRF solo ejecuta validate_<campo> si el campo existe en el serializer.
    """

    def validate_first_name(self, value):
        return _nombre_mayus(value, "El nombre")

    def validate_last_name(self, value):
        return _nombre_mayus(value, "El apellido")

    def validate_email(self, value):
        return value.strip().lower()

    def validate_telefono1(self, value):
        return validar_telefono(value) if value else value

    def validate_ubicacion(self, value):
        return validar_texto(limpiar(value), "La ubicación", maximo=200)

    def validate_banco(self, value):
        return validar_texto(limpiar(value), "El banco", maximo=100)

    def validate_tipo_cuenta(self, value):
        return validar_texto(limpiar(value), "El tipo de cuenta", maximo=20)

    def validate_numero_cuenta(self, value):
        value = (value or "").strip()
        if value and not value.isdigit():
            raise serializers.ValidationError("El número de cuenta solo puede tener dígitos.")
        return value

    def validate_contacto_emergencia(self, value):
        return validar_texto(limpiar(value), "El contacto de emergencia", maximo=150)

    def validate_descripcion_emergencia(self, value):
        return validar_texto(limpiar(value), "La descripción de emergencia", maximo=250)

    def validate_observaciones(self, value):
        # Texto libre: solo se limpia (permite puntuación)
        return (value or "").strip()


class EstadoActivoField(serializers.Field):
    """Muestra is_active como 'A' / 'I' para que el frontend use el mismo campo estado."""

    def to_representation(self, value):
        return "A" if value else "I"

    def to_internal_value(self, data):
        if data not in ("A", "I"):
            raise serializers.ValidationError("Estado no válido.")
        return data == "A"


_CAMPOS_PERSONA = (
    "identificacion", "first_name", "last_name", "email",
    "telefono1", "tipo", "ubicacion", "fk_codigo_localidad",
)


# =========================================================
# CLIENTE / PROVEEDOR (vínculo empresa-persona)
# =========================================================
class _VinculoPersonaSerializer(_TextosLimpiosMixin, serializers.ModelSerializer):
    """
    Busca a la persona por identificación: si existe la reutiliza, si no la crea.
    Luego crea (o reactiva) el vínculo con la empresa.
    Las subclases definen: Rol, rol, campos_rol y Meta.
    """

    Rol = None          # Cliente / Proveedor
    rol = None          # "cliente" / "proveedor" (nombre del FK en el vínculo)
    campos_persona = _CAMPOS_PERSONA
    campos_rol = ()

    empresa = serializers.PrimaryKeyRelatedField(
        queryset=Empresa.objects.filter(estado="A"),
        required=False,
        error_messages={"does_not_exist": "La empresa no existe o está inactiva."},
    )
    empresa_nombre = serializers.CharField(source="empresa.razon_social", read_only=True)

    # Datos de la persona (solo escritura; la lectura se arma en to_representation)
    identificacion = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False, allow_blank=True)
    telefono1 = serializers.CharField(write_only=True, required=False, allow_blank=True)
    tipo = serializers.ChoiceField(choices=Usuario.TIPO_CHOICES, write_only=True, required=False)
    ubicacion = serializers.CharField(write_only=True, required=False, allow_blank=True, max_length=200)
    fk_codigo_localidad = serializers.PrimaryKeyRelatedField(
        queryset=Localidad.objects.filter(estado="A"),
        write_only=True, required=False, allow_null=True,
    )

    # ---------- validaciones ----------
    def validate_empresa(self, value):
        if value.pk not in empresas_permitidas(self.context["request"].user):
            raise serializers.ValidationError("No tienes acceso a esa empresa.")
        return value

    def validate_identificacion(self, value):
        # Sin validar_unico: si la persona ya existe se reutiliza
        return _validar_identificacion(value)

    def validate_estado(self, value):
        if value == "A" and self.instance and self.instance.empresa.estado != "A":
            raise serializers.ValidationError("No se puede activar: la empresa está inactiva.")
        return value

    def validate(self, attrs):
        if not self.instance:
            faltan = [c for c in ("identificacion", "first_name", "last_name") if not attrs.get(c)]
            if faltan:
                raise serializers.ValidationError(
                    {c: "Este campo es obligatorio." for c in faltan}
                )
            if "empresa" not in attrs:
                ids = empresas_permitidas(self.context["request"].user)
                if len(ids) != 1:
                    raise serializers.ValidationError({"empresa": "Selecciona la empresa."})
                attrs["empresa"] = Empresa.objects.get(pk=next(iter(ids)))
        return attrs

    # ---------- lectura ----------
    def _compartida(self, vinculo):
        """True si la persona también está vinculada a otra empresa (como cliente o proveedor)."""
        pid = getattr(vinculo, f"{self.rol}_id")
        return (
            ClienteEmpresa.objects.filter(cliente_id=pid).exclude(empresa_id=vinculo.empresa_id).exists()
            or ProveedorEmpresa.objects.filter(proveedor_id=pid).exclude(empresa_id=vinculo.empresa_id).exists()
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        persona = getattr(instance, self.rol)
        for c in self.campos_persona:
            data[c] = getattr(persona, "fk_codigo_localidad_id" if c == "fk_codigo_localidad" else c)
        for c in self.campos_rol:
            data[c] = getattr(persona, c)
        data["nombre"] = persona.get_full_name()

        view = self.context.get("view")
        if view and getattr(view, "action", None) in ("retrieve", "update", "partial_update"):
            # Si es True, el frontend debe deshabilitar los datos personales
            data["datos_compartidos"] = self._compartida(instance)
        return data

    # ---------- escritura ----------
    def _crear_rol(self, datos, aud):
        ident = datos["identificacion"]
        usuario = Usuario.objects.filter(identificacion=ident).first()
        if usuario:
            # La persona ya existe (por ejemplo, es empleado o proveedor): se le agrega el rol.
            # Se copian los datos del padre para que el guardado no los sobrescriba con vacíos.
            persona = self.Rol(usuario_ptr_id=usuario.pk)
            persona.__dict__.update(usuario.__dict__)
            datos = {k: v for k, v in datos.items() if k in self.campos_rol}
        else:
            persona = self.Rol(username=ident, usuario_crea=aud.get("usuario_crea"))
            persona.set_unusable_password()  # no inicia sesión
        for k, v in datos.items():
            setattr(persona, k, v)
        persona.usuario_actualiza = aud.get("usuario_actualiza")
        persona.save()
        return persona

    @transaction.atomic
    def create(self, vd):
        aud = {k: vd.pop(k) for k in ("usuario_crea", "usuario_actualiza") if k in vd}
        empresa = vd.pop("empresa")
        datos = {k: vd.pop(k) for k in self.campos_persona + self.campos_rol if k in vd}

        persona = self.Rol.objects.filter(identificacion=datos["identificacion"]).first()
        if persona is None:
            persona = self._crear_rol(datos, aud)

        Vinculo = self.Meta.model
        filtro = {self.rol: persona, "empresa": empresa}
        vinculo = Vinculo.objects.filter(**filtro).first()

        if vinculo and vinculo.estado == "A":
            raise serializers.ValidationError(
                {"identificacion": "Ya está registrado en esta empresa."}
            )
        if vinculo:  # estaba inactivo: se reactiva con los datos nuevos
            for k, v in {**vd, "estado": "A", "usuario_actualiza": aud.get("usuario_actualiza")}.items():
                setattr(vinculo, k, v)
            vinculo.save()
            return vinculo
        return Vinculo.objects.create(**filtro, **vd, **aud)

    @transaction.atomic
    def update(self, instance, vd):
        vd.pop("empresa", None)          # el vínculo no cambia de empresa
        vd.pop("identificacion", None)   # la identificación no se edita
        datos = {k: vd.pop(k) for k in self.campos_persona + self.campos_rol if k in vd}

        # Los datos de la persona solo se editan si no la usa otra empresa
        if datos and not self._compartida(instance):
            persona = getattr(instance, self.rol)
            for k, v in datos.items():
                setattr(persona, k, v)
            persona.usuario_actualiza = vd.get("usuario_actualiza")
            persona.save()
        return super().update(instance, vd)


class ClienteSerializer(_VinculoPersonaSerializer):
    Rol = Cliente
    rol = "cliente"
    campos_rol = ("observaciones",)

    observaciones = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = ClienteEmpresa
        fields = (
            ("id", "empresa", "empresa_nombre", "limite_credito", "dias_credito", "estado")
            + _CAMPOS_PERSONA + ("observaciones",)
        )
        read_only_fields = ("id",)
        extra_kwargs = {"limite_credito": {"min_value": 0}}


class ProveedorSerializer(_VinculoPersonaSerializer):
    Rol = Proveedor
    rol = "proveedor"
    campos_rol = ("link_catalogo", "banco", "tipo_cuenta", "numero_cuenta", "observaciones")

    link_catalogo = serializers.URLField(write_only=True, required=False, allow_blank=True, allow_null=True)
    banco = serializers.CharField(write_only=True, required=False, allow_blank=True, max_length=100)
    tipo_cuenta = serializers.CharField(write_only=True, required=False, allow_blank=True, max_length=20)
    numero_cuenta = serializers.CharField(write_only=True, required=False, allow_blank=True, max_length=30)
    observaciones = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = ProveedorEmpresa
        fields = (
            ("id", "empresa", "empresa_nombre", "estado")
            + _CAMPOS_PERSONA
            + ("link_catalogo", "banco", "tipo_cuenta", "numero_cuenta", "observaciones")
        )
        read_only_fields = ("id",)


# =========================================================
# EMPLEADO (una sola empresa, inicia sesión)
# =========================================================
class EmpleadoSerializer(_TextosLimpiosMixin, serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, style={"input_type": "password"})
    estado = EstadoActivoField(source="is_active", required=False)
    empresa = serializers.PrimaryKeyRelatedField(
        queryset=Empresa.objects.filter(estado="A"),
        error_messages={"does_not_exist": "La empresa no existe o está inactiva."},
    )
    sucursal = serializers.PrimaryKeyRelatedField(
        queryset=Sucursal.objects.filter(estado="A"),
        required=False, allow_null=True,
        error_messages={"does_not_exist": "La sucursal no existe o está inactiva."},
    )
    empresa_nombre = serializers.CharField(source="empresa.razon_social", read_only=True)
    sucursal_nombre = serializers.CharField(source="sucursal.nombre", read_only=True, default="")

    class Meta:
        model = Empleado
        fields = (
            "id", "username", "password", "identificacion", "first_name", "last_name",
            "email", "telefono1", "tipo", "fecha_nacimiento", "ubicacion",
            "fk_codigo_localidad", "empresa", "empresa_nombre", "sucursal",
            "sucursal_nombre", "fecha_ingreso", "salario", "banco", "tipo_cuenta",
            "numero_cuenta", "contacto_emergencia", "descripcion_emergencia", "estado",
        )
        read_only_fields = ("id",)
        extra_kwargs = {
            "salario": {"min_value": 0},
            # La unicidad se valida abajo con mensajes propios
            "identificacion": {"validators": []},
            "username": {"required": False, "validators": []},
        }

    def validate_empresa(self, value):
        if value.pk not in empresas_permitidas(self.context["request"].user):
            raise serializers.ValidationError("No tienes acceso a esa empresa.")
        return value

    def validate_identificacion(self, value):
        value = _validar_identificacion(value)
        return validar_unico(
            value, self.instance, Usuario, "identificacion",
            "Ya existe una persona con esa identificación.",
        )

    def validate_username(self, value):
        value = (value or "").strip()
        return validar_unico(
            value, self.instance, Usuario, "username",
            "Ya existe un usuario con ese nombre de usuario.",
        )

    def validate_password(self, value):
        validar_clave(value)
        return value

    def validate(self, attrs):
        empresa = attrs.get("empresa", getattr(self.instance, "empresa", None))
        sucursal = attrs.get("sucursal", getattr(self.instance, "sucursal", None))
        if sucursal and empresa and sucursal.empresa_id != empresa.pk:
            raise serializers.ValidationError({"sucursal": "La sucursal no pertenece a esa empresa."})
        if not self.instance:
            if not attrs.get("password"):
                raise serializers.ValidationError({"password": "La contraseña es obligatoria."})
            # Si no envían usuario, se usa la identificación
            if not attrs.get("username"):
                attrs["username"] = attrs["identificacion"]
        return attrs

    def create(self, vd):
        password = vd.pop("password")
        empleado = Empleado(**vd)
        empleado.set_password(password)
        empleado.save()
        return empleado

    def update(self, instance, vd):
        password = vd.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, vd)