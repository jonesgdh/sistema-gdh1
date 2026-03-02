from django.urls import path
from . import views

urlpatterns = [
    path("nova/", views.nova_tarefa, name="nova_tarefa"),
    path("", views.lista_tarefas, name="lista_tarefas"),
    path("projetos/novo/", views.novo_projeto, name="novo_projeto"),
    path("responsaveis/novo/", views.novo_responsavel, name="novo_responsavel"),
]