from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def get_admin_user_id():
    """
    Fetch the ID of the superuser. Returns None if no superuser exists or the database is uninitialized.
    """
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
        return admin_user.id if admin_user else None
    except Exception as e:
        return None


from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    sender = models.ForeignKey(
        'account.BankAccount',
        related_name='sent_transactions',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    receiver = models.ForeignKey(
        'account.BankAccount',
        related_name='received_transactions',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    status = models.CharField(max_length=20, default='PENDING')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    value_date = models.DateTimeField(auto_now=True)  # Updates on every save
    TransactionType = models.CharField(max_length=20, default='TRANSFER')

    @staticmethod
    def get_user_transactions(user):
        return Transaction.objects.filter(
            sender__user=user
        ) | Transaction.objects.filter(
            receiver__user=user
        )

    def __str__(self):
        return f"Transaction by {self.sender.user} for {self.amount} on {self.date}"


class Beneficiary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='beneficiaries')
    nickname = models.CharField(max_length=50)
    account_number = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nickname']
        unique_together = [['user', 'account_number']]

    def __str__(self):
        return f"{self.nickname} ({self.account_number})"


class ScheduledTransfer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scheduled_transfers')
    recipient_account_number = models.CharField(max_length=16)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    failure_reason = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_at']

    def __str__(self):
        return f"{self.user.username} → {self.recipient_account_number} ₹{self.amount}"
