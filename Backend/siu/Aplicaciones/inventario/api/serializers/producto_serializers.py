from Aplicaciones.user import serializers
from Aplicaciones.inventario.models import *
from Aplicaciones.inventario.api.serializers.general_serializers import *
from Aplicaciones.inventario.api.serializers.imagenes_serializers import *


class ProductoSerializer(serializers.ModelSerializer):
    fk_codigo_marca = serializers.StringRelatedField()
    fk_codigo_categoria = serializers.StringRelatedField()
    fk_codigo_unidad_medida = serializers.StringRelatedField()

    class Meta:
        model = Producto
        exclude = ('estado',)
    
class ProductoCrearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ProductoCambiarEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['codigo','estado',]
    