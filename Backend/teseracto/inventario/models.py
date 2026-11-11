from django.db import models
from usuarios.models import BaseModel

class UnidadMedida(BaseModel):
    codigo = models.AutoField(primary_key=True)
    abreviatura = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    id_texto_Empresa = models.CharField(max_length=500, default="[]")

    def __str__(self):
        return self.nombre

class Categoria(BaseModel):
    codigo = models.AutoField(primary_key=True)
    codigo_padre = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=100)
    id_texto_Empresa = models.CharField(max_length=500, default="[]")

    def __str__(self):
        return self.nombre

class Marca(BaseModel):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    id_texto_Empresa = models.CharField(max_length=500, default="[]")

    def __str__(self):
        return self.nombre
