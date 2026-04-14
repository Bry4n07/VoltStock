from django.urls import path
from . import views

urlpatterns = [
    path('categorias/', views.lista_categorias, name='lista-categorias'),
    path('categorias/<int:id>/', views.detalle_categoria, name='detalle-categoria'),
    path('componentes/', views.lista_componentes, name='lista-componentes'),
    path('componentes/<int:id>/', views.detalle_componente, name='detalle-componente'),
    path('pedidos/', views.gestion_pedidos, name='Pedido_cola'),
    path('devoluciones/', views.gestion_devoluciones, name='Devolucion_pila'),
]