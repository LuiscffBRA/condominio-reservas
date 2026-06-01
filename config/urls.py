from django.contrib import admin
from django.urls import path
from condominio_reservas import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('meu-perfil/', views.perfil_view, name='perfil'),  
    
    path('', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('sair/', views.logout_view, name='logout'),
    
    path('morador/', views.home_morador, name='home_morador'),
    path('admin-home/', views.home_admin, name='home_admin'),
    path('sindico/', views.home_sindico, name='home_sindico'),
    
    path('usuarios/pendentes/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/aprovar/<int:id>/', views.aprovar_usuario, name='aprovar_usuario'),
    path('usuarios/negar/<int:id>/', views.negar_usuario, name='negar_usuario'),
    path('moradores/todos/', views.listar_todos_moradores, name='listar_todos_moradores'),
    path('meu-perfil/alterar-senha/', views.alterar_senha, name='alterar_senha'),
    
    path('alternar_status_morador/<int:id>/', views.alternar_status_morador, name='alternar_status_morador'),
    
    path('locais/', views.listar_locais, name='listar_locais'),
    path('locais/cadastrar/', views.cadastrar_local, name='cadastrar_local'),
    path('locais/editar/<int:id>/', views.editar_local, name='editar_local'),
    path('locais/deletar/<int:id>/', views.deletar_local, name='deletar_local'),
    path('locais/visualizar/<int:id>/', views.visualizar_local, name='visualizar_local'),
    
    path('reservar/<int:area_id>/', views.solicitar_reserva, name='solicitar_reserva'),
    path('reservar/cancelar/<int:id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('reservar/editar/<int:id>/', views.editar_reserva, name='editar_reserva'),
    
    path('sindico/reservas/alternar-pagamento/<int:id>/', views.alternar_pagamento_reserva, name='alternar_pagamento_reserva'),
    
    path('api/ocupacao/<int:area_id>/', views.buscar_ocupacao, name='buscar_ocupacao'),

    path('sindico/reservas/', views.listar_reservas, name='listar_reservas'),
]