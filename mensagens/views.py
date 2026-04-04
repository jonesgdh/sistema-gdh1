from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MensagemForm
from .models import Mensagem


@login_required
def caixa_entrada(request):
    usuarios = User.objects.exclude(id=request.user.id)

    ultimas_conversas = []
    for usuario in usuarios:
        ultima = Mensagem.objects.filter(
            Q(remetente=request.user, destinatario=usuario) |
            Q(remetente=usuario, destinatario=request.user)
        ).order_by('-data_envio').first()

        nao_lidas = Mensagem.objects.filter(
            remetente=usuario,
            destinatario=request.user,
            lida=False
        ).count()

        if ultima:
            ultimas_conversas.append({
                'usuario': usuario,
                'ultima': ultima,
                'nao_lidas': nao_lidas,
            })

    ultimas_conversas.sort(
        key=lambda x: x['ultima'].data_envio if x['ultima'] else x['usuario'].username,
        reverse=True
    )

    form = MensagemForm(user=request.user)

    if request.method == 'POST':
        form = MensagemForm(request.POST, user=request.user)
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.remetente = request.user
            mensagem.save()
            return redirect('mensagens:conversa', user_id=mensagem.destinatario.id)

    return render(request, 'mensagens/caixa_entrada.html', {
        'conversas': ultimas_conversas,
        'form': form,
    })


@login_required
def conversa(request, user_id):
    outro_usuario = get_object_or_404(User, id=user_id)

    mensagens = Mensagem.objects.filter(
        Q(remetente=request.user, destinatario=outro_usuario) |
        Q(remetente=outro_usuario, destinatario=request.user)
    ).order_by('data_envio')

    Mensagem.objects.filter(
        remetente=outro_usuario,
        destinatario=request.user,
        lida=False
    ).update(lida=True)

    if request.method == 'POST':
        texto = request.POST.get('texto', '').strip()
        if texto:
            Mensagem.objects.create(
                remetente=request.user,
                destinatario=outro_usuario,
                texto=texto
            )
            return redirect('mensagens:conversa', user_id=outro_usuario.id)

    usuarios = User.objects.exclude(id=request.user.id)
    ultimas_conversas = []

    for usuario in usuarios:
        ultima = Mensagem.objects.filter(
            Q(remetente=request.user, destinatario=usuario) |
            Q(remetente=usuario, destinatario=request.user)
        ).order_by('-data_envio').first()

        nao_lidas = Mensagem.objects.filter(
            remetente=usuario,
            destinatario=request.user,
            lida=False
        ).count()

        if ultima:
            ultimas_conversas.append({
                'usuario': usuario,
                'ultima': ultima,
                'nao_lidas': nao_lidas,
            })

    ultimas_conversas.sort(
        key=lambda x: x['ultima'].data_envio if x['ultima'] else x['usuario'].username,
        reverse=True
    )

    return render(request, 'mensagens/conversa.html', {
        'outro_usuario': outro_usuario,
        'mensagens': mensagens,
        'conversas': ultimas_conversas,
    })