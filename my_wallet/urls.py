from django.urls import path, include
from my_wallet.views import TransactionListView, TransactionRetrieveUpdateDestroyView, StockCreateView, StockListView, CalculoTotalView, CalculoPrecoMedioView, CalculoLucroPrejuizoView, TransactionListYearlyView, TransactionListMonthlyView

urlpatterns = [
    path('stocks/create/', StockCreateView.as_view(), name='stock-create'),
    path('stocks/', StockListView.as_view(), name='stock-list'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', TransactionRetrieveUpdateDestroyView.as_view(), name='transaction-detail'),
    path('transactions/<int:pk>/total/', CalculoTotalView.as_view(), name='transaction-total'),
    path('transactions/<int:pk>/medio/', CalculoPrecoMedioView.as_view(), name='transaction-medio'),
    path('transactions/<int:pk>/lp/', CalculoLucroPrejuizoView.as_view(), name='transaction-lucro-prejuizo'),
    path('transactions/yearly/', TransactionListYearlyView.as_view(), name='transaction-list-yearly'),
    path('transactions/monthly/', TransactionListMonthlyView.as_view(), name='transaction-list-monthly'),
]
