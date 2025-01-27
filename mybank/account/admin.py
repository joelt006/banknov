from django.contrib import admin
from .models import BankAccount, BankAccountminor, BankAccountsenior

admin.site.register(BankAccount)
admin.site.register(BankAccountminor)
admin.site.register(BankAccountsenior)



# from django.contrib import admin
# from .models import CustomUser, BankAccount, BankAccountminor, BankAccountsenior

# @admin.register(CustomUser)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'is_staff', 'is_active')
#     search_fields = ('username', 'email')
#     list_filter = ('is_staff', 'is_active')

# @admin.register(BankAccount)
# class BankAccountAdmin(admin.ModelAdmin):
#     list_display = ('account_number', 'account_holder_name', 'balance')
#     search_fields = ('account_number', 'account_holder_name')
#     list_filter = ('balance',)

# @admin.register(BankAccountminor)
# class BankAccountminorAdmin(admin.ModelAdmin):
#     list_display = ('account_number', 'account_holder_name', 'balance')
#     search_fields = ('account_number', 'account_holder_name')
#     list_filter = ('balance',)

# @admin.register(BankAccountsenior)
# class BankAccountseniorAdmin(admin.ModelAdmin):
#     list_display = ('account_number', 'account_holder_name', 'balance')
#     search_fields = ('account_number', 'account_holder_name')
#     list_filter = ('balance',)
