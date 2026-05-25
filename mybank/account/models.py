from django.db import models
import random
import uuid
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, AbstractUser, Group, Permission

def generate_unique_account_number():
    while True:
        account_number = str(random.randint(1015000000000000, 1015999999999999))
        if not BankAccount.objects.filter(account_number=account_number).exists():
            return account_number

def validate_identification_numbers(instance):
    if not (instance.aadhar_number or instance.passport_number or instance.voter_id_number or instance.pan_card_number):
        raise ValidationError('At least one identification number must be provided.')


class CustomUser(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text=('The groups this user belongs to.'),
        verbose_name=('groups'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )

    def __str__(self):
        return self.username


class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    account_number = models.CharField(max_length=16, unique=True, default=generate_unique_account_number, editable=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_frozen = models.BooleanField(default=False)
    account_holder_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    current_address = models.TextField(default="")
    Permanent_Address = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, default=None)
    annual_income = models.IntegerField(default=0)
    occupation = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, default="India")
    state = models.CharField(max_length=50, default="kerala")
    city = models.CharField(max_length=50, default="delhi")
    street = models.CharField(max_length=50, default="main lane")
    pincode = models.IntegerField(default=123456)
    phone_number = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex='^\d{10}$',
                message='Phone number must be exactly 10 digits',
                code='invalid_phone_number'
            ),
        ],
    )
    email = models.EmailField(max_length=100, blank=True)
    aadhar_number = models.CharField(
        max_length=12,
        blank=True,
        validators=[
            RegexValidator(
                regex='^\d{12}$',
                message='Aadhar number must be exactly 12 digits',
                code='invalid_aadhar_number'
            ),
        ],
    )
    passport_number = models.CharField(
        max_length=9,
        blank=True,
        validators=[
            RegexValidator(
                regex='^[A-PR-WYa-pr-wy][1-9]\d\s?\d{4}[1-9]$',
                message='Invalid passport number',
                code='invalid_passport_number'
            ),
        ],
    )
    voter_id_number = models.CharField(
        max_length=10,
        blank=True,
        validators=[
            RegexValidator(
                regex='^[A-Z]{3}[0-9]{7}$',
                message='Voter ID number must be 3 letters followed by 7 digits',
                code='invalid_voter_id_number'
            ),
        ],
    )
    pan_card_number = models.CharField(
        max_length=10,
        blank=True,
        validators=[
            RegexValidator(
                regex='^[A-Z]{5}[0-9]{4}[A-Z]$',
                message='PAN card number must be 5 letters followed by 4 digits and 1 letter',
                code='invalid_pan_card_number'
            ),
        ],
    )
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    transaction_pin = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_holder_name} ({self.account_number})"

    def clean(self):
        validate_identification_numbers(self)


