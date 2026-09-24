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

class Empresa(BaseModel):
    codigo = models.AutoField(primary_key=True)
    razon_social = models.CharField(max_length=200)
    representante = models.CharField(max_length=200)
    ruc = models.CharField(max_length=13)
    fecha_constitucion = models.DateField(auto_now_add=True)
    calle_principal = models.CharField(max_length=100)
    calle_secundaria = models.CharField(max_length=100)
    numero_casa = models.CharField(max_length=50)
    telefono = models.CharField(max_length=9)
    obligado_contabilidad = models.CharField(default="N", max_length=1, help_text="S=SI, N=NO")
    facturacion_electronica = models.CharField(default="N", max_length=1, help_text="S=SI, N=NO")
    logotipo = models.BinaryField(null=True,blank=True)
    certificado = models.BinaryField(null=True,blank=True)
    id_localidad = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.razon_social

class Configuracion(BaseModel):
    codigo = models.AutoField(primary_key=True)
    codigo_auxiliar = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    grupo = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.nombre

class EmpreasConfiguracion(BaseModel):
    pk_codigo_empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        db_column='pk_codigo_empresa',
        related_name='empresa_configuraciones'
    )
    # FK hacia configuracion (columna: pk_codigo_configuracion)
    pk_codigo_configuracion = models.ForeignKey(
        Configuracion,
        on_delete=models.CASCADE,
        db_column='pk_codigo_configuracion',
        related_name='configuracion_empresas'
    )
    valor = models.CharField(max_length=50)

    class Meta:
        db_table = 'empresa_configuracion'
        # Replica la PK compuesta: no puede repetirse la misma pareja
        unique_together = (('pk_codigo_empresa', 'pk_codigo_configuracion'),)
    
    def __str__(self):
        return self.nombre

class Sucursal(BaseModel):
    codigo = models.AutoField(primary_key=True)
    fk_codigo_empresa = models.ForeignKey(Empresa)
    id_localidad = models.IntegerField(blank=False, null=False)
    nombre = models.CharField(max_length=200)
    gerente = models.CharField(max_length=200)
    secuencial_sucursal = models.CharField(max_length=200)
    calle_principal = models.CharField(max_length=100)
    calle_secundaria = models.CharField(max_length=100)
    numero_casa = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Usuario(Persona):
    fk_codigo_sucursal = models.ForeignKey(Sucursal)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=300)

    def __str__(self):
        return self.username

class IngresoSistema():
    codigo = models.AutoField(primary_key=True)
    fk_codigo_usuario = models.ForeignKey(Usuario)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=200)
    ip = models.CharField(max_length=25)
    validador = models.CharField(max_length=25)
    estado = models.CharField(default="G", max_length=1, help_text="G=GENERADO, O=OCUPADO, C=CADUCADO")

    def __str__(self):
        return self.codigo