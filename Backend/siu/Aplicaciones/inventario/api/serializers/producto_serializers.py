from rest_framework import serializers

from Aplicaciones.inventario.models import Producto


class ProductoSerializer(serializers.ModelSerializer):


    class Meta:
        model = Producto
        exclude = ('estado', 'usuario_crea', 'usuario_actualiza',
                   'fecha_crea', 'fecha_actualiza')

    def validate_fk_codigo_categoria(self, value):
        if value is None or value == '':
            raise serializers.ValidationError("Debe ingresar una Categoría.")
        return value

    def validate_fk_codigo_marca(self, value):
        if value is None or value == '':
            raise serializers.ValidationError("Debe ingresar una Marca.")
        return value

    def validate_fk_codigo_unidad_medida(self, value):
        if value is None or value == '':
            raise serializers.ValidationError("Debe ingresar una Unidad de Medida.")
        return value

    def validate(self, data):
        if 'fk_codigo_categoria' not in data.keys():
            raise serializers.ValidationError({
                "fk_codigo_categoria": "Debe ingresar una Categoría."
            })
        if 'fk_codigo_marca' not in data.keys():
            raise serializers.ValidationError({
                "fk_codigo_marca": "Debe ingresar una Marca."
            })
        if 'fk_codigo_unidad_medida' not in data.keys():
            raise serializers.ValidationError({
                "fk_codigo_unidad_medida": "Debe ingresar una Unidad de Medida."
            })
        return data

    def to_representation(self, instance):
        imagen_principal = instance.imagenproducto_set.filter(
            principal=True, estado='A'
        ).first()

        return {
            'codigo': instance.codigo,
            'nombre': instance.nombre,
            'modelo': instance.modelo,
            'fk_codigo_categoria': instance.fk_codigo_categoria.codigo
                if instance.fk_codigo_categoria else None,
            'categoria': instance.fk_codigo_categoria.nombre
                if instance.fk_codigo_categoria else '',
            'fk_codigo_marca': instance.fk_codigo_marca.codigo
                if instance.fk_codigo_marca else None,
            'marca': instance.fk_codigo_marca.nombre
                if instance.fk_codigo_marca else '',
            'fk_codigo_unidad_medida': instance.fk_codigo_unidad_medida.codigo
                if instance.fk_codigo_unidad_medida else None,
            'unidad_medida': instance.fk_codigo_unidad_medida.nombre
                if instance.fk_codigo_unidad_medida else '',
            'id_empresa': instance.id_empresa,
            'stock': instance.stock if instance.stock is not None else 0,
            'stock_minimo': instance.stock_minimo,
            'stock_maximo': instance.stock_maximo,
            'precio_compra': instance.precio_compra,
            'porcentaje_cliente': instance.porcentaje_cliente,
            'precio_venta_cliente': instance.precio_venta_cliente,
            'porcentaje_distribuidor': instance.porcentaje_distribuidor,
            'precio_venta_distribuidor': instance.precio_venta_distribuidor,
            'porcentaje_promocion': instance.porcentaje_promocion,
            'precio_venta_promocion': instance.precio_venta_promocion,
            'estado_promocion': instance.estado_promocion,
            'tipo': instance.tipo,
            'caracteristica': instance.caracteristica,
            'imagen': imagen_principal.imagen.url if imagen_principal else '',
        }


class ProductoRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        exclude = ('estado', 'usuario_crea', 'usuario_actualiza',
                   'fecha_crea', 'fecha_actualiza')