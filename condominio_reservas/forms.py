from django import forms
from .models import Morador, AreaComum, Reserva
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
            field.required = True
            
    def clean_first_name(self):
        nome = self.cleaned_data.get('first_name')
        if not nome or not nome.strip():
            raise forms.ValidationError("O nome não pode ficar em branco.")
        return nome
            

class FormularioAlterarSenha(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-2'
            field.widget.render_value = True
        
        self.fields['old_password'].label = 'Senha Atual'
        self.fields['new_password1'].label = 'Nova Senha'
        self.fields['new_password2'].label = 'Confirme a Nova Senha'
        
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['dataReserva', 'horarioInicio', 'horarioFim']
        labels = {
            'dataReserva': 'Data da Reserva',
            'horarioInicio': 'Horário de Início',
            'horarioFim': 'Horário de Término',
        }
        widgets = {
            'dataReserva': forms.DateInput(attrs={'type': 'date', 'class': 'form-control mb-3'}),
            'horarioInicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control mb-3'}),
            'horarioFim': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control mb-3'}),
        }
        

class LocalForm(forms.ModelForm):
    class Meta:
        model = AreaComum
        fields = ['nome', 'capacidade', 'prazoCancelamentoDias', 'tempoDaReserva', 'statusLocal']
        labels = {
            'nome': 'Nome do Local (Ex: Salão de Festas)',
            'capacidade': 'Capacidade Máxima (Pessoas)',
            'prazoCancelamentoDias': 'Prazo para Cancelamento (Dias)',
            'tempoDaReserva': 'Tempo máximo da reserva (Horas)',
            'statusLocal': 'Status Atual',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-3'
            
        self.fields['capacidade'].widget.attrs['min'] = '1'
        self.fields['prazoCancelamentoDias'].widget.attrs['min'] = '0'
        self.fields['tempoDaReserva'].widget.attrs['min'] = '1'

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        areas_existentes = AreaComum.objects.filter(nome__iexact=nome)
        
        if self.instance and self.instance.pk:
            areas_existentes = areas_existentes.exclude(pk=self.instance.pk)
            
        if areas_existentes.exists():
            raise forms.ValidationError('Já existe uma área comum cadastrada com este nome.')
        return nome

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('capacidade', 0) < 1:
            self.add_error('capacidade', 'A capacidade deve ser de pelo menos 1 pessoa.')
        if cleaned_data.get('prazoCancelamentoDias', 0) < 0:
            self.add_error('prazoCancelamentoDias', 'O prazo não pode ser negativo.')
        if cleaned_data.get('tempoDaReserva', 0) < 1:
            self.add_error('tempoDaReserva', 'O tempo de reserva deve ser no mínimo 1 hora.')
        return cleaned_data