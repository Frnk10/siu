from django.db import models

class BaseModel(models.Model):
    estado = models.CharField(default="A", max_length=1, help_text="A=Activo, I=Inactivo")
    usuario_crea = models.IntegerField(blank=False, null=False)
    usuario_actualiza = models.IntegerField(blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True)
    fecha_actualiza = models.DateField(auto_now=True)

    def crear(self, usuario_crea):
            self.usuario_crea = usuario_crea
            self.save()

    def actualizar(self, usuario_actualiza):
        self.usuario_actualiza = usuario_actualiza
        self.save()

    def cambiar_estado(self, usuario_actualiza, estado):
        self.estado = estado
        self.usuario_actualiza = usuario_actualiza
        self.save()

    class Meta:
        abstract = True