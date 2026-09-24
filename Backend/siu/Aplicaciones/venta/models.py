from django.db import models
from Backend.siu.Aplicaciones.basemodel.models import BaseModel

# Create your models here.

class Cliente(models.Model):
    codigo = models.AutoField(primary_key=True)
    tiene_credito = models.CharField(
        default="N", max_length=1, help_text="S=SI, N=NO", blank=False, null=False
    )
    dias_mora = models.IntegerField(blank=True, null=True)
    monto_credito = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    saldo_credito = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    deuda_total = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    tipo = models.CharField(
        default="N", max_length=1, help_text="N=NORMAL, M=MAYORISTA", blank=True, null=True
    )

    def __str__(self):
        return self.tiene_credito

class Comprobante(BaseModel):
    codigo = models.AutoField(primary_key=True)
    pk_codigo_cliente = models.ForeignKey(
        Cliente,
        db_column='pk_codigo_cliente',
        related_name='codigo_clientes'
    )
    id_comprobante_referencia = models.IntegerField(blank=True, null=True)
    fecha_emision = models.DateTimeField(blank=False, null=False)
    clave_acceso = models.CharField(max_length=49, blank=False, null=False)
    numero_autorizacion = models.CharField(max_length=49, blank=True, null=True)
    estado_transmision = models.CharField(
        default="GEN", max_length=3, 
        help_text="GEN=GENERADO, TRA=TRANSMITIDO, AUT=AUTORIZADO, NAT=NO AUTORIZADO", 
        blank=False, null=False
    )
    fecha_respuesta = models.DateField(blank=True, null=True)
    tipo_comprobante = models.CharField(
        default="01", max_length=2, 
        help_text="01=FACTURA, 03=LIQUIDACION COMPRA, 04=NOTA CREDITO, 05=NOTA DEBITO, 06=GUIA REMISION, 07=GUIA REMISION", 
        blank=False, null=False
    )
    tipo_ambiente = models.CharField(
        default="1", max_length=1, help_text="1=PRUEBAS, 2=PRODUCCION", blank=False, null=False
    )
    serie = models.CharField(max_length=6, blank=False, null=False)
    secuencial = models.CharField(max_length=9, blank=False, null=False)
    codigo_numerico = models.CharField(max_length=8, blank=False, null=False)
    tipo_emision = models.CharField(
        default="1", max_length=1, help_text="1=NORMAL", blank=False, null=False
    )
    digito_verificador = models.CharField(max_length=1, blank=False, null=False)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    impuesto1 = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    impuesto2 = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    descuento = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    tipo = models.CharField(
        default="C", max_length=1, help_text="C=COMPROBANTE, P=PROFORMA", blank=False, null=False
    )
    estado_comprobante = models.CharField(
        max_length=1, help_text="G=GENERADO, P=PAGADO, D=DESPACHADO", blank=False, null=False
    )

    def __str__(self):
        return self.fecha_emision

class ComprobanteDetalle(models.Model):
    codigo = models.AutoField(primary_key=True)
    pk_codigo_cabecera = models.ForeignKey(
        Cliente,
        db_column='pk_codigo_cabecera',
        related_name='codigo_cabeceras'
    )
    id_producto = models.IntegerField(blank=False, null=False)
    id_promocion = models.IntegerField(blank=True, null=True)
    nombre_producto = models.CharField(max_length=250, blank=False, null=False)
    numero_serie = models.CharField(max_length=200, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    precio_compra = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    precio_unidad = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    descuento = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    tipo_precio = models.CharField(
        default="C", max_length=1, 
        help_text="C=CLIENTE, D=DISTRIBUIDOR, P=PROMOCION", blank=False, null=False
    )

    def __str__(self):
        return self.nombre_producto

class Cobro(BaseModel):
    codigo = models.AutoField(primary_key=True)
    pk_codigo_comprobante = models.ForeignKey(
        Comprobante,
        db_column='pk_codigo_comprobante',
        related_name='codigo_comprobantes'
    )
    forma = models.CharField(
        default="C", max_length=1, help_text="C=CONTADO, D=DIFERIDO", blank=False, null=False
    )
    fecha = models.DateField(blank=False, null=False)
    total_comprobante = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    numero_cuotas = models.IntegerField(blank=False, null=False)
    porcentaje_intereses = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    entrada = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    monto_cuota = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    estado_cobro = models.CharField(
        max_length=1, help_text="G=GENERADO, P=PENDIENTE, C=COMPLETADO", blank=False, null=False
    )

    def __str__(self):
        return self.total_comprobante

class CobroDetalle(BaseModel):
    codigo = models.AutoField(primary_key=True)
    pk_codigo_cobro= models.ForeignKey(
        Cobro,
        db_column='pk_codigo_cobro',
        related_name='codigo_cobros'
    )
    id_movimiento_caja = models.IntegerField(blank=True, null=True)
    numero_cuota = models.IntegerField(blank=False, null=False)
    fecha_cuota = models.DateField(blank=False, null=False)
    monto_cuota = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    fecha_cobro = models.DateField(blank=True, null=True)
    monto_cobro_efectivo = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    monto_cobro_transferencia = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    monto_cobro_cheque = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    monto_cobro_comprobante = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    id_comprobante = models.IntegerField(blank=True, null=True)
    monto_cobro_tarjeta = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    tipo_tarjeta = models.CharField(
        max_length=1, help_text="C=CREDITO, D=DEBITO", blank=True, null=True
    )
    monto_cobro_total = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    archivo1 = models.BinaryField(blank=True, null=True)
    archivo1 = models.BinaryField(blank=True, null=True)

    def __str__(self):
        return self.numero_cuota