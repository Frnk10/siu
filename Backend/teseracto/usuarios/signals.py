
from django.db.models.signals import (
    m2m_changed,
    post_delete,
    post_save,
)
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .menu_service import invalidar_cache_menu
from .models import Menu

User = get_user_model()


# Invalidar cuando se crea, modifica o elimina un menú
@receiver([post_save, post_delete], sender=Menu)
def invalidar_por_menu(sender, **kwargs):
    invalidar_cache_menu()


# Invalidar cuando se agregan o quitan permisos de un grupo
@receiver(m2m_changed, sender=Group.permissions.through)
def invalidar_por_permisos_grupo(sender, **kwargs):
    invalidar_cache_menu()


# Invalidar cuando se agregan o quitan usuarios de un grupo
@receiver(m2m_changed, sender=User.groups.through)
def invalidar_por_grupos_usuario(sender, **kwargs):
    invalidar_cache_menu()


# Invalidar cuando se asignan o quitan permisos directamente a usuarios
@receiver(m2m_changed, sender=User.user_permissions.through)
def invalidar_por_permisos_usuario(sender, **kwargs):
    invalidar_cache_menu()
