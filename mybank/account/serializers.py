from .models import BankAccount, BankAccountminor, BankAccountsenior
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from rest_framework import serializers
from datetime import datetime ,date
import os

def generate_key():
    key = Fernet.generate_key()
    with open('encryption_key.key', 'wb') as file:
        file.write(key)

if __name__ == "__main__":
    generate_key()


def load_key_from_file():
    file_path = os.path.join(os.path.dirname(__file__), 'encryption_key.key')
    try:
        with open(file_path, 'rb') as file:
            key = file.read()
    except FileNotFoundError:
        raise FileNotFoundError("The file 'encryption_key.key' could not be found.")

    return key

def encrypt_data(data):
    key = load_key_from_file()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data):
    key = load_key_from_file()
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data

class UserSerializer(serializers.ModelSerializer):
    account_number = serializers.CharField(source='bankaccount.account_number', read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'],  
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['user', 'account_holder_name', 'date_of_birth', 'current_address', 'Permanent_Address', 'sex', 'annual_income', 'occupation', 'country', 'state', 'city', 'street', 'pincode', 'phone_number', 'email', 'aadhar_number', 'passport_number', 'voter_id_number', 'pan_card_number', 'photo']
        read_only_fields = ['account_number']

    def validate_date_of_birth(self, value):
        if value >= date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        
        return value



class BankAccountminorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccountminor
        fields = ['id', 'account_holder_name', 'date_of_birth','aadhar_number','passport_number','voter_id_number','pan_card_number','phone_number','email','created_at', 'account_number','current_address','Permanent_Address','sex','annual_income','occupation','country','state','city','street','pincode']
        read_only_fields = ['account_number']

    def validate_date_of_birth(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age <18:
            raise serializers.ValidationError("Not allowed to create an account as minor account. Please use major account.")
        return value

class BankAccountseniorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccountsenior
        fields = ['id', 'account_holder_name', 'date_of_birth','aadhar_number','passport_number','voter_id_number','pan_card_number','phone_number','email','created_at', 'account_number','current_address','Permanent_Address','sex','annual_income','occupation','country','state','city','street','pincode']
        read_only_fields = ['account_number']

    def validate_date_of_birth(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 65:
            raise serializers.ValidationError("Not allowed to create an account as senior account. Please use major account.")
        return value
