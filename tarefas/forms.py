from django import forms
from .models import Tarefa, Projeto, Responsavel

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ["titulo", "descricao", "projeto", "responsavel", "prazo", "foto"]
        widgets = {
            "prazo": forms.DateInput(attrs={"type": "date"}),
        }

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ["nome"]

class ResponsavelForm(forms.ModelForm):
    class Meta:
        model = Responsavel
        fields = ["nome", "username"]