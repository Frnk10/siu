from django.contrib import admin
from Aplicaciones.inventario.models import *

admin.site.register(Marca)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(UnidadMedida)