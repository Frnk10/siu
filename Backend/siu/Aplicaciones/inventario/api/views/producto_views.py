from rest_framework import generics, status
from rest_framework.response import Response
from Aplicaciones.basemodel.api import GeneralListAPIView
from Aplicaciones.inventario.api.serializers.producto_serializers import *

class ProductoListAPIView(GeneralListAPIView):
    serializer_class = ProductoSerializer
    def get_queryset(self):
        return Producto.objects.filter(estado=True)

class ProductoCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductoCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            producto = serializer.save()
            return Response({'message': 'Producto creado exitosamente', 'producto_id': producto.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)