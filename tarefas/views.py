from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q

from .models import Cliente, Servico, Despesa
from .forms import ClienteForm, ServicoForm, DespesaForm


@login_required
def index(request):
    total_clientes = Cliente.objects.count()
    total_servicos = Servico.objects.count()
    servicos_abertos = Servico.objects.filter(status='aberto').count()
    servicos_andamento = Servico.objects.filter(status='andamento').count()
    servicos_concluidos = Servico.objects.filter(status='concluido').count()
    servicos_entregues = Servico.objects.filter(status='entregue').count()

    faturamento_total = Servico.objects.aggregate(
        total=Sum('valor_cobrado')
    )['total'] or 0

    despesas_total = Despesa.objects.aggregate(
        total=Sum('valor')
    )['total'] or 0

    lucro_total = faturamento_total - despesas_total

    ultimos_servicos = Servico.objects.select_related('cliente').order_by('-id')[:5]

    context = {
        'total_clientes': total_clientes,
        'total_servicos': total_servicos,
        'servicos_abertos': servicos_abertos,
        'servicos_andamento': servicos_andamento,
        'servicos_concluidos': servicos_concluidos,
        'servicos_entregues': servicos_entregues,
        'faturamento_total': faturamento_total,
        'despesas_total': despesas_total,
        'lucro_total': lucro_total,
        'ultimos_servicos': ultimos_servicos,
    }

    return render(request, 'index.html', context)


@login_required
def listar_clientes(request):
    clientes = Cliente.objects.all().order_by('nome')
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
    servicos = Servico.objects.select_related('cliente').all().order_by('-id')
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
    despesas = Despesa.objects.filter(servico=servico).order_by('-id')

    if request.method == 'POST':
        despesa_form = DespesaForm(request.POST)
        if despesa_form.is_valid():
            despesa = despesa_form.save(commit=False)
            despesa.servico = servico
            despesa.save()
            return redirect('detalhe_servico', servico_id=servico.id)
    else:
        despesa_form = DespesaForm()

    context = {
        'servico': servico,
        'despesas': despesas,
        'despesa_form': despesa_form,
        'total_despesas': servico.total_despesas(),
        'lucro': servico.lucro(),
    }

    return render(request, 'detalhe_servico.html', context)


@login_required
def pesquisar_servicos(request):
    termo = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()

    servicos = Servico.objects.select_related('cliente').all().order_by('-id')

    if termo:
        servicos = servicos.filter(
            Q(descricao__icontains=termo) |
            Q(cliente__nome__icontains=termo) |
            Q(equipamento__icontains=termo) |
            Q(marca__icontains=termo) |
            Q(modelo__icontains=termo) |
            Q(defeito_relatado__icontains=termo) |
            Q(diagnostico__icontains=termo)
        )

    if status:
        servicos = servicos.filter(status=status)

    return render(request, 'listar_servicos.html', {
        'servicos': servicos,
        'termo': termo,
        'status_selecionado': status,
    })