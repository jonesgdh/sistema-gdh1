from django.urls import path
from . import views

app_name = 'tarefas'

urlpatterns = [
    path('', views.index, name='index'),
    
   
    # CLIENTES
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/novo/', views.novo_cliente, name='novo_cliente'),
    path('clientes/<int:cliente_id>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:cliente_id>/deletar/', views.excluir_cliente, name='excluir_cliente'),
    
    
     # SERVIÇOS
    path('servicos/', views.listar_servicos, name='listar_servicos'),
    path('servicos/novo/', views.novo_servico, name='novo_servico'),
    path('servicos/<int:servico_id>/', views.detalhe_servico, name='detalhe_servico'),
    path('servicos/<int:servico_id>/editar/', views.editar_servico, name='editar_servico'),
    path('servicos/<int:servico_id>/deletar/', views.excluir_servico, name='excluir_servico'),
    
  
    # FINANCEIRO
    path('financeiro/', views.financeiro, name='financeiro'),
    path('financeiro/exportar/excel/', views.exportar_financeiro_excel, name='exportar_financeiro_excel'),
    
     # DESPESAS
    path('despesas/<int:despesa_id>/editar/', views.editar_despesa, name='editar_despesa'),
    path('despesas/<int:despesa_id>/deletar/', views.excluir_despesa, name='excluir_despesa'),

    # PESQUISA
    path('pesquisar-servicos/', views.pesquisar_servicos, name='pesquisar_servicos'),
        
    # AUDITORIA
    path('auditoria/', views.arquivo_auditoria, name='arquivo_auditoria'),
    
    # CALENDARIO
    path('calendario/', views.calendario_agendamentos, name='calendario_agendamentos'),
    path('eventos-agendamentos/', views.eventos_agendamentos, name='eventos_agendamentos'),

    # LOGOUT
    path('logout/', views.logout_view, name='logout'),
]
    
   
   