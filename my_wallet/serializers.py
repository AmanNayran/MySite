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

    def create(self, validated_data):
        stock_data = validated_data.pop('stock')
        stock = Stock.objects.get(code=stock_data['code'])
        validated_data['stock'] = stock
        return Transaction.objects.create(**validated_data)
