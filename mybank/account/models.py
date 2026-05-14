from django.db import models
import random
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

    class Meta:
        ordering = ['-requested_at']

    def __str__(self):
        return f"{self.bank_account.account_holder_name} - {self.card_type} ({self.status})"
