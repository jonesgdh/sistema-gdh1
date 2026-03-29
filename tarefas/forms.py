from django import forms
from .models import Cliente, Servico, Despesa



from django import forms
from .models import Cliente, Servico, Despesa

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'email', 'endereco', 'documento', 'observacoes']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['cliente', 'descricao', 'data_servico', 'valor_cobrado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data_servico': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor_cobrado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }



class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['descricao', 'valor']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }