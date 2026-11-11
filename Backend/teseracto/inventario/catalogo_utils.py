import json

from django.db.models import Q
from rest_framework.exceptions import PermissionDenied

from usuarios.models import Empleado, Empresa


def parse_empresas(texto):
    """'[1, 2]' -> [1, 2]. Devuelve lista vacía si el texto no es válido."""
    try:
        datos = json.loads(texto or "[]")
        return sorted({int(x) for x in datos}) if isinstance(datos, list) else []
    except (ValueError, TypeError):
        return []


def obtener_empresas(registro):
    """Ids de las empresas asignadas a un registro de catálogo."""
    return parse_empresas(registro.id_texto_Empresa)


def empresas_del_usuario(user):
    """Empresas activas que representa el usuario (administrador)."""
    return list(
        Empresa.objects.filter(representante=user, estado="A").values_list("codigo", flat=True)
    )


def empresa_del_empleado(user):
    """Id de la empresa donde trabaja el usuario, o error si no aplica."""
    empresa_id = (
        Empleado.objects.filter(usuario=user, estado="A", empresa__estado="A")
        .values_list("empresa_id", flat=True)
        .first()
    )
    if empresa_id is None:
        raise PermissionDenied("No perteneces a ninguna empresa activa.")
    return empresa_id


def filtrar_por_empresas(qs, ids):
    """
    Registros asignados a al menos una de las empresas dadas.
    Depende del formato que guarda json.dumps(sorted(ids)): "[1, 2, 3]".
    """
    if not ids:
        return qs.none()
    q = Q()
    for i in ids:
        q |= (
            Q(id_texto_Empresa=f"[{i}]")
            | Q(id_texto_Empresa__startswith=f"[{i},")
            | Q(id_texto_Empresa__contains=f", {i},")
            | Q(id_texto_Empresa__endswith=f", {i}]")
        )
    return qs.filter(q)