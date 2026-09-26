from Aplicaciones.user import serializers
from Aplicaciones.inventario.models import *
from Aplicaciones.inventario.api.serializers.general_serializers import *

class ImagenProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenProducto
        fields = '__all__'