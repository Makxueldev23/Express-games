from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.lista_pedidos, name='lista'),
    path('novo/', views.criar_pedido, name='criar'),
    path('<int:pk>/', views.detalhe_pedido, name='detalhe'),
]