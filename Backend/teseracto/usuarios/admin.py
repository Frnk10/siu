from django.contrib import admin
from usuarios.models import *

admin.site.register(Usuario)
admin.site.register(Menu)
admin.site.register(AccesoMenu)
admin.site.register(Empresa)
admin.site.register(Configuracion)
admin.site.register(EmpresaConfiguracion)
admin.site.register(Sucursal)