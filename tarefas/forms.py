from django import forms
from .models import Tarefa, Projeto, Responsavel, Cliente

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ["titulo", "descricao", "cliente", "projeto", "responsavel", "prazo", "foto"]
        widgets = {"prazo": forms.DateInput(attrs={"type": "date"})}

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ["nome"]

class ResponsavelForm(forms.ModelForm):
    class Meta:
        model = Responsavel
        fields = ["nome", "username", "telefone", "endereco"]  # se você já adicionou contato em Responsável

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "telefone", "endereco", "email"]