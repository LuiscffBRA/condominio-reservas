"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from condominio_reservas import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rota do Meu Perfil
    path('meu-perfil/', views.perfil_view, name='perfil'),  
    
    # Rotas de Autenticação
    path('', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('sair/', views.logout_view, name='logout'),
    
    # Rotas dos Painéis
    path('morador/', views.home_morador, name='home_morador'),
    path('admin-home/', views.home_admin, name='home_admin'),
    path('sindico/', views.home_sindico, name='home_sindico'),
    
    # Rotas do Gerenciar Usuários
    path('usuarios/pendentes/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/aprovar/<int:id>/', views.aprovar_usuario, name='aprovar_usuario'),
    path('usuarios/negar/<int:id>/', views.negar_usuario, name='negar_usuario'),
    path('moradores/todos/', views.listar_todos_moradores, name='listar_todos_moradores'),
    path('meu-perfil/alterar-senha/', views.alterar_senha, name='alterar_senha'),
    
    # Rota de desabilitar e abilitar morador
    path('alternar_status_morador/<int:id>/', views.alternar_status_morador, name='alternar_status_morador'),
    
    # Rotas do Gerenciar Locais
    path('locais/', views.listar_locais, name='listar_locais'),
    path('locais/cadastrar/', views.cadastrar_local, name='cadastrar_local'),
    path('locais/editar/<int:id>/', views.editar_local, name='editar_local'),
    path('locais/deletar/<int:id>/', views.deletar_local, name='deletar_local'),
    path('locais/visualizar/<int:id>/', views.visualizar_local, name='visualizar_local'),
    
    # Solicitar Reserva
    path('reservar/<int:area_id>/', views.solicitar_reserva, name='solicitar_reserva'),
]