from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Categoria, Componente, Pedido, Devolucion, HistorialMovimiento
from .serializers import CategoriaSerializer, ComponenteSerializer, PedidoSerializer, DevolucionSerializer, UserSerializer, ChangePasswordSerializer, HistorialMovimientoSerializer
from collections import deque

# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
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
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_usuarios(request):
    if not request.user.is_superuser:
        return Response({"error": "No tienes permisos."}, status=status.HTTP_403_FORBIDDEN)
    # Traemos los usuarios y los convertimos a una lista de diccionarios
    usuarios = list(User.objects.all().values('id', 'username', 'first_name', 'is_staff', 'is_superuser', 'is_active'))
    # Usamos JsonResponse con safe=False para permitir que se envíe una lista directamente
    return JsonResponse(usuarios, safe=False)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_usuario(request, pk):
    if not request.user.is_superuser:
        return Response({"error": "No tienes permisos."}, status=status.HTTP_403_FORBIDDEN)
        
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    
    if 'is_active' in data:
        if user == request.user and not data['is_active']:
            return Response({"error": "No puedes desactivar tu propia cuenta."}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = data['is_active']
        
    if 'rol' in data:
        if data['rol'] == 'admin':
            user.is_staff = True
            user.is_superuser = True
        elif data['rol'] == 'operador':
            user.is_staff = True
            user.is_superuser = False
        elif data['rol'] == 'auditor':
            user.is_staff = False
            user.is_superuser = False

    if 'password' in data and data['password'] != '':
        user.set_password(data['password'])

    user.save()
    return Response({"mensaje": "Usuario actualizado exitosamente."})
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_usuario_actual(request):
    rol = "auditor" 
    
    if request.user.is_superuser:
        rol = "admin"
    elif request.user.is_staff:
        rol = "tecnico"
        
    return Response({
        "username": request.user.username,
        "rol": rol,
        "first_name": request.user.first_name,
        "is_staff": request.user.is_staff,
        "is_superuser": request.user.is_superuser,
    })

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
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data, status=200)
        
    elif request.method == 'POST':
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        # Lógica para candelar un pedido sin alterar el stock
        cancelar_id = request.data.get('cancelar_id')
        if cancelar_id:
            try:
                pedido = Pedido.objects.get(id=cancelar_id)
                pedido.delete()
                return Response({"mensaje": "Pedido cancelado y eliminado de la cola"}, status=200)
            except Pedido.DoesNotExist:
                return Response({"error": "No encontrado"}, status=404)

        # Logica FIFO
        primer_pedido = Pedido.objects.all().order_by('fecha_solicitud').first()
        if primer_pedido:
            componente = primer_pedido.componente
            cantidad_a_restar = getattr(primer_pedido, 'cantidad', 1) 
            
            if componente.stock >= cantidad_a_restar:
                HistorialMovimiento.objects.create(
                    componente_nombre=componente.nombre,
                    usuario_nombre=request.user.get_full_name() or request.user.username,
                    cantidad=cantidad_a_restar,
                    tipo='SALIDA'
                )
                
                componente.stock -= cantidad_a_restar
                componente.save()
                primer_pedido.delete()
                return Response({"mensaje": "Pedido despachado y stock actualizado"}, status=204)
            else:
                return Response({"error": "Stock insuficiente para despachar este pedido"}, status=400)
                
        return Response({"error": "La cola está vacía"}, status=404)
    
@api_view(['GET','POST','DELETE'])
def gestion_devoluciones(request):
    if request.method == 'GET':
        devoluciones = Devolucion.objects.all().order_by('-fecha_devolucion')
        serializer = DevolucionSerializer(devoluciones, many=True)
        return Response(serializer.data, status=200)
        
    elif request.method == 'POST':
        serializer = DevolucionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        
    elif request.method == 'DELETE':
        # Si el frontend manda un ID específico para cancelar
        cancelar_id = request.data.get('cancelar_id')
        if cancelar_id:
            try:
                dev = Devolucion.objects.get(id=cancelar_id)
                dev.delete()
                return Response({"mensaje": "Retorno eliminado de la pila"}, status=200)
            except Devolucion.DoesNotExist:
                return Response({"error": "No encontrado"}, status=404)

        # Logica LIFO
        ultima_devolucion = Devolucion.objects.all().order_by('-fecha_devolucion').first()
        if ultima_devolucion:
            componente = ultima_devolucion.componente
            cantidad_a_sumar = getattr(ultima_devolucion, 'cantidad', 1)
            # Guardar en historial
            HistorialMovimiento.objects.create(
                componente_nombre=componente.nombre,
                usuario_nombre=request.user.get_full_name() or request.user.username,
                cantidad=cantidad_a_sumar,
                tipo='ENTRADA'
            )
            
            componente.stock += cantidad_a_sumar
            componente.save()
            ultima_devolucion.delete()
            return Response({"mensaje": "Reingresado con éxito"}, status=204)
            
        return Response({"error": "La pila está vacía"}, status=404)
    
@api_view(['GET'])
def obtener_historial(request):
    movimientos = HistorialMovimiento.objects.all().order_by('-fecha')
    serializer = HistorialMovimientoSerializer(movimientos, many=True)
    return Response(serializer.data)