from Aplicaciones.inventario.models import *
from rest_framework import serializers

class UnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadMedida
        exclude = ('estado',)

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        exclude = ('estado',)

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        exclude = ('estado',)