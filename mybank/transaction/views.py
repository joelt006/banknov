from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from transaction.serializers import TransactionSerializer
from django.shortcuts import get_object_or_404
from decimal import Decimal, InvalidOperation
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction as db_transaction
from django.contrib.auth.hashers import check_password as check_pw
from django.core.cache import cache
from django.utils import timezone
from account.models import BankAccount
from rest_framework import status
from .models import Transaction, Beneficiary, ScheduledTransfer
import logging


def _pin_rate_limit(key, max_attempts=3, window_seconds=300):
    attempts = cache.get(key, 0)
    if attempts >= max_attempts:
        return False
    cache.set(key, attempts + 1, timeout=window_seconds)
    return True

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_money_view(request):
    user = request.user
    recipient_account_number = request.data.get('recipient_account_number')
    amount = request.data.get('amount')

    transaction_pin = request.data.get('transaction_pin', '')
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

            if sender.is_frozen:
                return Response(
                    {'error': 'Your account is frozen. Please contact support.'},
                    status=status.HTTP_403_FORBIDDEN,
                )

            if not sender.transaction_pin:
                return Response(
                    {'error': 'Please set a transaction PIN in Security Settings before sending money.'},
                    status=status.HTTP_403_FORBIDDEN,
                )
            if not transaction_pin:
                return Response({'error': 'Transaction PIN is required.'}, status=status.HTTP_400_BAD_REQUEST)
            if not _pin_rate_limit(f'pin_{sender.account_number}'):
                return Response(
                    {'error': 'Too many incorrect PIN attempts. Try again in 5 minutes.'},
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )
            if not check_pw(transaction_pin, sender.transaction_pin):
                return Response({'error': 'Incorrect transaction PIN.'}, status=status.HTTP_400_BAD_REQUEST)

            if sender.balance < amount:
                return Response({'error': 'Insufficient funds.'}, status=status.HTTP_400_BAD_REQUEST)

            sender.balance -= amount
            recipient.balance += amount
            sender.save()
            recipient.save()
            Transaction.objects.create(
                sender=sender, receiver=recipient, amount=amount, status='Completed'
            )
            from account.models import Notification
            try:
                Notification.objects.create(
                    user=sender.user, title='Money Sent',
                    message=f'₹{float(amount):,.2f} sent to account ending {recipient.account_number[-4:]}.',
                    notification_type='transaction', link='/TransactionStatement',
                )
                if recipient.user:
                    Notification.objects.create(
                        user=recipient.user, title='Money Received',
                        message=f'₹{float(amount):,.2f} received from account ending {sender.account_number[-4:]}.',
                        notification_type='transaction', link='/TransactionStatement',
                    )
            except Exception:
                pass

        return Response({'message': 'Transaction successful.'}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in send_money_view: {str(e)}")
        return Response(
            {'error': 'An error occurred during the transaction.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(['POST'])
@permission_classes([IsAdminUser])
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
        try:
            account = BankAccount.objects.select_for_update().get(account_number=account_number)
        except BankAccount.DoesNotExist:
            return Response({'error': 'Account not found.'}, status=status.HTTP_404_NOT_FOUND)

        if account.is_frozen:
            return Response({'error': 'Cannot deposit to a frozen account.'}, status=status.HTTP_400_BAD_REQUEST)

        account.balance += amount
        account.save()

        Transaction.objects.create(
            sender=None,
            receiver=account,
            amount=amount,
            status='Completed',
            TransactionType='DEPOSIT',
        )

    return Response(
        {
            'message': 'Deposit successful.',
            'new_balance': str(account.balance),
            'account_holder': account.account_holder_name,
        },
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
            logger.error(f"TransactionStatementView error: {str(e)}")
            return Response({'error': 'Failed to retrieve transactions.'}, status=500)


# ── Beneficiaries ──────────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def beneficiaries_view(request):
    user = request.user
    if request.method == 'GET':
        items = Beneficiary.objects.filter(user=user)
        data = [{'id': b.id, 'nickname': b.nickname, 'account_number': b.account_number} for b in items]
        return Response(data)

    nickname = request.data.get('nickname', '').strip()
    account_number = request.data.get('account_number', '').strip()
    if not nickname or not account_number:
        return Response({'error': 'Nickname and account number are required.'}, status=400)
    if len(account_number) != 16 or not account_number.isdigit():
        return Response({'error': 'Account number must be exactly 16 digits.'}, status=400)
    if not BankAccount.objects.filter(account_number=account_number).exists():
        return Response({'error': 'Account not found.'}, status=404)
    try:
        own = BankAccount.objects.get(user=user)
        if own.account_number == account_number:
            return Response({'error': 'Cannot add your own account as beneficiary.'}, status=400)
    except BankAccount.DoesNotExist:
        pass
    if Beneficiary.objects.filter(user=user, account_number=account_number).exists():
        return Response({'error': 'This account is already in your beneficiaries.'}, status=400)
    b = Beneficiary.objects.create(user=user, nickname=nickname, account_number=account_number)
    return Response({'id': b.id, 'nickname': b.nickname, 'account_number': b.account_number}, status=201)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def beneficiary_detail_view(request, pk):
    try:
        b = Beneficiary.objects.get(pk=pk, user=request.user)
    except Beneficiary.DoesNotExist:
        return Response({'error': 'Beneficiary not found.'}, status=404)
    b.delete()
    return Response(status=204)


# ── Scheduled Transfers ────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def scheduled_transfers_view(request):
    user = request.user
    if request.method == 'GET':
        transfers = ScheduledTransfer.objects.filter(user=user)
        data = [{
            'id': t.id,
            'recipient_account_number': t.recipient_account_number,
            'amount': str(t.amount),
            'scheduled_at': t.scheduled_at.isoformat(),
            'status': t.status,
            'failure_reason': t.failure_reason,
            'created_at': t.created_at.isoformat(),
        } for t in transfers]
        return Response(data)

    # POST — create scheduled transfer
    recipient_account_number = request.data.get('recipient_account_number', '').strip()
    amount = request.data.get('amount')
    scheduled_at = request.data.get('scheduled_at')
    transaction_pin = request.data.get('transaction_pin', '')

    if not all([recipient_account_number, amount, scheduled_at]):
        return Response({'error': 'Recipient, amount, and scheduled_at are required.'}, status=400)

    try:
        amount = Decimal(str(amount))
        if amount <= 0:
            return Response({'error': 'Amount must be greater than zero.'}, status=400)
    except (ValueError, InvalidOperation):
        return Response({'error': 'Invalid amount.'}, status=400)

    try:
        from django.utils.dateparse import parse_datetime
        scheduled_dt = parse_datetime(scheduled_at)
        if not scheduled_dt:
            return Response({'error': 'Invalid date/time format.'}, status=400)
        if timezone.is_naive(scheduled_dt):
            scheduled_dt = timezone.make_aware(scheduled_dt)
        if scheduled_dt <= timezone.now():
            return Response({'error': 'Scheduled time must be in the future.'}, status=400)
    except Exception:
        return Response({'error': 'Invalid scheduled_at value.'}, status=400)

    try:
        sender = BankAccount.objects.get(user=user)
    except BankAccount.DoesNotExist:
        return Response({'error': 'Bank account not found.'}, status=404)

    if sender.is_frozen:
        return Response({'error': 'Your account is frozen. Please contact support.'}, status=403)
    if not BankAccount.objects.filter(account_number=recipient_account_number).exists():
        return Response({'error': 'Recipient account not found.'}, status=404)
    if sender.account_number == recipient_account_number:
        return Response({'error': 'Cannot transfer to the same account.'}, status=400)

    # Verify PIN at schedule time
    if not sender.transaction_pin:
        return Response({'error': 'Please set a transaction PIN in Security Settings first.'}, status=403)
    if not transaction_pin:
        return Response({'error': 'Transaction PIN is required to authorise the schedule.'}, status=400)
    if not _pin_rate_limit(f'pin_{sender.account_number}'):
        return Response({'error': 'Too many incorrect PIN attempts. Try again in 5 minutes.'}, status=429)
    if not check_pw(transaction_pin, sender.transaction_pin):
        return Response({'error': 'Incorrect transaction PIN.'}, status=400)

    st = ScheduledTransfer.objects.create(
        user=user,
        recipient_account_number=recipient_account_number,
        amount=amount,
        scheduled_at=scheduled_dt,
    )
    return Response({
        'id': st.id,
        'recipient_account_number': st.recipient_account_number,
        'amount': str(st.amount),
        'scheduled_at': st.scheduled_at.isoformat(),
        'status': st.status,
    }, status=201)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def scheduled_transfer_detail_view(request, pk):
    try:
        st = ScheduledTransfer.objects.get(pk=pk, user=request.user, status='pending')
    except ScheduledTransfer.DoesNotExist:
        return Response({'error': 'Scheduled transfer not found or already processed.'}, status=404)
    st.status = 'cancelled'
    st.save()
    return Response(status=204)
