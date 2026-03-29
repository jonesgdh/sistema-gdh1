from decimal import Decimal
from .utils import get_ip

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Q, Value, DecimalField
from django.db.models.functions import Coalesce
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from openpyxl import Workbook

from .forms import ClienteForm, ServicoForm, DespesaForm
from .models import Cliente, Servico, Despesa, LogAuditoria


# =========================
# FUNÇÕES AUXILIARES
# =========================

def eh_administrador(user):
    return user.is_authenticated and user.is_superuser


def admin_required(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


def obter_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR', '0.0.0.0')


def registrar_log(request, usuario, acao, modelo, objeto_id, descricao=''):
    try:
        ip = obter_ip(request)
    except Exception:
        ip = '0.0.0.0'

    nome_usuario = 'Anônimo'
    usuario_obj = None

    if hasattr(usuario, 'is_authenticated') and usuario.is_authenticated:
        usuario_obj = usuario
        nome_usuario = usuario.username

    LogAuditoria.objects.create(
        usuario=usuario_obj,
        nome_usuario=nome_usuario,
        acao=acao,
        modelo=modelo,
        objeto_id=objeto_id,
        descricao=descricao,
        ip=ip
    )


def get_financeiro_queryset():
    return (
        Servico.objects
        .select_related('cliente')
        .annotate(
            despesa_total=Coalesce(
                Sum('despesas__valor'),
                Value(Decimal('0.00')),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )
        .order_by('-data_servico', '-id')
    )


# =========================
# AUDITORIA
# =========================

@login_required
@user_passes_test(admin_required)
def arquivo_auditoria(request):
    logs = LogAuditoria.objects.all().order_by('-data')
    return render(request, 'tarefas/arquivo_auditoria.html', {'logs': logs})

def get_ip(request):
    return request.META.get('REMOTE_ADDR')




# =========================
# DASHBOARD / INDEX
# =========================

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
    )['total'] or Decimal('0.00')

    total_despesas = Despesa.objects.aggregate(
        total=Sum('valor')
    )['total'] or Decimal('0.00')

    lucro = faturamento_total - total_despesas

    contexto = {
        'total_clientes': total_clientes,
        'total_servicos': total_servicos,
        'servicos_abertos': servicos_abertos,
        'servicos_andamento': servicos_andamento,
        'servicos_concluidos': servicos_concluidos,
        'servicos_entregues': servicos_entregues,
        'faturamento_total': faturamento_total,
        'total_despesas': total_despesas,
        'lucro': lucro,
    }

    return render(request, 'tarefas/index.html', contexto)


# =========================
# CLIENTES
# =========================

@login_required
def listar_clientes(request):
    clientes = Cliente.objects.all().order_by('nome')
    return render(request, 'tarefas/listar_clientes.html', {'clientes': clientes})


@login_required
def novo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()

            registrar_log(
                request,
                request.user,
                'criou',
                'Cliente',
                cliente.id,
                f'Criou o cliente: {cliente.nome}'
            )

            return redirect('tarefas:listar_clientes')
    else:
        form = ClienteForm()

    return render(request, 'tarefas/form_cliente.html', {
        'form': form,
        'titulo': 'Novo Cliente'
    })


@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()

            registrar_log(
                request,
                request.user,
                'alterou',
                'Cliente',
                cliente.id,
                f'Alterou o cliente: {cliente.nome}'
            )

            return redirect('tarefas:listar_clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'tarefas/form_cliente.html', {
        'form': form,
        'titulo': 'Editar Cliente'
    })


@login_required
def excluir_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        cliente_id_original = cliente.id
        cliente_nome = cliente.nome

        registrar_log(
            request,
            request.user,
            'deletou',
            'Cliente',
            cliente_id_original,
            f'Deletou o cliente: {cliente_nome}'
        )

        cliente.delete()
        return redirect('tarefas:listar_clientes')

    return render(request, 'tarefas/confirmar_exclusao.html', {
        'objeto': cliente,
        'tipo': 'cliente'
    })


