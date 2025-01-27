from .views import send_money_view,deposit_money,TransactionStatementView
from django.urls import path

urlpatterns = [
    path('send-money/', send_money_view, name='send_money'),
    path('deposit-money/', deposit_money, name='deposit-money'),
    path('statement/', TransactionStatementView.as_view(), name='TransactionStatementView'),

]
