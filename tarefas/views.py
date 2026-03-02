from django.shortcuts import render, redirect
from .forms import TarefaForm, ProjetoForm, ResponsavelForm
from .models import Tarefa

def nova_tarefa(request):
    if request.method == "POST":
        form = TarefaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("lista_tarefas")
    else:
        form = TarefaForm()

    return render(request, "tarefas/nova_tarefa.html", {"form": form})


def lista_tarefas(request):
    tarefas = Tarefa.objects.select_related("projeto", "responsavel").order_by("-id")
    return render(request, "tarefas/lista_tarefas.html", {"tarefas": tarefas})


def novo_projeto(request):
    next_url = request.GET.get("next") or "/tarefas/nova/"

    if request.method == "POST":
        form = ProjetoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next_url)
    else:
        form = ProjetoForm()

    return render(request, "tarefas/novo_projeto.html", {"form": form, "next_url": next_url})


def novo_responsavel(request):
    next_url = request.GET.get("next") or "/tarefas/nova/"

    if request.method == "POST":
        form = ResponsavelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next_url)
    else:
        form = ResponsavelForm()

    return render(request, "tarefas/novo_responsavel.html", {"form": form, "next_url": next_url})