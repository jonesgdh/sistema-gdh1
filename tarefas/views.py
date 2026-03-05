from django.shortcuts import render, redirect
from .forms import TarefaForm, ProjetoForm, ResponsavelForm, ClienteForm
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

def novo_cliente(request):
    next_url = request.GET.get("next") or "/tarefas/nova/"

    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next_url)
    else:
        form = ClienteForm()

    return render(request, "tarefas/novo_cliente.html", {"form": form, "next_url": next_url})

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

def index(request):
    return render(request, "tarefas/index.html")

def pesquisar_tarefas(request):
    q = (request.GET.get("q") or "").strip()

    tarefas = Tarefa.objects.select_related("projeto", "responsavel").order_by("-id")
    if q:
        tarefas = tarefas.filter(
    Q(titulo__icontains=q) |
    Q(descricao__icontains=q) |
    Q(cliente__nome__icontains=q) |
    Q(cliente__telefone__icontains=q) |
    Q(cliente__endereco__icontains=q) |
    Q(projeto__nome__icontains=q) |
    Q(responsavel__nome__icontains=q)
)

    return render(request, "tarefas/pesquisar_tarefas.html", {"tarefas": tarefas, "q": q})