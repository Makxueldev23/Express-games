from django.urls import path
from . import views

app_name = 'jogos'

urlpatterns = [
    path('', views.JogoListView.as_view(), name='lista'),
    path('<int:pk>/', views.JogoDetailView.as_view(), name='detalhe'),
    path('novo/', views.JogoCreateView.as_view(), name='criar'),
    path('<int:pk>/editar/', views.JogoUpdateView.as_view(), name='editar'),
    path('<int:pk>/excluir/', views.JogoDeleteView.as_view(), name='excluir'),
]