
from collections import defaultdict

from django.core.cache import cache

from .models import Menu

TIEMPO_CACHE = 60 * 30  # 30 minutos


def _construir_arbol(user):
    """Construye el árbol de menús según los permisos Django del usuario."""

    activos = {
        m["id"]: m
        for m in Menu.objects.filter(estado="A").values(
            "id",
            "padre_id",
            "nombre",
            "url",
            "icono",
            "orden",
            "permission_required_id",
            "permission_required__codename",
            "permission_required__content_type__app_label",
        )
    }

    if user.is_superuser:
        permitidos = set(activos)
    else:
        permisos_usuario = user.get_all_permissions()

        permitidos = {
            mid
            for mid, m in activos.items()
            if m["permission_required_id"] is not None
            and (
                f'{m["permission_required__content_type__app_label"]}.'
                f'{m["permission_required__codename"]}'
            ) in permisos_usuario
        }

    # Incluir ancestros de los menús permitidos
    incluidos = set()

    for mid in permitidos:
        cadena = []
        actual = mid
        valido = True

        while actual is not None and actual not in cadena:
            if actual not in activos:
                valido = False
                break

            cadena.append(actual)
            actual = activos[actual]["padre_id"]

        if valido:
            incluidos.update(cadena)

    # Agrupar por menú padre
    por_padre = defaultdict(list)

    for mid in sorted(
        incluidos,
        key=lambda i: (activos[i]["orden"], i)
    ):
        por_padre[activos[mid]["padre_id"]].append(mid)

    def nodo(mid):
        m = activos[mid]

        return {
            "id": mid,
            "nombre": m["nombre"],
            "url": m["url"],
            "icono": m["icono"],
            "hijos": [
                nodo(h)
                for h in por_padre.get(mid, [])
            ],
        }

    return [
        nodo(r)
        for r in por_padre.get(None, [])
    ]


def menu_para_usuario(user):
    if not user or not user.is_authenticated or not user.is_active:
        return []

    version = cache.get("menu:version", 1)

    if user.is_superuser:
        sufijo = "super"
    else:
        grupos = sorted(user.groups.values_list("id", flat=True))
        sufijo = "g" + "-".join(map(str, grupos))

    clave = f"menu:{version}:{sufijo}"

    arbol = cache.get(clave)

    if arbol is None:
        arbol = _construir_arbol(user)
        cache.set(clave, arbol, TIEMPO_CACHE)

    return arbol


def invalidar_cache_menu():
    """Invalida las versiones anteriores del árbol de menús."""

    try:
        cache.incr("menu:version")
    except ValueError:
        cache.set("menu:version", 2, None)
