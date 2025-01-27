from django import forms

class TransferForm(forms.Form):
    sender_account = forms.CharField(max_length=20)
    recipient_account = forms.CharField(max_length=20)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
