from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Aprovado', 'Aprovado'),
        ('Negado', 'Negado'),
        ('Desabilitado', 'Desabilitado'),
    ]
    
    email = models.EmailField(unique=True)
    
    statusConta = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Pendente'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Morador(Usuario):
    bloco = models.CharField(max_length=10)
    apartamento = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Morador"
        verbose_name_plural = "Moradores"

class Administrador(Usuario):
    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"

class Sindico(Administrador):
    class Meta:
        verbose_name = "Sindico"
        verbose_name_plural = "Sindicos"

class AreaComum(models.Model):
    STATUS_CHOICES = [
        ('Disponivel', 'Disponivel'),
        ('EmManutencao', 'Em Manutencao'),
    ]
    nome = models.CharField(max_length=100, unique=True)
    capacidade = models.IntegerField()
    prazoCancelamentoDias = models.IntegerField()
    tempoDaReserva = models.IntegerField()
    statusLocal = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Disponivel')

class Reserva(models.Model):
    dataReserva = models.DateField()
    horarioInicio = models.TimeField()
    horarioFim = models.TimeField()
    status = models.CharField(max_length=50, default="Pendente")
    pago = models.BooleanField(default=False)
    
    morador = models.ForeignKey(Morador, on_delete=models.CASCADE)
    areaComum = models.ForeignKey(AreaComum, on_delete=models.CASCADE)