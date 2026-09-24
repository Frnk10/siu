from django.db import models
from Backend.siu.Aplicaciones.basemodel.models import BaseModel

class UnidadMedida(BaseModel):
    codigo = models.AutoField(primary_key=True)
    abreviatura = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    id_texto_Empresa = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Categoria(BaseModel):
    codigo = models.AutoField(primary_key=True)
    codigo_padre = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=100)
    id_texto_Empresa = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Marca(BaseModel):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    id_texto_Empresa = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class CentroCosto(BaseModel):
    codigo = models.AutoField(primary_key=True)
    fk_codigo_sucursal = models.IntegerField(blank=True, null=True)
    codigo_padre = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=1, default='B', help_text="B=BODEGA, A=ALMACEN")
    categoria = models.CharField(max_length=1, default='F', help_text="F=FISICO, L=LOGICO")
    ubicacion = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Producto(BaseModel):    
    codigo = models.AutoField(primary_key=True)
    fk_codigo_categoria = models.IntegerField(blank=True, null=True)
    fk_codigo_marca = models.IntegerField(blank=True, null=True)
    fk_codigo_unidad_medida = models.IntegerField(blank=True, null=True)
    id_empresa = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=250)
    modelo = models.CharField(max_length=100)
    stock_minimo = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    stock_maximo = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    stock = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    precio_compra = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    porcentaje_cliente = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    precio_venta_cliente = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    porcentaje_distribuidor = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    precio_venta_distribuidor = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    porcentaje_promocion = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    precio_venta_promocion = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    estado_promocion = models.CharField(max_length=1, default='N', help_text="N=NO, S=SI")
    tipo = models.CharField(max_length=1, default='P', help_text="P=PRODUCTO, S=SERVICIO")
    caracteristica = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.nombre

class CentroProducto (BaseModel):
    codigo = models.AutoField(primary_key=True)
    fk_codigo_centro_costo = models.IntegerField(blank=True, null=True)
    fk_codigo_producto = models.IntegerField(blank=True, null=True)
    stock = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    porcentaje_cliente = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    precio_venta_cliente = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    porcentaje_distribuidor = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    precio_venta_distribuidor = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    porcentaje_promocion = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    precio_venta_promocion = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Kardex(BaseModel):
    codigo = models.AutoField(primary_key=True)
    id_empresa = models.IntegerField(blank=True, null=True)
    id_comprobante = models.IntegerField(blank=True, null=True)
    tipo_movimiento = models.CharField(max_length=1, default='I', help_text="I=INGRESO, S=SALIDA")
    id_bodega = models.IntegerField(blank=True, null=True)
    id_compra = models.IntegerField(blank=True, null=True)
    id_producto = models.IntegerField(blank=True, null=True)
    id_venta = models.IntegerField(blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    cantidad_entrada = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    costo_unitario_entrada = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    costo_total_entrada = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    cantidad_salida = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    costo_unitario_salida = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    costo_total_salida = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    fecha_contable = models.DateField(blank=True, null=True)
    fecha_documento= models.DateField(blank=True, null=True)
    

    def __str__(self):
        return self.nombre