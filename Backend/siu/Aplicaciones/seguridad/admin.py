from django.contrib import admin
from Aplicaciones.seguridad.models import *

admin.site.register(Genero)
admin.site.register(EstadoCivil)
admin.site.register(GrupoSanguineo)
admin.site.register(Instruccion)
admin.site.register(Localidad)
admin.site.register(Persona)
admin.site.register(Empresa)
admin.site.register(Configuracion)
admin.site.register(EmpresaConfiguracion)
admin.site.register(Sucursal)
admin.site.register(Usuario)
admin.site.register(Rol)
admin.site.register(Menu)
admin.site.register(RolMenu)
admin.site.register(UsuarioRol)
admin.site.register(IngresoSistema)