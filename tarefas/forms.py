from django import forms
from .models import Cliente, Servico, Despesa


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'email', 'endereco']


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['cliente', 'descricao', 'data_servico', 'valor_cobrado']
        widgets = {
            'data_servico': forms.DateInput(attrs={'type': 'date'}),
        }


class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['descricao', 'valor']