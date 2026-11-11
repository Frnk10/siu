
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from knox.models import AuthToken

from .serializers import LoginSerializer

User = get_user_model()


class LoginViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request}
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # El LoginSerializer ya validó las credenciales.
        user = serializer.validated_data["user"]

        # Crear token de autenticación con Knox.
        _, token = AuthToken.objects.create(user)

        # Serializar únicamente los datos públicos del usuario.
        user_data = LoginSerializer(user).data

        return Response(
            {
                "user": user_data,
                "token": token
            },
            status=status.HTTP_200_OK
        )




from rest_framework import mixins
from rest_framework.exceptions import ValidationError

from .models import Configuracion, Empresa, EmpresaConfiguracion, Sucursal, Localidad
from .serializers import (
    ConfiguracionSerializer,
    EmpresaConfiguracionSerializer,
    EmpresaSerializer,
    OpcionSerializer,
    SucursalSerializer,
)


from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.exceptions import ValidationError


class BaseCrudViewSet(viewsets.ModelViewSet):
    """CRUD con borrado lógico (estado 'I') y auditoría (usuario/fecha)."""

    permission_classes = [permissions.IsAuthenticated]
    borrado_logico = True  # False = elimina el registro de verdad


    def perform_create(self, serializer):
        # usuario_crea y usuario_actualiza se llenan con el usuario actual.
        # fecha_crea / fecha_actualiza las pone Django (auto_now_add / auto_now).
        serializer.save(
            usuario_crea=self.request.user,
            usuario_actualiza=self.request.user,
        )

    def perform_update(self, serializer):
        # Si por PATCH/PUT intentan pasar a Inactivo, se aplica la misma validación
        if serializer.validated_data.get("estado") == "I":
            self.validar_baja(serializer.instance)
        serializer.save(usuario_actualiza=self.request.user)

    def perform_destroy(self, instance):
        self.validar_baja(instance)
        if self.borrado_logico:
            instance.estado = "I"
            instance.usuario_actualiza = self.request.user
            # incluir fecha_actualiza: con update_fields, auto_now solo se
            # aplica si el campo está en la lista
            instance.save(update_fields=["estado", "usuario_actualiza", "fecha_actualiza"])
        else:
            instance.delete()


class EmpresaViewSet(BaseCrudViewSet):
    queryset = (
        Empresa.objects.select_related("representante", "localidad")
        .order_by("estado", "razon_social")
    )
    serializer_class = EmpresaSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            representante=self.request.user
        )

    def validar_baja(self, instance):
        if instance.sucursales.filter(estado="A").exists():
            raise ValidationError({
                "detail": "No se puede eliminar: la empresa tiene sucursales activas."
            })
        
class SucursalViewSet(BaseCrudViewSet):
    queryset = (
        Sucursal.objects.select_related("empresa", "localidad")
        .order_by("estado", "nombre")
    )
    serializer_class = SucursalSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        # Empresas representadas por el usuario autenticado
        empresas_usuario = Empresa.objects.filter(
            representante=self.request.user
        ).values_list("codigo", flat=True)

        # Limitar las sucursales a sus empresas
        qs = qs.filter(empresa__in=empresas_usuario)

        # Filtro opcional por empresa seleccionada
        empresa_id = self.request.query_params.get("empresa")

        if empresa_id:
            qs = qs.filter(empresa_id=empresa_id)

        return qs

    def validar_baja(self, instance):
        if instance.empresa.estado != "A":
            raise ValidationError({
                "detail": "No se puede desactivar: la empresa de esta sucursal está inactiva."
            })
        
class ConfiguracionViewSet(BaseCrudViewSet):
    queryset = Configuracion.objects.all().order_by("estado", "nombre")
    serializer_class = ConfiguracionSerializer

    def validar_baja(self, instance):
        if instance.valores_empresa.filter(estado="A").exists():
            raise ValidationError(
                {"detail": "No se puede desactivar: hay empresas que usan esta configuración."}
            )

