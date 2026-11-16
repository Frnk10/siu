from rest_framework.permissions import DjangoModelPermissions


class ModeloPermisos(DjangoModelPermissions):
    """
    Valida los permisos de Django asignados a los grupos del usuario:
      GET / HEAD   -> view
      POST         -> add
      PUT / PATCH  -> change
      DELETE       -> delete
    El modelo se toma del queryset del ViewSet. También exige autenticación.
    """

    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": ["%(app_label)s.view_%(model_name)s"],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }