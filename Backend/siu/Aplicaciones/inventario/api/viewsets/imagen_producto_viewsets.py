from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from Aplicaciones.inventario.models import ImagenProducto
from Aplicaciones.inventario.api.serializers.imagen_producto_serializers import (
    ImagenProductoSerializer,
)


class ImagenProductoViewSet(viewsets.ModelViewSet):
    serializer_class = ImagenProductoSerializer
    parser_classes = (JSONParser, MultiPartParser,)

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(estado='A')
        return self.get_serializer().Meta.model.objects.filter(
            id=pk, estado='A'
        ).first()

    def list(self, request):
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
            return Response({'message': 'Imagen registrada correctamente!'},
                            status=status.HTTP_201_CREATED)
        return Response({'message': '', 'error': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        obj = self.get_queryset(pk)
        if obj:
            return Response(self.get_serializer(obj).data, status=status.HTTP_200_OK)
        return Response({'error': 'No existe una Imagen con estos datos!'},
                        status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        obj = self.get_queryset(pk)
        if obj:
            serializer = self.serializer_class(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Imagen actualizada correctamente!'},
                                status=status.HTTP_200_OK)
            return Response({'message': '', 'error': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'No existe una Imagen con estos datos!'},
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        obj = self.get_queryset(pk)
        if obj:
            obj.estado = 'I'
            obj.save()
            return Response({'message': 'Imagen eliminada correctamente!'},
                            status=status.HTTP_200_OK)
        return Response({'error': 'No existe una Imagen con estos datos!'},
                        status=status.HTTP_400_BAD_REQUEST)