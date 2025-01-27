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
