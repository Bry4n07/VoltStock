from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Categoria, Componente, Pedido, Devolucion
from .serializers import CategoriaSerializer, ComponenteSerializer, PedidoSerializer, DevolucionSerializer, UserSerializer, ChangePasswordSerializer
from collections import deque

# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["La contraseña actual es incorrecta."]}, 
                    status=400
                )
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response ({"detail": "¡Contraseña actualizada con éxito!"}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=400)

@api_view(['GET', 'POST'])
def lista_categorias(request):
    
    if request.method == 'GET':
        categorias_db = Categoria.objects.all()
        traductor = CategoriaSerializer(categorias_db, many=True)
        return Response(traductor.data)
        
    elif request.method == 'POST':
        traductor = CategoriaSerializer(data=request.data)
        if traductor.is_valid():
            traductor.save()
            return Response(traductor.data, status=201)
        return Response(traductor.errors, status=400)
    
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_categoria(request, id):
    # Primero verificamos si esa ID específica existe
    try:
        categoria_db = Categoria.objects.get(id=id)
    except Categoria.DoesNotExist:
        return Response(status=404)
        
    if request.method == 'GET':
        traductor = CategoriaSerializer(categoria_db)
        return Response(traductor.data)
        
    elif request.method == 'PUT':
        traductor = CategoriaSerializer(categoria_db, data=request.data)
        if traductor.is_valid():
            traductor.save()
            return Response(traductor.data, status=200)
        return Response(traductor.errors, status=400)
        
    elif request.method == 'DELETE':
        categoria_db.delete()
        return Response(status=204)
    

@api_view(['GET', 'POST'])
def lista_componentes(request):
    if request.method == 'GET':
        componente_db = Componente.objects.all()
        traductor = ComponenteSerializer(componente_db, many=True)
        return Response(traductor.data) 
    elif request.method == 'POST':
        traductor = ComponenteSerializer(data=request.data)
        if traductor.is_valid():
            traductor.save()
            return Response(traductor.data, status=201)
        return Response(traductor.errors, status=400)
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_componente(request, id):
    try:
        componente_db = Componente.objects.get(id=id)
    except Componente.DoesNotExist:
        return Response(status=404)
    
    if request.method == 'GET':
        traductor = ComponenteSerializer(componente_db)
        return Response (traductor.data)
    elif request.method == 'PUT':
        traductor = ComponenteSerializer(componente_db, data=request.data)
        if traductor.is_valid():
            traductor.save()
            return Response(traductor.data,status=200)
        return Response(traductor.errors, status=400)
    
    elif request.method == 'DELETE':
        componente_db.delete()
        return Response(status=204)
    

@api_view(['GET','POST','DELETE'])
def gestion_pedidos(request):
    if request.method == 'GET':
        pedidos = Pedido.objects.all().order_by('fecha_solicitud')
        cola = deque(pedidos)
        serializer = PedidoSerializer(cola, many=True)
        return Response(serializer.data, status=200)
    elif request.method == 'POST':
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status = 400)
    elif request.method == 'DELETE':
        primer_pedido = Pedido.objects.all().order_by('fecha_solicitud').first()
        if primer_pedido:
            primer_pedido.delete()
            return Response({"Pedido atendido"}, status = 204)
        return Response({"Error": "Cola vacia"},status=404)
    
@api_view(['GET','POST','DELETE'])
def gestion_devoluciones(request):
    if request.method == 'GET':
        devoluciones = Devolucion.objects.all().order_by('-fecha_devolucion')
        serializer = DevolucionSerializer(devoluciones, many=True)
        return Response(request.data, status=200)
    elif request.method == 'POST':
        serializer = DevolucionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    if request.method == 'DELETE':
        ultima_devolucion = Devolucion.objects.all().order_by('fecha_devolucion').first()
        if ultima_devolucion:
            ultima_devolucion.delete()
            return Response({"Componente devuelto"}, status=204)
        return Response({"Error": "Pila Vacia"},status=404)