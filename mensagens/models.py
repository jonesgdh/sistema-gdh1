from django.db import models
from django.contrib.auth.models import User


class Mensagem(models.Model):
    remetente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mensagens_enviadas'
    )
    destinatario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mensagens_recebidas'
    )
    texto = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    class Meta:
        ordering = ['data_envio']

    def __str__(self):
        return f'{self.remetente} -> {self.destinatario}'