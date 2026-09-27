from rest_framework import generics, status
from rest_framework.response import Response
from Aplicaciones.basemodel.api import GeneralListAPIView
from Aplicaciones.inventario.api.serializers.producto_serializers import *

class ProductoListarAPI(GeneralListAPIView):
    serializer_class = ProductoSerializer
    def get_queryset(self):
        return Producto.objects.filter(estado = "A")

class ProductoCrearAPI(generics.CreateAPIView):
    serializer_class = ProductoCrearSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Producto creado exitosamente'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ProductoDetallarAPI(generics.RetrieveAPIView):
    queryset = Producto.objects.filter(estado = "A")
    serializer_class = ProductoSerializer
    lookup_field = 'codigo'

class ProductoCambiarEstado2API(generics.UpdateAPIView):
    serializer_class=ProductoCambiarEstadoSerializer
    lookup_field = 'codigo'

    def get_queryset(self, codigo = None):
            return Producto.objects.filter(codigo = codigo).first()

    def put(self, request, codigo=None, estado = None):
        serializer = self.update(self.get_queryset(codigo),estado = estado)
        if serializer:
            return Response({'message': 'Producto actualizado exitosamente'}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ProductoCambiarEstadoAPI(generics.UpdateAPIView):
    serializer_class = ProductoCambiarEstadoSerializer

    def put(self, request, codigo = None):
        estado = request.data.get('estado')

        producto = Producto.objects.filter(codigo = codigo).update(estado = estado)

        if producto:
            return Response(
                {'message': 'Producto actualizado exitosamente'},
                status=status.HTTP_200_OK
            )

        return Response(
            {'error': 'No existe un Producto con estos datos!'},
            status=status.HTTP_404_NOT_FOUND
        )


