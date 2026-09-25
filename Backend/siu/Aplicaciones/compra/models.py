from django.db import models
from Backend.siu.Aplicaciones.basemodel.models import BaseModel
from seguridad.models import Persona

class Proveedor(Persona):
    numero_cuenta = models.CharField( max_length=50, blank=False, null=False)

    def __str__(self):
        return self.numero_cuenta

class Compra(BaseModel):
    codigo = models.AutoField(primary_key=True)
    fk_codigo_proveedor = models.ForeignKey(
        Proveedor,
        db_column='fk_codigo_cliente',
        related_name='FK_PROVEEDOR_COMPRA'
    )
    id_comprobante_referencia = models.IntegerField(blank=True, null=True)
    fecha_compra = models.DateTimeField(blank=False, null=False)
    numero_autorizacion = models.CharField(max_length=49, blank=True, null=True)
    secuencial = models.CharField(max_length=9, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    impuesto1 = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    impuesto2 = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    descuento = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    tipo = models.CharField(
        default="C", max_length=1, help_text="C=COMPRA, P=PEDIDO", blank=False, null=False
    )
    estado_compra = models.CharField(
        max_length=1, default="G" help_text="G=GENERADO, A=APROBADO P=PAGADO, R=RECIBIDO EN BODEGA", blank=False, null=False
    )

    def __str__(self):
        return self.fecha_emision

class CompraDetalle(models.Model):
    codigo = models.AutoField(primary_key=True)
    fk_codigo_compra = models.ForeignKey(
        Compra,
        db_column='fk_codigo_comprobante',
        related_name='FK_COMPRA_DETALLE'
    )
    id_producto = models.IntegerField(blank=False, null=False)
    id_promocion = models.IntegerField(blank=True, null=True)
    nombre_producto = models.CharField(max_length=250, blank=False, null=False)
    numero_serie = models.CharField(max_length=200, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    precio_unidad = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    descuento = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)

    def __str__(self):
        return self.nombre_producto

class Pago(BaseModel):
    codigo = models.AutoField(primary_key=True)
    fk_codigo_compra = models.ForeignKey(
        Compra,
        db_column='fk_codigo_compra',
        related_name='FK_COMPRA_PAGO'
    )
    forma = models.CharField(
        default="C", max_length=1, help_text="C=CONTADO, D=DIFERIDO", blank=False, null=False
    )
    fecha = models.DateField(blank=False, null=False)
    total_compra = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    numero_cuotas = models.IntegerField(blank=False, null=False)
    porcentaje_intereses = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    entrada = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    monto_cuota = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    estado_pago = models.CharField(
        max_length=1, help_text="G=GENERADO, P=PENDIENTE, C=COMPLETADO", blank=False, null=False
    )

    def __str__(self):
        return self.total_comprobante

class PagoDetalle(BaseModel):
    codigo = models.AutoField(primary_key=True)
    fk_codigo_pago= models.ForeignKey(
        Pago,
        db_column='fk_codigo_pago',
        related_name='FK_PAGO_DETALLE'
    )
    id_movimiento_caja = models.IntegerField(blank=True, null=True)
    numero_cuota = models.IntegerField(blank=False, null=False)
    fecha_cuota = models.DateField(blank=False, null=False)
    monto_cuota = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    fecha_pago = models.DateField(blank=True, null=True)
    monto_pago_efectivo = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    monto_pago_transferencia = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    monto_pago_cheque = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    monto_pago_comprobante = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    id_comprobante = models.IntegerField(blank=True, null=True)
    monto_pago_tarjeta = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    tipo_tarjeta = models.CharField(
        max_length=1, help_text="C=CREDITO, D=DEBITO", blank=True, null=True
    )
    monto_pago_total = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    archivo1 = models.BinaryField(blank=True, null=True)
    archivo2 = models.BinaryField(blank=True, null=True)

    def __str__(self):
        return self.numero_cuota
