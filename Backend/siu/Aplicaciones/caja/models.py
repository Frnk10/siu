from django.db import models
from Backend.siu.Aplicaciones.basemodel.models import BaseModel

class Financiera(BaseModel):
    codigo = models.AutoField(primary_key=True)
    codigo_auxiliar = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Caja(BaseModel):
    codigo = models.AutoField(primary_key=True)
    id_usuario = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=100)
    efectivo = models.DecimalField(max_digits=8,decimal_places=2, blank=False, null=False)
    transferencia = models.DecimalField(max_digits=8,decimal_places=2, blank=False, null=False)
    cheque = models.DecimalField(max_digits=8,decimal_places=2, blank=False, null=False)
    tarjeta = models.DecimalField(max_digits=8,decimal_places=2, blank=False, null=False)
    tipo_tarjeta = models.CharField(default="C", max_length=1, help_text="C=CRÉDITO, D=DÉBITO", blank=False, null=False)
    comprobante = models.DecimalField(max_digits=8,decimal_places=2, blank=False, null=False)
    id_comprobante = models.IntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=8,decimal_places=2, blank=False, null=False)
    estado_caja = models.CharField(default="C", max_length=1, help_text="A=ABIERTO, C=CERRADO, R=ARQUEO", blank=False, null=False)

    def __str__(self):
        return self.nombre

class MovimientoCaja(BaseModel):
    codigo = models.AutoField(primary_key=True)
    caja = models.ForeignKey(Caja,on_delete=models.PROTECT)
    financiera = models.ForeignKey(Financiera,on_delete=models.PROTECT, blank=True, null=True)
    motivo = models.CharField(default="I", max_length=1, help_text="A=APERTURA, I=INGRESO, R=ARQUEO, G=GASTO, C=CIERRE")
    detalle = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    efectivo = models.DecimalField(max_digits=8,decimal_places=2)
    transferencia = models.DecimalField(max_digits=8,decimal_places=2)
    cheque = models.DecimalField(max_digits=8,decimal_places=2)
    tarjeta = models.DecimalField(max_digits=8,decimal_places=2)
    tipo_tarjeta = models.CharField(default="C", max_length=1, help_text="C=CRÉDITO, D=DÉBITO")
    comprobante = models.DecimalField(max_digits=8,decimal_places=2)
    id_comprobante = models.IntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=8,decimal_places=2)
    diferencia_efectivo = models.DecimalField(max_digits=8,decimal_places=2)
    diferencia_transferencia = models.DecimalField(max_digits=8,decimal_places=2)
    diferencia_cheque = models.DecimalField(max_digits=8,decimal_places=2)
    diferencia_tarjeta = models.DecimalField(max_digits=8,decimal_places=2)
    diferencia_comprobante = models.DecimalField(max_digits=8,decimal_places=2)
    diferencia_total = models.DecimalField(max_digits=8,decimal_places=2)

    def __str__(self):
        return self.nombre