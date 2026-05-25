from django.urls import path
from .views import (
    send_money_view, deposit_money, TransactionStatementView,
    beneficiaries_view, beneficiary_detail_view,
    scheduled_transfers_view, scheduled_transfer_detail_view,
)

urlpatterns = [
    path('send-money/', send_money_view, name='send_money'),
    path('deposit-money/', deposit_money, name='deposit-money'),
    path('statement/', TransactionStatementView.as_view(), name='TransactionStatementView'),
    path('beneficiaries/', beneficiaries_view, name='beneficiaries'),
    path('beneficiaries/<int:pk>/', beneficiary_detail_view, name='beneficiary_detail'),
    path('scheduled/', scheduled_transfers_view, name='scheduled_transfers'),
    path('scheduled/<int:pk>/', scheduled_transfer_detail_view, name='scheduled_transfer_detail'),
]
