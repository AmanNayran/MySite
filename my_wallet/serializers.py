from rest_framework import serializers
from .models import Stock, Transaction

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['code', 'name', 'cnpj']

class TransactionSerializer(serializers.ModelSerializer):
    stock = StockSerializer()

    class Meta:
        model = Transaction
        fields = ['id', 'date', 'stock', 'quantidade', 'preco_unitario', 'operation', 'corretagem', 'investor']

