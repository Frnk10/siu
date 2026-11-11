
import os
import re
from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

# ---------- Constantes ----------
TELEFONO_RE = re.compile(r"^\d{10}$")
TEXTO_RE = re.compile(r"^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ ]+$")
NOMBRE_ARCHIVO_RE = re.compile(r"^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ _-]+$")

FECHA_MAX_DIAS_FUTURO = 3

LOGO_MAX_BYTES = 2 * 1024 * 1024
LOGO_TIPOS = {"image/png", "image/jpeg", "image/webp"}
LOGO_EXTENSIONES = {".png", ".jpg", ".jpeg", ".webp"}
LOGO_NOMBRE_MAX = 100


# ---------- Validadores reutilizables ----------
def validar_texto(value, nombre, minimo=0, maximo=None):
    """Texto sin caracteres especiales (solo letras, números y espacios)."""
    value = (value or "").strip()
    if not value:
        return value
    if len(value) < minimo:
        raise serializers.ValidationError(f"{nombre} debe tener al menos {minimo} caracteres.")
    if maximo and len(value) > maximo:
        raise serializers.ValidationError(f"{nombre} no puede superar los {maximo} caracteres.")
    if not TEXTO_RE.match(value):
        raise serializers.ValidationError(
            f"{nombre} no puede contener caracteres especiales. Use solo letras, números y espacios."
        )
    return value


def validar_telefono(value):
    value = (value or "").replace(" ", "").replace("-", "")
    if value and not TELEFONO_RE.match(value):
        raise serializers.ValidationError("El teléfono debe tener exactamente 10 dígitos numéricos.")
    return value


FECHA_RANGO_DIAS = 3  # días antes y después de hoy


def validar_fecha_rango(value, dias=FECHA_RANGO_DIAS):
    """Solo permite fechas entre (hoy - dias) y (hoy + dias)."""
    if value:
        hoy = timezone.localdate()
        minimo = hoy - timedelta(days=dias)
        maximo = hoy + timedelta(days=dias)
        if value < minimo or value > maximo:
            raise serializers.ValidationError(
                f"La fecha debe estar entre {minimo.strftime('%d-%m-%Y')} "
                f"y {maximo.strftime('%d-%m-%Y')} (3 días antes o después de hoy)."
            )
    return value

def validar_logotipo(value):
    if not value:
        return value

    nombre, extension = os.path.splitext(value.name)

    if extension.lower() not in LOGO_EXTENSIONES:
        raise serializers.ValidationError("El logotipo debe ser PNG, JPG o WEBP.")
    if not NOMBRE_ARCHIVO_RE.match(nombre):
        raise serializers.ValidationError(
            "El nombre del archivo no puede contener caracteres especiales. "
            "Use solo letras, números, espacios, guiones (-) o guion bajo (_)."
        )
    if len(value.name) > LOGO_NOMBRE_MAX:
        raise serializers.ValidationError(
            f"El nombre del archivo es demasiado largo (máx. {LOGO_NOMBRE_MAX} caracteres)."
        )
    if value.size > LOGO_MAX_BYTES:
        raise serializers.ValidationError("El logotipo no puede superar los 2 MB.")

    tipo = getattr(value, "content_type", None)
    if tipo and tipo not in LOGO_TIPOS:
        raise serializers.ValidationError("El logotipo debe ser PNG, JPG o WEBP.")
    return value

def validar_reactivacion(value, instance, modelo, campo, nombre):
    """
    Impide pasar a Activo ("A") si ya existe otro registro activo
    con el mismo valor en `campo`.

    value:    nuevo estado ("A" / "I")
    instance: registro que se está editando (None al crear)
    modelo:   clase del modelo (Empresa, Sucursal, ...)
    campo:    nombre del campo que debe ser único entre activos (ej. "razon_social")
    nombre:   texto para el mensaje (ej. "una empresa")
    """
    if value == "A" and instance:
        existe = modelo.objects.filter(
            **{f"{campo}__iexact": getattr(instance, campo)},
            estado="A",
        ).exclude(pk=instance.pk)
        if existe.exists():
            raise serializers.ValidationError(
                f"No se puede activar: ya existe {nombre} activa con ese mismo valor."
            )
    return value

CODIGO_RE = re.compile(r"^[A-Z0-9_]+$")


def validar_nombre(value, etiqueta="El nombre", minimo=3, maximo=100):
    """Nombre obligatorio, sin caracteres especiales."""
    value = validar_texto(value, etiqueta, minimo=minimo, maximo=maximo)
    if not value:
        raise serializers.ValidationError(f"{etiqueta} es obligatorio.")
    return value


def validar_codigo(value, etiqueta="El código", minimo=2, maximo=30):
    """Código obligatorio: mayúsculas, números y guion bajo, sin espacios."""
    value = (value or "").strip().upper()
    if not value:
        raise serializers.ValidationError(f"{etiqueta} es obligatorio.")
    if len(value) < minimo:
        raise serializers.ValidationError(f"{etiqueta} debe tener al menos {minimo} caracteres.")
    if len(value) > maximo:
        raise serializers.ValidationError(f"{etiqueta} no puede superar los {maximo} caracteres.")
    if not CODIGO_RE.match(value):
        raise serializers.ValidationError(
            f"{etiqueta} solo puede tener letras mayúsculas, números y guion bajo (sin espacios)."
        )
    return value


def validar_unico(value, instance, modelo, campo, mensaje, solo_activos=False, **filtros):
    """
    Impide repetir `value` en `campo`.

    instance:     registro que se edita (None al crear), se excluye de la búsqueda
    solo_activos: True = solo compara contra registros con estado "A"
    mensaje:      texto del error
    filtros:      condiciones extra, p. ej. empresa=empresa para unicidad por empresa
    """
    existe = modelo.objects.filter(**{f"{campo}__iexact": value}, **filtros)
    if solo_activos:
        existe = existe.filter(estado="A")
    if instance:
        existe = existe.exclude(pk=instance.pk)
    if existe.exists():
        raise serializers.ValidationError(mensaje)
    return value