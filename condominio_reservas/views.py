from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Morador
from .forms import CadastroMoradorForm, EditarPerfilForm

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = authenticate(request, email=email, password=senha)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('home_sindico')
            
            if user.statusConta == 'Pendente':
                messages.warning(request, 'Sua conta ainda está aguardando aprovação do Síndico.')
                return redirect('login')
            
            elif user.statusConta == 'Negado':
                messages.error(request, 'Seu cadastro foi negado. Procure a administração.')
                return redirect('login')
            
            else:
                login(request, user)
                if hasattr(user, 'sindico'):
                    return redirect('home_sindico')
                elif hasattr(user, 'administrador'):
                    return redirect('home_admin')
                else:
                    return redirect('home_morador')
        else:
            messages.error(request, 'Email ou senha incorretos.')

    return render(request, 'login.html')

def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroMoradorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Aguarde a aprovação.')
            return redirect('login')
    else:
        form = CadastroMoradorForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home_morador(request):
    return render(request, 'home_morador.html')

@login_required(login_url='login')
def home_admin(request):
    total_moradores = Morador.objects.filter(statusConta='Aprovado').count()
    return render(request, 'home_admin.html', {'total_moradores': total_moradores})

@login_required(login_url='login')
def home_sindico(request):
    total_moradores = Morador.objects.filter(statusConta='Aprovado').count()
    return render(request, 'home_sindico.html', {'total_moradores': total_moradores})

@login_required(login_url='login')
def listar_usuarios(request):
    usuarios_pendentes = Morador.objects.filter(statusConta='Pendente').exclude(is_superuser=True)
    return render(request, 'listar_usuarios.html', {'usuarios_pendentes': usuarios_pendentes})

@login_required(login_url='login')
def aprovar_usuario(request, id):
    morador = Morador.objects.get(id=id)
    morador.statusConta = 'Aprovado'
    morador.save()
    messages.success(request, f'Cadastro de {morador.first_name} APROVADO com sucesso!')
    return redirect('listar_usuarios')

@login_required(login_url='login')
def negar_usuario(request, id):
    morador = Morador.objects.get(id=id)
    morador.statusConta = 'Negado'
    morador.save()
    messages.error(request, f'Cadastro de {morador.first_name} NEGADO.')
    return redirect('listar_usuarios')

@login_required(login_url='login')
def perfil_view(request):
    try:
        morador_logado = request.user.morador
    except:
        morador_logado = request.user

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=morador_logado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = EditarPerfilForm(instance=morador_logado)

    return render(request, 'perfil.html', {'form': form})