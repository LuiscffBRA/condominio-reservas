from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import Morador
from .models import Morador, AreaComum
from .forms import CadastroMoradorForm, EditarPerfilForm, FormularioAlterarSenha, LocalForm

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or hasattr(request.user, 'sindico'):
            return redirect('home_sindico')
        elif hasattr(request.user, 'administrador'):
            return redirect('home_admin')
        else:
            return redirect('home_morador')

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
                messages.error(request, 'SEU CADASTRO FOI NEGADO. Procure a administração.', extra_tags='danger fw-bold')
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
            # Se a senha for fraca ou não coincidir, o form avisa
            for error in list(form.errors.values()):
                messages.error(request, error)
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
    messages.error(request, f'CADASTRO NEGADO: O acesso de {morador.first_name} foi recusado.', extra_tags='danger fw-bold')
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

@login_required(login_url='login')
def listar_todos_moradores(request):
    moradores = Morador.objects.filter(statusConta='Aprovado').exclude(is_superuser=True)
    return render(request, 'listar_todos.html', {'moradores': moradores})

@login_required(login_url='login')
def alterar_senha(request):
    if request.method == 'POST':
        old_pwd = request.POST.get('old_password')
        new_pwd = request.POST.get('new_password1')
        
        if old_pwd and new_pwd and old_pwd == new_pwd:
            if request.user.check_password(old_pwd):
                messages.warning(request, '⚠️ A nova senha não pode ser igual à sua senha atual!')
                form = FormularioAlterarSenha(request.user, request.POST)
                return render(request, 'alterar_senha.html', {'form': form})

        form = FormularioAlterarSenha(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('perfil')
        else:
            messages.error(request, 'Erro ao alterar a senha. Verifique os dados digitados.')
    else:
        form = FormularioAlterarSenha(request.user)
    
    return render(request, 'alterar_senha.html', {'form': form})

@login_required(login_url='login')
def listar_locais(request):
    locais = AreaComum.objects.all()
    return render(request, 'listar_locais.html', {'locais': locais})

@login_required(login_url='login')
def cadastrar_local(request):
    if request.method == 'POST':
        form = LocalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Área comum cadastrada com sucesso!')
            return redirect('listar_locais')
    else:
        form = LocalForm()
    return render(request, 'form_local.html', {'form': form, 'titulo': 'Cadastrar Novo Local'})

@login_required(login_url='login')
def editar_local(request, id):
    local = AreaComum.objects.get(id=id)
    if request.method == 'POST':
        form = LocalForm(request.POST, instance=local)
        if form.is_valid():
            form.save()
            messages.success(request, 'Área comum atualizada com sucesso!')
            return redirect('listar_locais')
    else:
        form = LocalForm(instance=local)
    return render(request, 'form_local.html', {'form': form, 'titulo': f'Editar Local: {local.nome}'})

@login_required(login_url='login')
def deletar_local(request, id):
    local = AreaComum.objects.get(id=id)
    local.delete()
    messages.success(request, 'Área comum excluída com sucesso!')
    return redirect('listar_locais')

@login_required(login_url='login')
def visualizar_local(request, id):
    local = AreaComum.objects.get(id=id)
    return render(request, 'visualizar_local.html', {'local': local})