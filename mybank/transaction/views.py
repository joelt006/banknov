from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from transaction.serializers import TransactionSerializer
from django.shortcuts import get_object_or_404
from decimal import Decimal, InvalidOperation
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction as db_transaction
from account.models import BankAccount
from rest_framework import status
from .models import Transaction
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_money_view(request):
    user = request.user
    recipient_account_number = request.data.get('recipient_account_number')
    amount = request.data.get('amount')

    if not recipient_account_number or not amount:
        return Response(
            {'error': 'Recipient account number and amount are required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        amount = Decimal(amount)
        if amount <= 0:
            return Response(
                {'error': 'Amount must be greater than zero.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except (ValueError, InvalidOperation):
        return Response({'error': 'Invalid amount.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with db_transaction.atomic():
            try:
                sender = BankAccount.objects.select_for_update().get(user=user)
            except BankAccount.DoesNotExist:
                return Response(
                    {'error': 'Bank account not found for the user.'},
                    status=status.HTTP_404_NOT_FOUND,
                )

            try:
                recipient = BankAccount.objects.select_for_update().get(
                    account_number=recipient_account_number
                )
            except BankAccount.DoesNotExist:
                return Response(
                    {'error': 'Recipient bank account not found.'},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if sender.account_number == recipient.account_number:
                return Response(
                    {'error': 'Cannot transfer to the same account.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if sender.balance < amount:
                return Response({'error': 'Insufficient funds.'}, status=status.HTTP_400_BAD_REQUEST)

            sender.balance -= amount
            recipient.balance += amount
            sender.save()
            recipient.save()
            Transaction.objects.create(
                sender=sender, receiver=recipient, amount=amount, status='Completed'
            )

        return Response({'message': 'Transaction successful.'}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in send_money_view: {str(e)}")
        return Response(
            {'error': 'An error occurred during the transaction.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit_money(request):
    account_number = request.data.get('account_number')
    amount = request.data.get('amount')

    if not account_number or not amount:
        return Response(
            {'error': 'Account number and amount are required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        amount = Decimal(amount)
        if amount <= 0:
            return Response(
                {'error': 'Amount must be greater than zero.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except (ValueError, InvalidOperation):
        return Response({'error': 'Invalid amount.'}, status=status.HTTP_400_BAD_REQUEST)

    with db_transaction.atomic():
        account = get_object_or_404(BankAccount, account_number=account_number)
        account.balance += amount
        account.save()

    return Response(
        {'message': 'Deposit successful.', 'new_balance': str(account.balance)},
        status=status.HTTP_200_OK,
    )


class TransactionStatementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            transactions = (
                Transaction.objects.filter(sender__user=user)
                | Transaction.objects.filter(receiver__user=user)
            ).distinct().order_by('-date')

            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data, status=200)

        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)
