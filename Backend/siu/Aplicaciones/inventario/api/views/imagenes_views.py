from rest_framework import generics
from Aplicaciones.basemodel.api import GeneralListAPIView
from Aplicaciones.inventario.api.serializers.imagenes_serializers import *

class ImagenProductoListarAPI(GeneralListAPIView):
    serializer_class = ImagenProductoSerializer