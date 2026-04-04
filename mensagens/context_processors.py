from .models import Mensagem


def total_mensagens(request):
    if request.user.is_authenticated:
        total = Mensagem.objects.filter(
            destinatario=request.user,
            lida=False
        ).count()
    else:
        total = 0

    return {
        'total_mensagens': total
    }