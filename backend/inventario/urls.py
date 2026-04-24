from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='auth_register'),
    path('auth/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('auth/me/', views.obtener_usuario_actual, name='user_me'),
    path('auth/users/', views.listar_usuarios, name='listar_usuarios'),
    path('auth/users/<int:pk>/', views.actualizar_usuario, name='actualizar_usuario'),

    path('categorias/', views.lista_categorias, name='lista-categorias'),
    path('categorias/<int:id>/', views.detalle_categoria, name='detalle-categoria'),
    path('componentes/', views.lista_componentes, name='lista-componentes'),
    path('componentes/<int:id>/', views.detalle_componente, name='detalle-componente'),
    path('pedidos/', views.gestion_pedidos, name='Pedido_cola'),
    path('devoluciones/', views.gestion_devoluciones, name='Devolucion_pila'),
    path('historial/', views.obtener_historial, name='obtener_historial'),
]