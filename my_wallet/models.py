from django.db import models

# Create your models here.

class Stock(models.Model):
    code = models.CharField(max_length=6, unique=True, help_text='Código de 4 letras maiúsculas seguidas de 1 ou 2 números.')
    name = models.CharField(max_length=35)
    cnpj = models.CharField(max_length=18, unique=True, help_text='Deve conter apenas números.')

    def __str__(self):
        return f"{self.code} - {self.name}"

from django.contrib.auth.models import User
from django.utils import timezone

class Transaction(models.Model):
    OPERATION_CHOICES = (
        ('C', 'Compra'),
        ('V', 'Venda'),
    )

    date = models.DateField(default=timezone.now)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    operation = models.CharField(max_length=1, choices=OPERATION_CHOICES)
    corretagem = models.FloatField()
    investor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} - {self.stock.code} - {self.investor} - {self.operation}"

