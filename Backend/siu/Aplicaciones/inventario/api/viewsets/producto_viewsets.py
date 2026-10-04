from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from Aplicaciones.inventario.models import Producto
from Aplicaciones.inventario.api.serializers.producto_serializers import (
    ProductoSerializer, ProductoRetrieveSerializer,
)


class ProductoViewSet(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    parser_classes = (JSONParser, MultiPartParser,)

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(estado='A')
        return self.get_serializer().Meta.model.objects.filter(
            codigo=pk, estado='A'
        ).first()

    def list(self, request):
        """
        Listado de Productos
        
        
        precio--->Precio del producto
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "total": queryset.count(),
            "totalNotFiltered": queryset.count(),
            "rows": serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Producto creado correctamente!'},
                            status=status.HTTP_201_CREATED)
        return Response({'message': '', 'error': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        producto = self.get_queryset(pk)
        if producto:
            serializer = ProductoRetrieveSerializer(producto)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'No existe un Producto con estos datos!'},
                        status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        producto = self.get_queryset(pk)
        if producto:
            serializer = self.serializer_class(producto, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Producto actualizado correctamente!'},
                                status=status.HTTP_200_OK)
            return Response({'message': '', 'error': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'No existe un Producto con estos datos!'},
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        producto = self.get_queryset(pk)
        if producto:
            producto.estado = 'I'
            producto.save()
            return Response({'message': 'Producto eliminado correctamente!'},
                            status=status.HTTP_200_OK)
        return Response({'error': 'No existe un Producto con estos datos!'},
                        status=status.HTTP_400_BAD_REQUEST)