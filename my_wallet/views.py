from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Transaction, Stock
from .serializers import TransactionSerializer, StockSerializer
from django.views import View
from django.db.models import F, Sum
from datetime import datetime, timedelta

class StockListView(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class StockCreateView(generics.CreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stock = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response({'success': 'Stock created successfully'}, status=status.HTTP_201_CREATED, headers=headers)


class TransactionListView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        investor = self.request.user
        return Transaction.objects.filter(investor=investor).order_by('date')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(investor=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response({'success': 'Transaction created successfully'}, status=status.HTTP_201_CREATED, headers=headers)

class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(investor=self.request.user)


class CalculoTotalView(APIView):
    def get(self, request, pk):
        try:
            transaction = Transaction.objects.get(pk=pk, investor=request.user)
            corretagem = transaction.corretagem
            operation = transaction.operation
            quantidade = transaction.quantidade
            preco_unitario = transaction.preco_unitario

            # Calcular o preço total da negociação
            taxa = float(corretagem) + 0.0325
            if operation == 'C':
                total = float(quantidade) * float(preco_unitario) + taxa
            elif operation == 'V':
                total = float(quantidade) * float(preco_unitario) - taxa

            data = {
                'quantidade': quantidade,
                'preco_unitario': preco_unitario,
                'operation': operation,
                'corretagem': corretagem,
                'total': total
            }
            return Response(data)
        except Transaction.DoesNotExist:
            return Response(status=404)

class CalculoPrecoMedioView(APIView):
    def get(self, request, pk):
        try:
            transaction = Transaction.objects.get(pk=pk, investor=request.user)

            # Calcular o preço total da negociação
            corretagem = transaction.corretagem
            quantidade = transaction.quantidade
            preco_unitario = transaction.preco_unitario

            taxa = float(corretagem) + 0.0325
            total = float(quantidade) * float(preco_unitario) + taxa

            # Calcular o preço médio
            stock = transaction.stock
            date = transaction.date

            transacoes_anteriores = Transaction.objects.filter(
                stock=stock,
                date__lt=date,
                operation='C'
            )
            cont = transacoes_anteriores.aggregate(total_quantidade=Sum('quantidade'))['total_quantidade'] or 0
            pm = transacoes_anteriores.aggregate(total_preco_medio=Sum(F('quantidade') * F('preco_unitario')))['total_preco_medio'] or 0
            pm = (cont * pm + total) / (cont + quantidade)

            data = {
                'total': total,
                'quantidade': quantidade,
                'cont': cont,
                'preco_medio': pm,
            }

            return Response(data)

        except Transaction.DoesNotExist:
            return Response(status=404)

class CalculoLucroPrejuizoView(APIView):
    def get(self, request, pk):
        try:
            transaction = Transaction.objects.get(pk=pk, investor=request.user)

            # Calcular o preço total da negociação
            corretagem = transaction.corretagem
            quantidade = transaction.quantidade
            preco_unitario = transaction.preco_unitario

            taxa = float(corretagem) + 0.0325
            total = float(quantidade) * float(preco_unitario) + taxa
    
            # Obter o total de ações e o preço médio das transações anteriores
            stock = transaction.stock
            date = transaction.date

            transacoes_anteriores = Transaction.objects.filter(
                stock=stock,
                date__lt=date,
                operation='V'
            )
            cont = transacoes_anteriores.aggregate(total_quantidade=Sum('quantidade'))['total_quantidade'] or 0
            pm = transacoes_anteriores.aggregate(total_preco_medio=Sum(F('quantidade') * F('preco_unitario')))['total_preco_medio'] or 0
            
            # Calcular o lucro/prejuízo
            lp = total - (quantidade * pm)
            eh_lucro_prejuizo = ''

            if(lp > 0):
                eh_lucro_prejuizo = 'Lucro!'
            elif(lp < 0):
                eh_lucro_prejuizo = 'Prejuízo!'
            else:
                eh_lucro_prejuizo = '0 x 0!'
            
            data = {
                'lp': lp,
                'eh_lucro_prejuizo': eh_lucro_prejuizo,
            }

            return Response(data)

        except Transaction.DoesNotExist:
            return Response(status=404)

class TransactionListYearlyView(APIView):
    def get(self, request):
        investor = self.request.user
        
        # Obtem a data atual e calcula a data há um ano atrás
        current_date = datetime.now().date()
        one_year_ago = current_date - timedelta(days=365)

        # Filtra e lista as transações encontradas
        transactions = Transaction.objects.filter(investor=investor, date__gte=one_year_ago, date__lte=current_date)
        serializer = TransactionSerializer(transactions, many=True)

        return Response(serializer.data)

class TransactionListMonthlyView(APIView):
    def get(self, request):
        investor = self.request.user

        # Obter o mês e ano atuais
        current_month = datetime.now().month
        current_year = datetime.now().year

        # Filtra e lista as transações encontradas
        transactions = Transaction.objects.filter(investor=investor, date__month=current_month, date__year=current_year)
        serializer = TransactionSerializer(transactions, many=True)

        return Response(serializer.data)
