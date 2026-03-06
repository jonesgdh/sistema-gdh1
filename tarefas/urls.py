from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('clientes/novo/', views.novo_cliente, name='novo_cliente'),
    path('clientes/', views.listar_clientes, name='listar_clientes'),

    path('servicos/novo/', views.novo_servico, name='novo_servico'),
    path('servicos/', views.listar_servicos, name='listar_servicos'),
]