class BankAccountminor(models.Model):
    account_number = models.CharField(max_length=16, unique=True, default=generate_unique_account_number, editable=False)
    account_holder_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    current_address = models.TextField(default="")
    Permanent_Address = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, default=None)
    annual_income = models.IntegerField(default=0)
    occupation = models.CharField(max_length=50, default=None, null=True)
    country = models.CharField(max_length=50, default="India")
    state = models.CharField(max_length=50, default="kerala")
    city = models.CharField(max_length=50, default="delhi")
    street = models.CharField(max_length=50, default="main lane")
    pincode = models.IntegerField(default=123456)
    phone_number = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex='^\d{10}$',
                message='Phone number must be between 10 and 15 digits',
                code='invalid_phone_number'
            ),
        ],
    )
    email = models.EmailField(max_length=100, blank=True)
    aadhar_number = models.CharField(
        max_length=12,
        blank=True,
        validators=[
            RegexValidator(
                regex='^\d{12}$',
                message='Aadhar number must be exactly 12 digits',
                code='invalid_aadhar_number'
            ),
        ],
    )
    passport_number = models.CharField(
        max_length=9,
        blank=True,
        validators=[
            RegexValidator(
                regex='^[A-PR-WYa-pr-wy][1-9]\d\s?\d{4}[1-9]$',
                message='Invalid passport number',
                code='invalid_passport_number'
            ),
        ],
    )
    voter_id_number = models.CharField(
        max_length=10,
        blank=True,
        validators=[
            RegexValidator(
                regex='^[A-Z]{3}[0-9]{7}$',
                message='Voter ID number must be 3 letters followed by 7 digits',
                code='invalid_voter_id_number'
            ),
        ],
    )
    pan_card_number = models.CharField(
        max_length=10,
        blank=True,
        validators=[
            RegexValidator(
                regex='^[A-Z]{5}[0-9]{4}[A-Z]$',
                message='PAN card number must be 5 letters followed by 4 digits and 1 letter',
                code='invalid_pan_card_number'
            ),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_holder_name} ({self.account_number})"

    def clean(self):
        validate_identification_numbers(self)


class BankAccountsenior(models.Model):
    account_number = models.CharField(max_length=16, unique=True, default=generate_unique_account_number, editable=False)
    account_holder_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    current_address = models.TextField(default="")
    Permanent_Address = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, default=None)
    annual_income = models.IntegerField(default=0)
    occupation = models.CharField(max_length=50, default=None, null=True)
    country = models.CharField(max_length=50, default="India")
    state = models.CharField(max_length=50, default="kerala")
    city = models.CharField(max_length=50, default="delhi")
    street = models.CharField(max_length=50, default="main lane")
    pincode = models.IntegerField(default=123456)
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex='^\d{10,15}$',
                message='Phone number must be between 10 and 15 digits',
                code='invalid_phone_number'
            ),
        ],
    )
    email = models.EmailField(max_length=100, blank=True)
    aadhar_number = models.CharField(
        max_length=12,
        blank=True,
        validators=[
            RegexValidator(
                regex='^\d{12}$',
                message='Aadhar number must be exactly 12 digits',
                code='invalid_aadhar_number'
            ),
        ],
    )
    passport_number = models.CharField(
        max_length=9,
        blank=True,
        validators=[
            RegexValidator(
                regex='^[A-PR-WYa-pr-wy][1-9]\d\s?\d{4}[1-9]$',
                message='Invalid passport number',
                code='invalid_passport_number'
            ),
        ],
    )
    voter_id_number = models.CharField(
        max_length=10,
        blank=True,
        validators=[
            RegexValidator(
                regex='^[A-Z]{3}[0-9]{7}$',
                message='Voter ID number must be 3 letters followed by 7 digits',
                code='invalid_voter_id_number'
            ),
        ],
    )
    pan_card_number = models.CharField(
        max_length=10,
        blank=True,
        validators=[
            RegexValidator(
                regex='^[A-Z]{5}[0-9]{4}[A-Z]$',
                message='PAN card number must be 5 letters followed by 4 digits and 1 letter',
                code='invalid_pan_card_number'
            ),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_holder_name} ({self.account_number})"

    def clean(self):
        validate_identification_numbers(self)


class CardRequest(models.Model):
    CARD_TYPES = [('classic', 'Classic'), ('gold', 'Gold'), ('platinum', 'Platinum')]
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]

    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='card_requests')
    card_type = models.CharField(max_length=20, choices=CARD_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_cards')
    admin_note = models.TextField(blank=True)
    card_number = models.CharField(max_length=16, blank=True, null=True, unique=True)
    expiry_date = models.DateField(null=True, blank=True)
    cvv = models.CharField(max_length=200, blank=True)
    is_blocked = models.BooleanField(default=False)
    allow_international = models.BooleanField(default=True)
    allow_online = models.BooleanField(default=True)
    allow_contactless = models.BooleanField(default=True)

    class Meta:
        ordering = ['-requested_at']

    def __str__(self):
        return f"{self.bank_account.account_holder_name} - {self.card_type} ({self.status})"


class LoanApplication(models.Model):
    LOAN_TYPES = [
        ('personal', 'Personal Loan'),
        ('home', 'Home Loan'),
        ('car', 'Car Loan'),
        ('education', 'Education Loan'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='loans')
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    tenure_months = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    purpose = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    monthly_emi = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    admin_note = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_loans')

    class Meta:
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.bank_account.account_holder_name} - {self.loan_type} ₹{self.amount} ({self.status})"


class FixedDeposit(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('matured', 'Matured'),
        ('closed', 'Closed'),
    ]
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='fixed_deposits')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    tenure_months = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)
    maturity_date = models.DateField()
    maturity_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.bank_account.account_holder_name} - FD ₹{self.amount} ({self.tenure_months}M)"


class SupportTicket(models.Model):
    CATEGORIES = [
        ('account', 'Account Issue'),
        ('transaction', 'Transaction Issue'),
        ('card', 'Card Issue'),
        ('loan', 'Loan Issue'),
        ('fd', 'Fixed Deposit Issue'),
        ('technical', 'Technical Problem'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets')
    ticket_number = models.CharField(max_length=12, unique=True)
    subject = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORIES, default='other')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.ticket_number}] {self.subject} ({self.status})"


class TicketMessage(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        role = 'Staff' if self.is_staff else 'User'
        return f"{self.ticket.ticket_number} — {role}: {self.body[:40]}"


class Notification(models.Model):
    TYPES = [
        ('transaction', 'Transaction'),
        ('loan', 'Loan'),
        ('fd', 'Fixed Deposit'),
        ('card', 'Card'),
        ('security', 'Security'),
        ('system', 'System'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPES, default='system')
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} — {self.title}"


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history', null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    failure_reason = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        status = 'Success' if self.success else 'Failed'
        username = self.user.username if self.user else 'Unknown'
        return f"{username} - {status} - {self.timestamp}"


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        status = 'Active' if self.is_active else 'Revoked'
        return f"{self.user.username} - {self.ip_address} - {status}"
