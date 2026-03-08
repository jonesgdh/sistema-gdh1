from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cliente, Servico, Despesa
from .forms import ClienteForm, ServicoForm, DespesaForm


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'listar_clientes.html', {'clientes': clientes})


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
def listar_servicos(request):
    servicos = Servico.objects.all().order_by('-id')
    return render(request, 'listar_servicos.html', {'servicos': servicos})


@login_required
def novo_servico(request):
    if request.method == 'POST':
        servico_form = ServicoForm(request.POST)
        if servico_form.is_valid():
            servico = servico_form.save()
            return redirect('detalhe_servico', servico_id=servico.id)
    else:
        servico_form = ServicoForm()

    return render(request, 'novo_servico.html', {
        'servico_form': servico_form
    })


@login_required
def detalhe_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)
    despesas = Despesa.objects.filter(servico=servico)

    if request.method == 'POST':
        despesa_form = DespesaForm(request.POST)
        if despesa_form.is_valid():
            despesa = despesa_form.save(commit=False)
            despesa.servico = servico
            despesa.save()
            return redirect('detalhe_servico', servico_id=servico.id)
    else:
        despesa_form = DespesaForm()

    return render(request, 'detalhe_servico.html', {
        'servico': servico,
        'despesas': despesas,
        'despesa_form': despesa_form
    })
    
def pesquisar_servicos(request):
    termo = request.GET.get('q', '')
    servicos = Servico.objects.all()

    if termo:
        servicos = servicos.filter(descricao__icontains=termo)

    return render(request, 'listar_servicos.html', {
        'servicos': servicos
    })