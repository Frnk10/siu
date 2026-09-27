from Aplicaciones.basemodel.api import GeneralListAPIView
from Aplicaciones.inventario.api.serializers.general_serializers import *

class UnidadMedidaListarAPI(GeneralListAPIView):
    serializer_class = UnidadMedidaSerializer

class CategoriaListarAPI(GeneralListAPIView):
    serializer_class = CategoriaSerializer

class MarcaListarAPI(GeneralListAPIView):
    serializer_class = MarcaSerializer