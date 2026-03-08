from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/novo/', views.novo_cliente, name='novo_cliente'),
    path('servicos/', views.listar_servicos, name='listar_servicos'),
    path('servicos/novo/', views.novo_servico, name='novo_servico'),
    path('servicos/<int:servico_id>/', views.detalhe_servico, name='detalhe_servico'),
    path('servicos/pesquisar/', views.pesquisar_servicos, name='pesquisar_servicos'),
]