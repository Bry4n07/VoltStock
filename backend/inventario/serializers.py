from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import Categoria, Componente, Pedido, Devolucion

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'is_staff']
        extra_kwargs = { 'password': {'write_only': True}}

    def create(serlf, valiated_data):
        user = User.objects.create_user(
                username=valiated_data['username'],
                password=valiated_data['password'],
                first_name=valiated_data.get('first_name', ''),
                is_staff=valiated_data.get('is_staff', False)
        )
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = cls.for_user(user)
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        token['first_name'] = user.first_name
        return token

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ComponenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Componente
        fields = '__all__'
        
class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
        
class DevolucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devolucion
        fields = '__all__'