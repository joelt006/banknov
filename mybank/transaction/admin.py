from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'amount', 'status', 'TransactionType', 'date')
    search_fields = ('sender__account_holder_name', 'receiver__account_holder_name', 'sender__account_number', 'receiver__account_number')
    list_filter = ('status', 'TransactionType', 'date')
    readonly_fields = ('date',)
    ordering = ('-date',)