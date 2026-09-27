from django.contrib import admin
from Aplicaciones.inventario.models import *

class MarcaAdmin(admin.ModelAdmin):
    list_display = ('codigo','nombre',)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('codigo','nombre',)

class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ('codigo','nombre',)
    
admin.site.register(Marca,MarcaAdmin)
admin.site.register(Categoria,CategoriaAdmin)
admin.site.register(UnidadMedida,UnidadMedidaAdmin)
admin.site.register(Producto)