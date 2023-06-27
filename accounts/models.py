from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Investor(models.Model):
    PERFIL_CHOICES = (
        ('C', 'Conservador'),
        ('M', 'Moderado'),
        ('A', 'Arrojado'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    perfil_de_risco = models.CharField(max_length=1, choices=PERFIL_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.perfil_de_risco}"
