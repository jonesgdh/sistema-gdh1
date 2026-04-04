from django.contrib import admin
from .models import Mensagem


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('remetente', 'destinatario', 'data_envio', 'lida')
    list_filter = ('lida', 'data_envio')
    search_fields = ('remetente__username', 'destinatario__username', 'texto')