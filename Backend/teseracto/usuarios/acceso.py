from .models import Empleado, Empresa


def empresas_permitidas(user):
    """Ids de las empresas que el usuario representa o en las que trabaja."""
    ids = set(
        Empresa.objects.filter(representante=user, estado="A")
        .values_list("codigo", flat=True)
    )
    ids.update(
        Empleado.objects.filter(pk=user.pk, is_active=True, empresa__estado="A")
        .values_list("empresa_id", flat=True)
    )
    return ids