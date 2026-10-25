
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import Group, Permission

# =========================================================
# MODELO BASE
# =========================================================

class BaseModel(models.Model):
    ESTADO_CHOICES = [
        ("A", "Activo"),
        ("I", "Inactivo"),
    ]

    estado = models.CharField(
        max_length=1,
        choices=ESTADO_CHOICES,
        default="A",
        db_index=True,
    )

    usuario_crea = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
    )
    usuario_actualiza = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
    )

    fecha_crea = models.DateTimeField(auto_now_add=True)
    fecha_actualiza = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# =========================================================
# CATÁLOGOS
# =========================================================

class Genero(BaseModel):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class EstadoCivil(BaseModel):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class GrupoSanguineo(BaseModel):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nombre


class Instruccion(BaseModel):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Localidad(BaseModel):
    codigo = models.AutoField(primary_key=True)

    localidad_padre = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="localidades_hijas",
    )

    codigo_auxiliar = models.CharField(
        max_length=25,
        blank=True,
        null=True,
    )
    nombre = models.CharField(max_length=250)
    nivel = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["nivel", "nombre"]

    def __str__(self):
        return self.nombre

# =========================================================
# EMPRESAS Y SUCURSALES
# =========================================================

class Empresa(BaseModel):
    codigo = models.AutoField(primary_key=True)
    razon_social = models.CharField(max_length=200)
    representante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="empresas_representadas",
        null=True,
        blank=True,
    )
    fecha_constitucion = models.DateField(
        null=True,
        blank=True,
    )

    calle_principal = models.CharField(max_length=100, blank=True)
    calle_secundaria = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=15, blank=True)

    obligado_contabilidad = models.BooleanField(default=False)
    facturacion_electronica = models.BooleanField(default=False)

    logotipo = models.ImageField(
        upload_to="empresas/logotipos/",
        null=True,
        blank=True,
    )

    localidad = models.ForeignKey(
        Localidad,
        on_delete=models.PROTECT,
        related_name="empresas",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.razon_social


class Sucursal(BaseModel):
    codigo = models.AutoField(primary_key=True)

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.PROTECT,
        related_name="sucursales",
    )

    localidad = models.ForeignKey(
        Localidad,
        on_delete=models.PROTECT,
        related_name="sucursales",
        null=True,
        blank=True,
    )

    nombre = models.CharField(max_length=200)

    calle_principal = models.CharField(max_length=100, blank=True)
    calle_secundaria = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.empresa.razon_social} - {self.nombre}"


# =========================================================
# USUARIO ÚNICO DEL SISTEMA
# =========================================================

class Usuario(AbstractUser):
    identificacion = models.CharField(
        max_length=13,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\d{10}(\d{3})?$",
                message="La identificación debe tener 10 o 13 dígitos.",
            )
        ],
    )
    fk_codigo_genero = models.ForeignKey(
        Genero,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="usuarios",
    )
    fk_codigo_estado_civil = models.ForeignKey(
        EstadoCivil,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="usuarios",
    )
    fk_codigo_grupo_sanguineo = models.ForeignKey(
        GrupoSanguineo,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="usuarios",
    )
    fk_codigo_instruccion = models.ForeignKey(
        Instruccion,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="usuarios",
    )
    fk_codigo_localidad = models.ForeignKey(
        Localidad,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="usuarios",
    )

    fecha_nacimiento = models.DateField(null=True, blank=True)

    image = models.ImageField(
        upload_to="perfil/",
        null=True,
        blank=True,
    )

    telefono1 = models.CharField(max_length=15, blank=True)

    TIPO_CHOICES = [
        ("P", "Persona natural"),
        ("S", "Sociedad"),
    ]
    tipo = models.CharField(
        max_length=1,
        choices=TIPO_CHOICES,
        default="P",
    )
    ubicacion = models.CharField(max_length=200, blank=True)

    usuario_crea = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
    )
    usuario_actualiza = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
    )
    
    fecha_crea = models.DateTimeField(auto_now_add=True)
    fecha_actualiza = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.get_full_name() or self.username
    
class Cliente(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="clientes",
    )
    empresa = models.ForeignKey(
        Empresa, on_delete=models.PROTECT, related_name="clientes"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "empresa"], name="uniq_cliente_usuario_empresa"
            )
        ]


class Proveedor(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="proveedores",
    )
    empresa = models.ForeignKey(
        Empresa, on_delete=models.PROTECT, related_name="proveedores"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "empresa"], name="uniq_proveedor_usuario_empresa"
            )
        ]


