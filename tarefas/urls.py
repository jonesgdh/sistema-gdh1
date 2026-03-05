from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),  # /tarefas/

    path("nova/", views.nova_tarefa, name="nova_tarefa"),
    path("pesquisar/", views.pesquisar_tarefas, name="pesquisar_tarefas"),

    path("projetos/novo/", views.novo_projeto, name="novo_projeto"),
    path("responsaveis/novo/", views.novo_responsavel, name="novo_responsavel"),
    path("clientes/novo/", views.novo_cliente, name="novo_cliente"),
]