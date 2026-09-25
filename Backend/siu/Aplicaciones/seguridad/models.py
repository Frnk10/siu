from django.db import models
from django.conf import settings  # Importante para referenciar el User
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

class Localidad(BaseModel):
    codigo = models.AutoField(primary_key=True)
    codigo_padre = models.IntegerField(blank=True, null=True)
    codigo_auxiliar = models.CharField(max_length=25, blank=True, null=True)
    nombre = models.CharField(max_length=250, blank=False, null=False)
    nivel = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.nombre

class Persona(BaseModel):
    # Relación Uno a Uno con el User de Django
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,                    # Permite tener Clientes/Proveedores sin usuario
        blank=True,
        related_name='persona'        # Permite acceder desde user via: request.user.persona
    )
    codigo = models.AutoField(primary_key=True)
    pk_codigo_genero = models.ForeignKey(
        Genero,
        db_column='pk_codigo_genero',
        related_name='codigo_generos'
    )
    pk_codigo_estado_civil = models.ForeignKey(
        EstadoCivil,
        db_column='pk_codigo_estado_civil',
        related_name='codigo_estado_civil'
    )
    pk_codigo_grupo_sanguineo = models.ForeignKey(
        GrupoSanguineo,
        db_column='pk_codigo_grupo_sanguineo',
        related_name='codigo_grupo_sanguineo'
    )
    pk_codigo_instruccion = models.ForeignKey(
        Instruccion,
        db_column='pk_codigo_instruccion',
        related_name='codigo_instruccion'
    )
    pk_codigo_localidad = models.ForeignKey(
        Localidad,
        db_column='pk_codigo_localidad',
        related_name='codigo_localidad'
    )
    identificacion = models.CharField(max_length=13, blank=False, null=False)
    razon_social = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    fotografia = models.BinaryField(blank=True, null=True)
    mail1 = models.EmailField(max_length=50, blank=True, null=True)
    mail2 = models.EmailField(max_length=50, blank=True, null=True)
    telefono1 = models.CharField(max_length=9, blank=True, null=True)
    telefono2 = models.CharField(max_length=9, blank=True, null=True)
    celular1 = models.CharField(max_length=10, blank=True, null=True)
    celular2 = models.CharField(max_length=10, blank=True, null=True)
    calle_principal = models.CharField(max_length=50, blank=True, null=True)
    calle_secundaria = models.CharField(max_length=50, blank=True, null=True)
    numero_casa = models.CharField(max_length=50, blank=True, null=True)
    tipo = models.CharField(
        max_length=1, help_text="P=PERSONA NATURAL, S=SOCIEDAD", blank=False, null=False
    )
    ubicacion = models.CharField(max_length=50, blank=True, null=True)

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

class EmpresaConfiguracion(BaseModel):
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

class Usuario(models.Model):
    codigo = models.AutoField(primary_key=True)
    pk_codigo_sucursal = models.ForeignKey(
        Sucursal,
        db_column='pk_codigo_sucursal',
        related_name='codigo_sucursal'
    )
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=300)

    def __str__(self):
        return self.username

class Rol(BaseModel):
    codigo = models.AutoField(primary_key=True)
    codigo_auxiliar = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    permisos = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Menu(BaseModel):
    codigo = models.AutoField(primary_key=True)
    codigo_padre = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    nivel = models.IntegerField()
    orden = models.IntegerField()
    icono = models.CharField(max_length=50, blank=True, null=True)
    estilo_clase = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre

class RolMenu(models.Model):
    pk_codigo_rol = models.ForeignKey(
        Rol,
        db_column='pk_codigo_rol',
        related_name='codigo_rol'
    )
    pk_codigo_menu = models.ForeignKey(
        Menu,
        db_column='pk_codigo_menu',
        related_name='codigo_menu'
    )
    
class UsuarioRol(models.Model):
    pk_codigo_usuario = models.ForeignKey(
        Usuario,
        db_column='pk_codigo_usuario',
        related_name='codigo_usuarios'
    )
    pk_codigo_rol = models.ForeignKey(
        Rol,
        db_column='pk_codigo_rol',
        related_name='codigo_rol'
    )

class IngresoSistema():
    codigo = models.AutoField(primary_key=True)
    pk_codigo_usuario = models.ForeignKey(
        Usuario,
        db_column='pk_codigo_usuario',
        related_name='codigo_usuarios'
    )
    fecha = models.DateTimeField(auto_now_add=True, auto_now=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    ip = models.CharField(max_length=25, blank=True, null=True)
    validador = models.CharField(max_length=25, blank=True, null=True)
    estado = models.CharField(
        default="G", max_length=1, help_text="G=GENERADO, O=OCUPADO, C=CADUCADO"
    )

    def __str__(self):
        return self.codigo

