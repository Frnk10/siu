from django.contrib import admin
from Aplicaciones.venta.models import *

admin.site.register(Cliente)
admin.site.register(Comprobante)
admin.site.register(ComprobanteDetalle)
admin.site.register(Cobro)
admin.site.register(CobroDetalle)
