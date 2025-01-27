from django import forms
from .models import BankAccount

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_holder_name', 'date_of_birth', 'current_address', 'Permanent_Address', 'sex', 'annual_income', 'occupation', 'country', 'state', 'city', 'street', 'pincode', 'phone_number', 'email', 'aadhar_number', 'passport_number', 'voter_id_number', 'pan_card_number']
