from Aplicaciones.basemodel.api import GeneralListAPIView
from Aplicaciones.inventario.api.serializers.general_serializers import *

class UnidadMedidaListAPIView(GeneralListAPIView):
    serializer_class = UnidadMedidaSerializer

class CategoriaListAPIView(GeneralListAPIView):
    serializer_class = CategoriaSerializer

class MarcaListAPIView(GeneralListAPIView):
    serializer_class = MarcaSerializer