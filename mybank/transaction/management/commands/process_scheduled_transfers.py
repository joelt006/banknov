from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction as db_transaction
from decimal import Decimal
from transaction.models import ScheduledTransfer, Transaction
from account.models import BankAccount
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Process pending scheduled transfers that are due'

    def handle(self, *args, **options):
        due = ScheduledTransfer.objects.filter(status='pending', scheduled_at__lte=timezone.now())
        processed = failed = 0

        for st in due:
            try:
                with db_transaction.atomic():
                    sender = BankAccount.objects.select_for_update().get(user=st.user)
                    recipient = BankAccount.objects.select_for_update().get(
                        account_number=st.recipient_account_number
                    )

                    if sender.is_frozen:
                        raise ValueError('Sender account is frozen.')
                    if sender.balance < st.amount:
                        raise ValueError('Insufficient funds.')

                    sender.balance -= st.amount
                    recipient.balance += st.amount
                    sender.save()
                    recipient.save()

                    Transaction.objects.create(
                        sender=sender,
                        receiver=recipient,
                        amount=st.amount,
                        status='Completed',
                        TransactionType='SCHEDULED',
                    )

                    st.status = 'processed'
                    st.save()
                    processed += 1

            except BankAccount.DoesNotExist:
                st.status = 'failed'
                st.failure_reason = 'Account not found.'
                st.save()
                failed += 1
            except Exception as e:
                st.status = 'failed'
                st.failure_reason = str(e)[:200]
                st.save()
                failed += 1
                logger.error(f"Scheduled transfer {st.id} failed: {e}")

        self.stdout.write(
            self.style.SUCCESS(f'Processed {processed} transfer(s), {failed} failed.')
        )
