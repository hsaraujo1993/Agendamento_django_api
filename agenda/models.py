from django.db import models

# Create your models here.


class Agendamento(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    data_horario = models.DateTimeField()
    cancelamento = models.BooleanField(default=False)


