from rest_framework import serializers

from Aplicaciones.inventario.models import UnidadMedida


class UnidadMedidaSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnidadMedida
        exclude = ('estado', 'usuario_crea', 'usuario_actualiza',
                   'fecha_crea', 'fecha_actualiza')

    def validate_abreviatura(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Debe ingresar una abreviatura.")
        return value

    def validate_nombre(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Debe ingresar un nombre.")
        return value

    def to_representation(self, instance):
        return {
            'codigo': instance.codigo,
            'abreviatura': instance.abreviatura,
            'nombre': instance.nombre,
            'id_texto_Empresa': instance.id_texto_Empresa,
        }