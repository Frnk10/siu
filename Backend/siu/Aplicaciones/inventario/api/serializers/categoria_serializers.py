from rest_framework import serializers

from Aplicaciones.inventario.models import Categoria


class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria
        exclude = ('estado', 'usuario_crea', 'usuario_actualiza',
                   'fecha_crea', 'fecha_actualiza')

    def validate_nombre(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Debe ingresar un nombre de Categoría.")
        return value

    def to_representation(self, instance):
        return {
            'codigo': instance.codigo,
            'codigo_padre': instance.codigo_padre,
            'nombre': instance.nombre,
            'id_texto_Empresa': instance.id_texto_Empresa,
        }