from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from Aplicaciones.inventario.models import Categoria
from Aplicaciones.inventario.api.serializers.categoria_serializers import (
    CategoriaSerializer,
)


class CategoriaViewSet(viewsets.GenericViewSet):
    model = Categoria
    serializer_class = CategoriaSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(estado='A')

    def get_object(self):
        return self.get_serializer().Meta.model.objects.filter(
            codigo=self.kwargs['pk'], estado='A'
        ).first()

    @action(detail=False, methods=['get'])
    def get_categorias(self, request):
        data = Categoria.objects.filter(estado='A')
        serializer = CategoriaSerializer(data, many=True)
        return Response(serializer.data)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "total": queryset.count(),
            "totalNotFiltered": queryset.count(),
            "rows": serializer.data
        })

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Categoría registrada correctamente!'},
                            status=status.HTTP_201_CREATED)
        return Response({'message': '', 'error': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        obj = self.get_object()
        if obj:
            return Response(self.get_serializer(obj).data)
        return Response({'message': '', 'error': 'Categoría no encontrada!'},
                        status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        obj = self.get_object()
        if obj:
            serializer = self.serializer_class(instance=obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Categoría actualizada correctamente!'},
                                status=status.HTTP_200_OK)
            return Response({'message': '', 'error': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': '', 'error': 'Categoría no encontrada!'},
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        obj = self.get_object()
        if obj:
            obj.estado = 'I'
            obj.save()
            return Response({'message': 'Categoría eliminada correctamente!'},
                            status=status.HTTP_200_OK)
        return Response({'message': '', 'error': 'Categoría no encontrada!'},
                        status=status.HTTP_400_BAD_REQUEST)