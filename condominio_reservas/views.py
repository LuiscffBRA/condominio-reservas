from django.shortcuts import render

def login_view(request):
    return render(request, 'login.html')

def home_morador(request):
    return render(request, 'home_morador.html')

def home_admin(request):
    return render(request, 'home_admin.html')

def home_sindico(request):
    return render(request, 'home_sindico.html')