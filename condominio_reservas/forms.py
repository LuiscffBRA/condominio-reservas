import datetime
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
    dataFim_temp = forms.DateField(required=False)

    class Meta:
        model = Reserva
        fields = ['dataReserva', 'horarioInicio', 'horarioFim']

    def __init__(self, *args, **kwargs):
        self.area = kwargs.pop('area', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        data_reserva = cleaned_data.get('dataReserva')
        data_fim_temp = cleaned_data.get('dataFim_temp')
        inicio = cleaned_data.get('horarioInicio')
        fim = cleaned_data.get('horarioFim')

        if data_reserva and inicio and fim:
            inicio_dt = datetime.datetime.combine(data_reserva, inicio)
            
            if data_fim_temp and data_fim_temp != data_reserva:
                fim_dt = datetime.datetime.combine(data_fim_temp, fim)
            else:
                if fim <= inicio:
                    fim_dt = datetime.datetime.combine(data_reserva + datetime.timedelta(days=1), fim)
                else:
                    fim_dt = datetime.datetime.combine(data_reserva, fim)

            duracao_horas = (fim_dt - inicio_dt).total_seconds() / 3600.0
            if self.area and duracao_horas > self.area.tempoDaReserva:
                raise forms.ValidationError(f'Sua seleção dá {int(duracao_horas)} horas. O limite do local é de {self.area.tempoDaReserva} horas.')

            if self.area:
                current_date = data_reserva - datetime.timedelta(days=1)
                end_date_check = fim_dt.date()
                dates_to_check = []
                
                while current_date <= end_date_check:
                    dates_to_check.append(current_date)
                    current_date += datetime.timedelta(days=1)

                reservas_existentes = Reserva.objects.filter(
                    areaComum=self.area,
                    status='Aprovado',
                    dataReserva__in=dates_to_check
                )
                
                for r in reservas_existentes:
                    r_inicio = datetime.datetime.combine(r.dataReserva, r.horarioInicio)
                    if r.horarioFim <= r.horarioInicio:
                        r_fim = r_inicio + datetime.timedelta(days=1)
                        r_fim = r_fim.replace(hour=r.horarioFim.hour, minute=r.horarioFim.minute)
                    else:
                        r_fim = datetime.datetime.combine(r.dataReserva, r.horarioFim)
                    
                    # Se cruzou, bloqueia!
                    if inicio_dt < r_fim and fim_dt > r_inicio:
                        raise forms.ValidationError('Já existe uma reserva para este local nesse período. Verifique os blocos vermelhos no calendário.')
                    
        return cleaned_data


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