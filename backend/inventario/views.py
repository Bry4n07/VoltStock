from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Categoria, Componente
from .serializers import CategoriaSerializer, ComponenteSerializer

# Create your views here.
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