from django.urls import path, include
from my_wallet.views import TransactionListView, TransactionDetailView

urlpatterns = [
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
]

'''
urlpatterns = [
    path('accounts/wallet/', include([
        path('transactions/', TransactionListView.as_view(), name='transaction-list'),
        path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    ])),
]
'''