from rest_framework import serializers
from Aplicaciones.inventario.models import Categoria

class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria
        fields = ['codigo', 'nombre', 'id_texto_Empresa', 
                  'codigo_padre', 'estado', 
                  'usuario_crea', 'fecha_crea',
                  'usuario_actualiza', 'fecha_actualiza'
                  ]
        read_only_fields = ['codigo']

    def validar_codigo(self, value):
        value = value.strip().upper()
        if not value:
            raise serializers.ValidationError("El código no puede estar vacío.")
        return value

    def validar_nombre(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

    def validar_usuario_crea(self, value):
            value = value.strip().upper()
            if not value:
                raise serializers.ValidationError("El usuario crea no puede estar vacío.")
            return value

    def validate(self, data):
        # Validación de unicidad en actualización (excluye el propio registro)
        codigo = data.get('codigo')
        if codigo:
            qs = Categoria.objects.filter(codigo=codigo)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {"codigo": "Ya existe una categoría con este código."}
                )
        return data


# Serializer específico para actualizar SOLO el estado
class CategoriaEstadoSerializer(serializers.Serializer):
    estado = serializers.ChoiceField(choices=Categoria.ESTADO_CHOICES)