# =========================
# SERVIÇOS
# =========================

@login_required
def listar_servicos(request):
    servicos = Servico.objects.select_related('cliente').all().order_by('-id')
    return render(request, 'tarefas/listar_servicos.html', {'servicos': servicos})


@login_required
def novo_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            servico = form.save()

            registrar_log(
                request,
                request.user,
                'criou',
                'Servico',
                servico.id,
                f'Criou o serviço #{servico.id} para o cliente {servico.cliente.nome}'
            )

            return redirect('tarefas:detalhe_servico', servico_id=servico.id)
    else:
        form = ServicoForm()

    return render(request, 'tarefas/form_servico.html', {
        'form': form,
        'titulo': 'Novo Serviço'
    })


@login_required
def editar_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)

    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            servico = form.save()

            registrar_log(
                request,
                request.user,
                'alterou',
                'Servico',
                servico.id,
                f'Alterou o serviço #{servico.id} do cliente {servico.cliente.nome}'
            )

            return redirect('tarefas:detalhe_servico', servico_id=servico.id)
    else:
        form = ServicoForm(instance=servico)

    return render(request, 'tarefas/form_servico.html', {
        'form': form,
        'titulo': f'Editar Serviço #{servico.id}',
        'editando': True,
        'servico': servico,
    })


