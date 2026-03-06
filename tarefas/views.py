from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cliente, Servico
from .forms import ClienteForm, ServicoForm


@login_required
def index(request):
    total_clientes = Cliente.objects.count()
    total_servicos = Servico.objects.count()

    contexto = {
        'total_clientes': total_clientes,
        'total_servicos': total_servicos,
    }

    return render(request, 'index.html', contexto)


@login_required
def novo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()

    return render(request, 'novo_cliente.html', {'form': form})


@login_required
def listar_clientes(request):
    clientes = Cliente.objects.all().order_by('-id')
    return render(request, 'listar_clientes.html', {'clientes': clientes})


@login_required
def novo_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_servicos')
    else:
        form = ServicoForm()

    return render(request, 'novo_servico.html', {'form': form})


@login_required
def listar_servicos(request):
    servicos = Servico.objects.select_related('cliente').all().order_by('-id')
    return render(request, 'listar_servicos.html', {'servicos': servicos})