class EmpresaConfiguracionViewSet(BaseCrudViewSet):
    queryset = (
        EmpresaConfiguracion.objects.select_related("empresa", "configuracion")
        .order_by("estado", "configuracion__nombre")
    )
    serializer_class = EmpresaConfiguracionSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        # Obtener todas las empresas representadas por el usuario
        empresas_usuario = Empresa.objects.filter(
            representante=self.request.user
        ).values_list("codigo", flat=True)

        # Restringir las configuraciones a sus empresas
        qs = qs.filter(empresa__in=empresas_usuario)

        # Filtro opcional por empresa
        empresa_id = self.request.query_params.get("empresa")

        if empresa_id:
            qs = qs.filter(empresa_id=empresa_id)

        return qs

    def validar_baja(self, instance):
        if instance.empresa.estado != "A":
            raise ValidationError({
                "detail": "No se puede desactivar: la empresa está inactiva."
            })


# ---------- Opciones para los selects ----------
class UsuarioOpcionesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = get_user_model().objects.filter(is_active=True).order_by("first_name", "last_name", "username")
    serializer_class = OpcionSerializer


class LocalidadOpcionesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    /opciones/localidades/?nivel=1                 -> provincias
    /opciones/localidades/?nivel=2&padre=<id>      -> cantones de esa provincia
    /opciones/localidades/?nivel=3&padre=<id>      -> parroquias de ese cantón
    Sin parámetros: parroquias con ruta completa (como antes, por si otro formulario lo usa).
    """
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_serializer_class(self):
        if "nivel" in self.request.query_params:
            return OpcionSerializer
        return OpcionSerializer

    def get_queryset(self):
        params = self.request.query_params
        qs = Localidad.objects.filter(estado="A")

        if "nivel" not in params:
            return (
                qs.filter(nivel=3)
                .select_related("localidad_padre__localidad_padre")
                .order_by(
                    "localidad_padre__localidad_padre__nombre",
                    "localidad_padre__nombre",
                    "nombre",
                )
            )

        if params["nivel"] in ("1", "2", "3"):
            qs = qs.filter(nivel=int(params["nivel"]))
        else:
            qs = qs.none()
        if params.get("padre", "").isdigit():
            qs = qs.filter(localidad_padre_id=int(params["padre"]))
        return qs.order_by("nombre")



from rest_framework.response import Response
from rest_framework.views import APIView

from usuarios.menu_service import menu_para_usuario

from rest_framework import permissions, viewsets
from rest_framework.response import Response

from .menu_service import menu_para_usuario


class MenuViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        return Response(menu_para_usuario(request.user))
import hashlib
from datetime import timedelta

from django.utils import timezone
from django_rest_passwordreset.models import (
    ResetPasswordToken,
    get_password_reset_token_expiry_time,
)
from django_rest_passwordreset.views import (
    ResetPasswordRequestToken,
    ResetPasswordValidateToken,
)
from rest_framework.throttling import SimpleRateThrottle


class PasswordResetEmailThrottle(SimpleRateThrottle):
    """Límite por correo (por usuario), sin importar desde qué IP se pida."""

    scope = "password_reset"

    def get_cache_key(self, request, view):
        email = str(request.data.get("email", "")).strip().lower()
        if not email:
            return None  # sin correo no se cuenta (la vista responderá 400)
        ident = hashlib.sha256(email.encode()).hexdigest()
        return self.cache_format % {"scope": self.scope, "ident": ident}


class PasswordResetIPThrottle(SimpleRateThrottle):
    """Límite amplio por IP: evita que alguien pruebe muchos correos distintos."""

    scope = "password_reset_ip"

    def get_cache_key(self, request, view):
        return self.cache_format % {"scope": self.scope, "ident": self.get_ident(request)}


class SolicitarResetView(ResetPasswordRequestToken):
    throttle_classes = [PasswordResetEmailThrottle, PasswordResetIPThrottle]


class ValidarTokenView(ResetPasswordValidateToken):
    """
    Igual que la vista original (200 si el enlace es válido, 404 si caducó),
    pero además devuelve cuántos segundos le quedan al enlace.
    """

    def post(self, request, *args, **kwargs):
        respuesta = super().post(request, *args, **kwargs)

        if respuesta.status_code == 200:
            token = ResetPasswordToken.objects.filter(key=request.data.get("token")).first()
            if token:
                vence = token.created_at + timedelta(hours=get_password_reset_token_expiry_time())
                segundos = int((vence - timezone.now()).total_seconds())
                respuesta.data["segundos_restantes"] = max(0, segundos)

        return respuesta

from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

class ConfigViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        return Response({'logo_url': request.build_absolute_uri(settings.LOGO_URL)})