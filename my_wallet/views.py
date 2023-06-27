from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionListView(generics.ListCreateAPIView):

    def get_queryset(self):
        investor = self.request.user
        return Transaction.objects.filter(investor=investor).order_by('date')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(investor=request.user)
        return Response(serializer.data, status=201)

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
