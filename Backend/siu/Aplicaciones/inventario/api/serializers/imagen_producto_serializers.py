from rest_framework import serializers

from Aplicaciones.inventario.models import ImagenProducto


class ImagenProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImagenProducto
        exclude = ('estado', 'usuario_crea', 'usuario_actualiza',
                   'fecha_crea', 'fecha_actualiza')

    def validate_imagen(self, value):
        if not value:
            raise serializers.ValidationError("Debe subir una imagen.")
        return value

    def validate_orden(self, value):
        if value < 0:
            raise serializers.ValidationError("El orden debe ser un número positivo.")
        return value

    def to_representation(self, instance):
        return {
            'codigo': instance.codigo if hasattr(instance, 'codigo') else instance.id,
            'producto': instance.producto.codigo,
            'producto_nombre': instance.producto.nombre,
            'imagen': instance.imagen.url if instance.imagen else '',
            'principal': instance.principal,
            'orden': instance.orden,
        }