class Empleado(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="empleados",
    )
    empresa = models.ForeignKey(
        Empresa, on_delete=models.PROTECT, related_name="empleados"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "empresa"], name="uniq_empleado_usuario_empresa"
            )
        ]



class Menu(BaseModel):
    id = models.AutoField(primary_key=True)
    padre = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='hijos'
    )
    permission_required = models.ForeignKey(
        Permission,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Permiso requerido",
        help_text="Permiso específico necesario para acceder a este menú"
    )
    nombre = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=200, blank=True)
    icono = models.CharField(max_length=50, blank=True)
    orden = models.PositiveIntegerField(default=0, help_text="Orden de visualización")
 
    class Meta:
        db_table = 'menu'
        verbose_name = 'Menú'
        verbose_name_plural = 'Menús'
        ordering = ['orden', 'id']
 
    def __str__(self):
        return self.nombre or f"Menú {self.id}"
 
    def get_hijos_visibles(self, user):
        # Usuario no autenticado o inactivo: no ve nada
        if not user or not user.is_authenticated or not user.is_active:
            return self.hijos.none()
 
        base = self.hijos.filter(estado="A")
 
        # Superusuario: ve todos los hijos activos
        if user.is_superuser:
            return base
 
        # Resto: solo los hijos asignados a sus grupos
        grupos_ids = user.groups.values_list("id", flat=True)
        return base.filter(accesos__grupo_id__in=grupos_ids).distinct()
 
    def es_accesible_para(self, user):
        if not user or not user.is_authenticated or not user.is_active:
            return False
 
        if user.is_superuser:
            return True
 
        return AccesoMenu.objects.filter(
            menu=self,
            grupo__in=user.groups.all(),
        ).exists()


class AccesoMenu(models.Model):
    id = models.AutoField(primary_key=True)
    menu = models.ForeignKey(
        Menu, 
        on_delete=models.CASCADE,
        verbose_name='Menú',
        related_name='accesos'
    )
    grupo = models.ForeignKey(
        Group, 
        on_delete=models.CASCADE,
        verbose_name='Grupo',
        related_name='accesos_menu'
    )

    class Meta:
        db_table = 'acceso_menu'
        verbose_name = 'Acceso a Menú'
        verbose_name_plural = 'Accesos a Menús'
        unique_together = [['menu', 'grupo']]

    def __str__(self):
        return f"{self.menu.nombre} - {self.grupo.name}"


# =========================================================
# CONFIGURACIÓN DE EMPRESA
# =========================================================

class Configuracion(BaseModel):
    codigo = models.AutoField(primary_key=True)
    codigo_auxiliar = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=250, blank=True)
    grupo = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class EmpresaConfiguracion(BaseModel):
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="configuraciones",
    )
    configuracion = models.ForeignKey(
        Configuracion,
        on_delete=models.CASCADE,
        related_name="valores_empresa",
    )
    valor = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["empresa", "configuracion"],
                name="uq_empresa_configuracion",
            ),
        ]

    def __str__(self):
        return f"{self.empresa} - {self.configuracion}"


from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django_rest_passwordreset.signals import reset_password_token_created

MAX_SOLICITUDES = 3


@receiver(reset_password_token_created)
def password_reset_token_created(reset_password_token, *args, **kwargs):

    # URL del frontend React
    token = reset_password_token.key
    full_link = f"{settings.FRONTEND_URL.rstrip('/')}/password-reset/{token}"

    # Minutos de validez (la librería lo configura en horas)
    horas = getattr(settings, "DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME", 24)
    minutos_validez = max(1, round(horas * 60))

    # Datos para la plantilla HTML
    context = {
        "full_link": full_link,
        "email_address": reset_password_token.user.email,
        "minutos_validez": minutos_validez,
        "max_solicitudes": MAX_SOLICITUDES,
    }

    # Renderizar el HTML
    html_message = render_to_string(
        "pass.html",
        context=context
    )

    # Crear versión de texto plano
    plain_message = strip_tags(html_message)

    # Crear y enviar el correo
    msg = EmailMultiAlternatives(
        subject="Recuperación de contraseña | Teseracto Engine",
        body=plain_message,
        from_email=None,
        to=[reset_password_token.user.email],
    )

    msg.attach_alternative(html_message, "text/html")
    msg.send(fail_silently=False)