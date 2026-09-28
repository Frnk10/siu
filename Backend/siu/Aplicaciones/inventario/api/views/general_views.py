from Aplicaciones.basemodel.api import GeneralListarAPIView
from Aplicaciones.inventario.api.serializers.general_serializers import *

class UnidadMedidaListarAPI(GeneralListarAPIView):
    serializer_class = UnidadMedidaSerializer

class MarcaListarAPI(GeneralListarAPIView):
    serializer_class = MarcaSerializer