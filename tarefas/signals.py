from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import LogAuditoria


def obter_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    LogAuditoria.objects.create(
        usuario=user,
        nome_usuario=user.username,
        acao='login',
        modelo='Autenticacao',
        objeto_id=user.id,
        descricao='Usuário fez login no sistema',
        ip=obter_ip(request)
    )


@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    nome = user.username if user else 'Anônimo'
    user_id = user.id if user else None

    LogAuditoria.objects.create(
        usuario=user if user and user.is_authenticated else None,
        nome_usuario=nome,
        acao='logout',
        modelo='Autenticacao',
        objeto_id=user_id,
        descricao='Usuário fez logout do sistema',
        ip=obter_ip(request)
    )