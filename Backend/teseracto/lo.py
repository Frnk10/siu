import os
import re
import sys
from pathlib import Path

# ---------- Arranque de Django (lee el nombre de settings desde manage.py) ----------
BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
settings_mod = re.search(
    r"DJANGO_SETTINGS_MODULE['\"],\s*['\"]([^'\"]+)['\"]",
    (BASE / "manage.py").read_text(encoding="utf-8"),
).group(1)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_mod)

import django
django.setup()

from django.db import transaction
from openpyxl import load_workbook

from usuarios.models import Localidad  # cambia "usuarios" si tu app se llama distinto

# ---------- Configuración ----------
# Ruta del Excel: pásala como argumento o escríbela aquí
RUTA = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\Jhonnatan\Downloads\localidades_ecuador.xlsx"
HOJA = "Localidades"
COLUMNAS = ["codigo", "nombre", "nivel", "tipo", "codigo_padre"]


def texto(valor, ancho=None):
    """Convierte la celda a texto; si Excel guardó un número, recupera los ceros."""
    if valor is None:
        return ""
    if isinstance(valor, float) and valor.is_integer():
        valor = int(valor)
    t = str(valor).strip()
    return t.zfill(ancho) if ancho and t.isdigit() else t


@transaction.atomic
def cargar():
    wb = load_workbook(RUTA, read_only=True, data_only=True)
    filas = list(wb[HOJA].iter_rows(values_only=True))

    encabezado = [str(c).strip().lower() if c else "" for c in filas[0]]
    if encabezado[: len(COLUMNAS)] != COLUMNAS:
        raise SystemExit(f"Encabezados esperados {COLUMNAS}, encontrados {encabezado}")

    datos = []
    for n, fila in enumerate(filas[1:], start=2):
        if not any(fila):
            continue
        nivel = int(fila[2])
        codigo = texto(fila[0], nivel * 2)
        nombre = " ".join(texto(fila[1]).split())
        padre = texto(fila[4], (nivel - 1) * 2) if nivel > 1 else ""
        if nivel not in (1, 2, 3) or len(codigo) != nivel * 2 or not nombre:
            raise SystemExit(f"Fila {n} inválida: {fila}")
        datos.append((nivel, codigo, nombre, padre))

    datos.sort(key=lambda d: (d[0], d[1]))  # provincias, luego cantones, luego parroquias

    creadas = actualizadas = 0
    cache = {}
    for nivel, codigo, nombre, cod_padre in datos:
        padre = None
        if nivel > 1:
            padre = cache.get((nivel - 1, cod_padre))
            if padre is None:
                raise SystemExit(f"{codigo} ({nombre}): no existe su padre {cod_padre}")

        obj, creada = Localidad.objects.update_or_create(
            codigo_auxiliar=codigo,
            nivel=nivel,
            defaults={"nombre": nombre, "localidad_padre": padre, "estado": "A"},
        )
        cache[(nivel, codigo)] = obj
        creadas += creada
        actualizadas += not creada

    print(f"Listo: {creadas} creadas, {actualizadas} actualizadas, {len(datos)} filas leídas.")


if __name__ == "__main__":
    cargar()
    print("Total por nivel:", {n: Localidad.objects.filter(nivel=n).count() for n in (1, 2, 3)})