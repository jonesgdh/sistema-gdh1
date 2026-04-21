from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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

    entregue = models.BooleanField(default=False)
    lida = models.BooleanField(default=False)
    data_leitura = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['data_envio']

    def __str__(self):
        return f'{self.remetente} -> {self.destinatario}'