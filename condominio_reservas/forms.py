from django import forms
from .models import Morador

class CadastroMoradorForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Morador
        fields = ['first_name', 'email', 'bloco', 'apartamento', 'senha']

    def save(self, commit=True):
        user = super().save(commit=False)
        
        user.set_password(self.cleaned_data['senha'])
        
        user.username = self.cleaned_data['email'] 
        
        user.statusConta = 'Pendente' 
        
        if commit:
            user.save()
        return user
    
class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Morador
        fields = ['first_name', 'email', 'bloco', 'apartamento']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'