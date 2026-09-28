from rest_framework import generics
from Aplicaciones.basemodel.api import GeneralListarAPIView
from Aplicaciones.inventario.api.serializers.imagenes_serializers import *

class ImagenProductoListarAPI(GeneralListarAPIView):
    serializer_class = ImagenProductoSerializer