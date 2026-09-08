from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.lista_pedidos, name='lista'),
    path('carrinho/', views.ver_carrinho, name='carrinho'),
    path('carrinho/adicionar/<int:jogo_id>/', views.adicionar_ao_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover/<int:jogo_id>/', views.remover_do_carrinho, name='remover_carrinho'),
    path('carrinho/finalizar/', views.finalizar_pedido, name='finalizar'),
    path('<int:pk>/', views.detalhe_pedido, name='detalhe'),
    path('<int:pk>/cancelar/', views.cancelar_pedido, name='cancelar'),
]