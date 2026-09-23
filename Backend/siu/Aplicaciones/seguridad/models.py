from django.db import models
from Backend.siu.Aplicaciones.basemodel.models import BaseModel

class Genero(BaseModel):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class EstadoCivil(BaseModel):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class GrupoSanguineo(BaseModel):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
