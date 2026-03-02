from django.contrib import admin
from .models import Projeto, Responsavel, Tarefa

admin.site.register(Projeto)
admin.site.register(Responsavel)
admin.site.register(Tarefa)