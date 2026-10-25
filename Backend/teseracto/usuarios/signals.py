from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .menu_service import invalidar_cache_menu
from .models import AccesoMenu, Menu


@receiver([post_save, post_delete], sender=Menu)
@receiver([post_save, post_delete], sender=AccesoMenu)
def _invalidar(sender, **kwargs):
    invalidar_cache_menu()