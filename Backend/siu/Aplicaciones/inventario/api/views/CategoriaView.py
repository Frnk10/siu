from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from Aplicaciones.inventario.models import Categoria
from Aplicaciones.inventario.api.serializers.CategoriaSerializer import CategoriaSerializer
from Aplicaciones.inventario.api.serializers.CategoriaSerializer import CategoriaEstadoSerializer
from rest_framework.exceptions import ValidationError
from datetime import date

# Solo listar todos (sin crear)
class CategoriaListarTodosView(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# Solo listar por estado (sin crear)
class CategoriaListarView(generics.ListAPIView):
    serializer_class = CategoriaSerializer
    def get_queryset(self):
        estado = self.kwargs.get('estado', '').upper()
        codigos_validos = [codigo for codigo, etiqueta in Categoria.ESTADO_CHOICES]
        if estado not in codigos_validos:
            # lanzar error 400
            raise ValidationError(
                {"estado": "Valor inválido. Use 'A' o 'I'."}
            )
        return Categoria.objects.filter(estado = estado)
# Solo crear (sin listar)
class CategoriaCrearView(generics.CreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response(
                {'mensaje': 'Categoría creada correctamente', 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# Solo detalle (sin modificar)
class CategoriaDetallarView(generics.RetrieveAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# Solo actualizar (sin eliminar)
class CategoriaActualizarView(generics.RetrieveUpdateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    def perform_update(self, serializer):
        serializer.save(fecha_actualiza=date.today())

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(
                {
                    'mensaje': 'Categoría actualizada correctamente',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
# Solo eliminar
class CategoriaEliminarView(generics.RetrieveDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# PATCH /categoria/cambiarEstado/{id}/estado/  body: {"estado": "A"} o {"estado": "I"}
# También acepta query param: /categoria/cambiarEstado/{id}/estado/?estado=A
class CategoriaCambiarEstadoView(APIView):
    """
    Actualiza únicamente el campo 'estado'.
    Acepta el valor por:
      - Body JSON:  {"estado": "A"}
      - Query param: ?estado=A
    """

    def patch(self, request, codigo):
        # 1. Buscar el registro
        try:
            categoria = Categoria.objects.get(codigo=codigo)
        except Categoria.DoesNotExist:
            return Response(
                {'error': 'Categoría no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2. Obtener el valor desde body o query params
        estado = request.data.get('estado') or request.query_params.get('estado')

        if estado is None:
            return Response(
                {'error': 'Debe enviar el campo "estado" (A o I)'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Validar con el serializer
        serializer = CategoriaEstadoSerializer(data={'estado': estado})
        serializer.is_valid(raise_exception=True)
        estado_validado = serializer.validated_data['estado']

        # 4. Actualizar SOLO ese campo → 1 sola query
        categoria.estado = estado_validado
        categoria.save(update_fields=['estado'])

        # 5. Responder
        return Response(
            {
                'mensaje': 'Estado actualizado correctamente',
                'data': CategoriaSerializer(categoria).data
            },
            status=status.HTTP_200_OK
        )