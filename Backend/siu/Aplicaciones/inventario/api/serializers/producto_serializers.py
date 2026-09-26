from Aplicaciones.user import serializers
from Aplicaciones.inventario.models import *
from Aplicaciones.inventario.api.serializers.general_serializers import *
from Aplicaciones.inventario.api.serializers.imagenes_serializers import *


class ProductoSerializer(serializers.ModelSerializer):
    UnidadMedida = serializers.SerializerMethodField()
    Categoria = serializers.SerializerMethodField()
    Marca = serializers.SerializerMethodField()
    Imagenes = ImagenProductoSerializer(many=True, read_only=True, source='imagenproducto_set')
    class Meta:
        model = Producto
        exclude = ('estado',)
"""
    def to_representation(self, instance):
        representation = {
            'id': instance.id,
            'nombre': instance.nombre,
            'descripcion': instance.descripcion,
            'precio': instance.precio,
            'UnidadMedida': UnidadMedidaSerializer(instance.UnidadMedida).data if instance.UnidadMedida else None,
            'Categoria': CategoriaSerializer(instance.Categoria).data if instance.Categoria else None,
            'Marca': MarcaSerializer(instance.Marca).data if instance.Marca else None,
            'Imagenes': ImagenProductoSerializer(instance.imagenproducto_set.all(), many=True).data,
        }
        return representation
"""
class ProductoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
