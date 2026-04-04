from django import forms
from django.contrib.auth.models import User
from .models import Mensagem


class MensagemForm(forms.ModelForm):
    destinatario = forms.ModelChoiceField(
        queryset=User.objects.none(),
        label='Destinatário',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    texto = forms.CharField(
        label='Mensagem',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Digite sua mensagem...'
        })
    )

    class Meta:
        model = Mensagem
        fields = ['destinatario', 'texto']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['destinatario'].queryset = User.objects.exclude(id=user.id)