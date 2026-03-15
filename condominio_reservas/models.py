from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)
    statusConta = models.CharField(max_length=50, default="Pendente")

    class Meta:
        abstract = True

class Morador(Usuario):
    bloco = models.CharField(max_length=10)
    apartamento = models.CharField(max_length=10)

class Administrador(Usuario):
    pass

class Sindico(Administrador):
    pass

class AreaComum(models.Model):
    STATUS_CHOICES = [
        ('Disponivel', 'Disponível'),
        ('EmManutencao', 'Em Manutenção'),
        ('Ocupado', 'Ocupado'),
    ]
    nome = models.CharField(max_length=100)
    capacidade = models.IntegerField()
    prazoCancelamentoDias = models.IntegerField()
    tempoDaReserva = models.IntegerField(help_text="Tempo em horas")
    statusLocal = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Disponivel')

class Reserva(models.Model):
    dataReserva = models.DateField()
    horarioInicio = models.TimeField()
    horarioFim = models.TimeField()
    status = models.CharField(max_length=50, default="Pendente")
    
    morador = models.ForeignKey(Morador, on_delete=models.CASCADE)
    areaComum = models.ForeignKey(AreaComum, on_delete=models.CASCADE)