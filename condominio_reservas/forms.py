from django import forms
from .models import Morador
from django.contrib.auth.forms import PasswordChangeForm

class CadastroMoradorForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput())
    confirmar_senha = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Morador
        fields = ['first_name', 'email', 'bloco', 'apartamento']

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        if senha and len(senha) < 8:
            self.add_error('senha', 'A senha deve ter no mínimo 8 caracteres.')

        if senha and confirmar_senha and senha != confirmar_senha:
            self.add_error('confirmar_senha', 'As senhas não coincidem.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['senha'])
        user.statusConta = 'Pendente' 
        
        # AQUI ESTÁ A MÁGICA: O username obrigatoriamente recebe o e-mail
        user.username = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user


class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Morador
        fields = ['first_name', 'email']
        labels = {
            'first_name': 'Nome',
            'email': 'E-mail',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
class FormularioAlterarSenha(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-2'
        
        # Força os nomes em português
        self.fields['old_password'].label = 'Senha Atual'
        self.fields['new_password1'].label = 'Nova Senha'
        self.fields['new_password2'].label = 'Confirme a Nova Senha'