from django.db import models
from Backend.siu.Aplicaciones.basemodel.models import BaseModel

class UnidadMedida(BaseModel):
    codigo = models.AutoField(primary_key=True)
    abreviatura = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    id_texto_Empresa = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Categoria(BaseModel):
    codigo = models.AutoField(primary_key=True)
    codigo_padre = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=100)
    id_texto_Empresa = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Marca(BaseModel):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    id_texto_Empresa = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class Producto(BaseModel):    
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    cantidad = models.IntegerField(default=0)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ingreso = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)


    def __str__(self):
        return self.nombre