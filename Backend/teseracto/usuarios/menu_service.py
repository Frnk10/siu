from collections import defaultdict

from django.core.cache import cache

from .models import AccesoMenu, Menu

TIEMPO_CACHE = 60 * 30  # 30 minutos


def _construir_arbol(user):
    """Arma el árbol de menús del usuario con 2 consultas."""
    activos = {
        m["id"]: m
        for m in Menu.objects.filter(estado="A").values("id", "padre_id", "nombre", "url", "icono", "orden")
    }

    if user.is_superuser:
        permitidos = set(activos)
    else:
        permitidos = set(
            AccesoMenu.objects.filter(grupo__in=user.groups.all()).values_list("menu_id", flat=True)
        ) & set(activos)

    # Incluye los ancestros para que un hijo permitido nunca quede huérfano
    incluidos = set()
    for mid in permitidos:
        cadena, actual, valido = [], mid, True
        while actual is not None and actual not in cadena:
            if actual not in activos:  # ancestro inactivo: se descarta la rama
                valido = False
                break
            cadena.append(actual)
            actual = activos[actual]["padre_id"]
        if valido:
            incluidos.update(cadena)

    por_padre = defaultdict(list)
    for mid in sorted(incluidos, key=lambda i: (activos[i]["orden"], i)):
        por_padre[activos[mid]["padre_id"]].append(mid)

    def nodo(mid):
        m = activos[mid]
        return {
            "id": mid,
            "nombre": m["nombre"],
            "url": m["url"],
            "icono": m["icono"],
            "hijos": [nodo(h) for h in por_padre.get(mid, [])],
        }

    return [nodo(r) for r in por_padre.get(None, [])]


def menu_para_usuario(user):
    if not user or not user.is_authenticated or not user.is_active:
        return []

    version = cache.get("menu:version", 1)
    if user.is_superuser:
        sufijo = "super"
    else:
        grupos = sorted(user.groups.values_list("id", flat=True))
        sufijo = "g" + "-".join(map(str, grupos))  # el menú depende de los grupos, no del usuario

    clave = f"menu:{version}:{sufijo}"
    arbol = cache.get(clave)
    if arbol is None:
        arbol = _construir_arbol(user)
        cache.set(clave, arbol, TIEMPO_CACHE)
    return arbol


def invalidar_cache_menu():
    """Sube la versión: todas las claves anteriores dejan de usarse."""
    try:
        cache.incr("menu:version")
    except ValueError:
        cache.set("menu:version", 2, None)
