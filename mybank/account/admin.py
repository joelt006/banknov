from django.contrib import admin
from .models import BankAccount, BankAccountminor, BankAccountsenior


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'account_holder_name', 'balance', 'phone_number', 'email', 'city', 'country', 'created_at')
    search_fields = ('account_number', 'account_holder_name', 'email', 'phone_number', 'aadhar_number', 'pan_card_number')
    list_filter = ('country', 'sex', 'created_at')
    readonly_fields = ('account_number', 'created_at')
    ordering = ('-created_at',)
    fieldsets = (
        ('Account', {'fields': ('account_number', 'balance', 'user')}),
        ('Personal', {'fields': ('account_holder_name', 'date_of_birth', 'sex', 'occupation', 'annual_income', 'photo')}),
        ('Address', {'fields': ('current_address', 'Permanent_Address', 'country', 'state', 'city', 'street', 'pincode')}),
        ('Contact', {'fields': ('phone_number', 'email')}),
        ('ID Documents', {'fields': ('aadhar_number', 'pan_card_number', 'voter_id_number', 'passport_number')}),
        ('Meta', {'fields': ('created_at',)}),
    )


@admin.register(BankAccountminor)
class BankAccountminorAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'account_holder_name', 'phone_number', 'city', 'country', 'created_at')
    search_fields = ('account_number', 'account_holder_name', 'email', 'phone_number')
    list_filter = ('country', 'sex')
    readonly_fields = ('account_number', 'created_at')


@admin.register(BankAccountsenior)
class BankAccountseniorAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'account_holder_name', 'phone_number', 'email', 'city', 'country', 'created_at')
    search_fields = ('account_number', 'account_holder_name', 'email', 'phone_number')
    list_filter = ('country', 'sex')
    readonly_fields = ('account_number', 'created_at')
