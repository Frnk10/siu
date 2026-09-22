from rest_framework.decorators import api_view
from rest_framework.response import Response

from Aplicaciones.user.models import User
from Aplicaciones.user.serializers import *


@api_view(['GET', 'POST'])
def user_view(request):

    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        test_data = {
            "name": "",
            "email": "",
            "password": ""
        }
        test_user = UserSerializer(data=test_data)
        if test_user.is_valid():
            print("Test user is valid")
        else:
            print("Test user is not valid:", test_user.errors)

        return Response(serializer.data, status=200)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):

    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(
            {"error": "Usuario no encontrado"},
            status=404
        )

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=204)