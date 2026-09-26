from django.contrib import admin
from Aplicaciones.compra.models import *


admin.site.register(Proveedor)
admin.site.register(Compra)
admin.site.register(CompraDetalle)
admin.site.register(Pago)
admin.site.register(PagoDetalle)
