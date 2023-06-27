from django.db import models

# Create your models here.

class Stock(models.Model):
    code = models.CharField(max_length=6, unique=True, help_text='Código de 4 letras maiúsculas seguidas de 1 ou 2 números.')
    name = models.CharField(max_length=35)
    cnpj = models.CharField(max_length=18, unique=True, help_text='Deve conter apenas números.')

    def __str__(self):
        return self.code

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
        return f"{self.date} - {self.stock.code}"

    def calculo_total(self):
        taxa = self.corretagem + self.stock.b3_fees
        if self.operation == 'C':
            return self.quantidade * self.preco_unitario + taxa
        elif self.operation == 'V':
            return self.quantidade * self.preco_unitario - taxa

    def calculo_preco_medio(self):
        transacoes_anteriores = Transaction.objects.filter(
            stock=self.stock,
            investor=self.investor,
            date_lt=self.date,
            operation='C'
        )
        total_quantidade = transacoes_anteriores.aggregate(models.Sum('quantidade'))['quantidade_sum']
        preco_medio_anteriores = transacoes_anteriores.aggregate(models.Sum('quantidade', models.F('quantidade') * models.F('preco_unitario')))['quantidade_sum']
        return (preco_medio_anteriores + self.calculo_total()) / (total_quantidade + self.quantidade)

    def calculo_lucro_prejuizo(self):
        if self.operation == 'V':
            preco_medio = self.calculo_preco_medio()
            return self.calculo_total() - (self.quantidade * preco_medio)
        return 0

