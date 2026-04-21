from django import forms
from .models import Cliente, Servico, Despesa
import re


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nome',
            'telefone',
            'email',
            'endereco',
            'documento',
            'observacoes',
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(13) 99999-9999',
                'maxlength': '15'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço completo'
            }),
            'documento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CPF ou CNPJ'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Observações (opcional)'
            }),
        }

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone', '')
        telefone = re.sub(r'\D', '', telefone)

        if not telefone:
            raise forms.ValidationError('Informe o telefone.')

        if len(telefone) < 10 or len(telefone) > 11:
            raise forms.ValidationError('O telefone deve ter 10 ou 11 números.')

        return telefone

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            raise forms.ValidationError('Informe o e-mail.')

        return email

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = [
            'cliente',
            'data_servico',
            'tipo_servico',
            'descricao',
            'valor_cobrado',
            'status',
            'documento',
            'imagem',
        ]
        widgets = {
            'data_servico': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'valor_cobrado': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cliente': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tipo_servico': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'documento': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'imagem': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
             
        }
class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['descricao', 'valor']