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

class Instruccion(BaseModel):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Persona(BaseModel):
    codigo = models.AutoField(primary_key=True)
    fk_codigo_genero = models.ForeignKey(Genero)
    fk_codigo_estado_civil = models.ForeignKey(EstadoCivil)
    fk_codigo_grupo_sanguineo = models.ForeignKey(GrupoSanguineo)
    fk_codigo_instruccion = models.ForeignKey(Instruccion)
    identidficacion = models.CharField(max_length=10)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    razon_social = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    fotografia = models.ImageField(upload_to='fotos/', blank=True, null=True)
    mail1 = models.CharField(max_length=50)
    mail2 = models.CharField(max_length=50)
    telefono1 = models.CharField(max_length=15)
    telefono2 = models.CharField(max_length=15)
    celular1 = models.CharField(max_length=15)
    celular2 = models.CharField(max_length=15)
    calle_principal = models.CharField(max_length=50)
    calle_secundaria = models.CharField(max_length=50)
    numero_casa = models.CharField(max_length=10)
    tipo = models.CharField(max_length=10)
    ubicacion = models.CharField(max_length=100)
    estado = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre
