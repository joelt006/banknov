# from django.contrib import admin
# from .models import Transaction

# @admin.register(Transaction)
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ('sender', 'receiver', 'amount', 'status', 'date', 'TransactionType')
#     search_fields = ('sender__account_holder_name', 'receiver__account_holder_name', 'amount', 'status')
#     list_filter = ('status', 'TransactionType', 'date')