@login_required
def excluir_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)

    if request.method == 'POST':
        servico_id_original = servico.id
        cliente_nome = servico.cliente.nome

        registrar_log(
            request,
            request.user,
            'deletou',
            'Servico',
            servico_id_original,
            f'Deletou o serviço #{servico_id_original} do cliente {cliente_nome}'
        )

        servico.delete()
        return redirect('tarefas:listar_servicos')

    return render(request, 'tarefas/confirmar_exclusao.html', {
        'objeto': servico,
        'tipo': 'servico'
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

            registrar_log(
                request,
                request.user,
                'criou',
                'Despesa',
                despesa.id,
                f'Criou a despesa "{despesa.descricao}" no serviço #{servico.id}'
            )

            return redirect('tarefas:detalhe_servico', servico_id=servico.id)
    else:
        despesa_form = DespesaForm()

    context = {
        'servico': servico,
        'despesas': despesas,
        'despesa_form': despesa_form,
        'total_despesas': servico.total_despesas(),
        'lucro': servico.lucro(),
    }

    return render(request, 'tarefas/detalhe_servico.html', context)


@login_required
def editar_despesa(request, despesa_id):
    despesa = get_object_or_404(Despesa, id=despesa_id)

    if request.method == 'POST':
        form = DespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            despesa = form.save()

            registrar_log(
                request,
                request.user,
                'alterou',
                'Despesa',
                despesa.id,
                f'Alterou a despesa "{despesa.descricao}" do serviço #{despesa.servico.id}'
            )

            return redirect('tarefas:detalhe_servico', servico_id=despesa.servico.id)
    else:
        form = DespesaForm(instance=despesa)

    return render(request, 'tarefas/editar_despesa.html', {
        'form': form,
        'despesa': despesa
    })


@login_required
def excluir_despesa(request, despesa_id):
    despesa = get_object_or_404(Despesa, id=despesa_id)
    servico_id = despesa.servico.id

    if request.method == 'POST':
        despesa_id_original = despesa.id
        descricao_despesa = despesa.descricao

        registrar_log(
            request,
            request.user,
            'deletou',
            'Despesa',
            despesa_id_original,
            f'Deletou a despesa "{descricao_despesa}" do serviço #{servico_id}'
        )

        despesa.delete()
        return redirect('tarefas:detalhe_servico', servico_id=servico_id)

    return render(request, 'tarefas/confirmar_exclusao.html', {
        'objeto': despesa,
        'tipo': 'despesa'
    })


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

    return render(request, 'tarefas/listar_servicos.html', {
        'servicos': servicos,
        'termo': termo,
        'status_selecionado': status,
    })


# =========================
# FINANCEIRO
# =========================

@login_required
def financeiro(request):
    servicos = get_financeiro_queryset()

    pesquisa_servico = request.GET.get('servico', '').strip()
    pesquisa_cliente = request.GET.get('cliente', '').strip()
    data_inicio = request.GET.get('data_inicio', '').strip()
    data_fim = request.GET.get('data_fim', '').strip()

    if pesquisa_servico:
        servicos = servicos.filter(
            Q(descricao__icontains=pesquisa_servico) |
            Q(equipamento__icontains=pesquisa_servico) |
            Q(marca__icontains=pesquisa_servico) |
            Q(modelo__icontains=pesquisa_servico) |
            Q(defeito_relatado__icontains=pesquisa_servico)
        )

    if pesquisa_cliente:
        servicos = servicos.filter(cliente__nome__icontains=pesquisa_cliente)

    if data_inicio:
        servicos = servicos.filter(data_servico__gte=data_inicio)

    if data_fim:
        servicos = servicos.filter(data_servico__lte=data_fim)

    lista_servicos = []
    total_recebido = Decimal('0.00')
    total_despesas = Decimal('0.00')
    total_em_aberto = Decimal('0.00')

    for servico in servicos:
        valor = servico.valor_cobrado or Decimal('0.00')
        despesa_total = servico.despesa_total or Decimal('0.00')
        servico.lucro_item = valor - despesa_total

        total_recebido += valor
        total_despesas += despesa_total

        if str(servico.status).lower() in ['aberto', 'em aberto', 'pendente']:
            total_em_aberto += valor

        lista_servicos.append(servico)

    lucro_total = total_recebido - total_despesas

    contexto = {
        'servicos': lista_servicos,
        'pesquisa_servico': pesquisa_servico,
        'pesquisa_cliente': pesquisa_cliente,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'total_servicos': len(lista_servicos),
        'total_recebido': total_recebido,
        'total_em_aberto': total_em_aberto,
        'total_despesas': total_despesas,
        'lucro_total': lucro_total,
    }

    return render(request, 'tarefas/financeiro.html', contexto)


@login_required
def exportar_financeiro_excel(request):
    servicos = get_financeiro_queryset()

    pesquisa_servico = request.GET.get('servico', '').strip()
    pesquisa_cliente = request.GET.get('cliente', '').strip()
    data_inicio = request.GET.get('data_inicio', '').strip()
    data_fim = request.GET.get('data_fim', '').strip()

    if pesquisa_servico:
        servicos = servicos.filter(
            Q(descricao__icontains=pesquisa_servico) |
            Q(equipamento__icontains=pesquisa_servico) |
            Q(marca__icontains=pesquisa_servico) |
            Q(modelo__icontains=pesquisa_servico) |
            Q(defeito_relatado__icontains=pesquisa_servico)
        )

    if pesquisa_cliente:
        servicos = servicos.filter(cliente__nome__icontains=pesquisa_cliente)

    if data_inicio:
        servicos = servicos.filter(data_servico__gte=data_inicio)

    if data_fim:
        servicos = servicos.filter(data_servico__lte=data_fim)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Financeiro'

    headers = [
        'Data',
        'Cliente',
        'Descrição',
        'Equipamento',
        'Marca',
        'Modelo',
        'Status',
        'Valor Cobrado',
        'Despesas',
        'Lucro',
    ]
    sheet.append(headers)

    for servico in servicos:
        valor = servico.valor_cobrado or Decimal('0.00')
        despesa_total = servico.despesa_total or Decimal('0.00')
        lucro = valor - despesa_total

        sheet.append([
            servico.data_servico.strftime('%d/%m/%Y') if servico.data_servico else '',
            servico.cliente.nome if servico.cliente else '',
            servico.descricao or '',
            servico.equipamento or '',
            servico.marca or '',
            servico.modelo or '',
            servico.status or '',
            float(valor),
            float(despesa_total),
            float(lucro),
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="financeiro.xlsx"'

    workbook.save(response)
    return response


# =========================
# LOGOUT
# =========================

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')