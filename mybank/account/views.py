from decimal import Decimal, InvalidOperation
from .serializers import BankAccountSerializer, BankAccountminorSerializer, BankAccountseniorSerializer, UserSerializer
from django.contrib.auth import authenticate,  login as django_login
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie
from rest_framework.decorators import api_view,permission_classes
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token
from email.mime.multipart import MIMEMultipart
from rest_framework.response import Response
from django.middleware.csrf import get_token
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.http import JsonResponse
from email.mime.text import MIMEText
from django.core.cache import cache
from .forms import EditProfileForm
from rest_framework import status
from django.conf import settings
from .models import BankAccount
from PIL import Image
import pytesseract
import logging
import smtplib
import random
import json
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal, InvalidOperation
from django.shortcuts import get_object_or_404
from .models import BankAccount
from rest_framework_simplejwt.tokens import AccessToken
from django.http import JsonResponse
import json
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from decimal import Decimal, InvalidOperation
import logging
from django.http import JsonResponse
from django.middleware.csrf import get_token
import logging
from decimal import Decimal, InvalidOperation
from rest_framework.response import Response
from transaction.models import  Transaction



logger = logging.getLogger(__name__)
def generate_otp():
    return random.randint(100000, 999999)
def send_otp_email(user_email, otp):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your OTP Code"
    msg["From"] = settings.EMAIL_HOST_USER
    msg["To"] = user_email
    text = f"Hi {user_email},\n\nYour OTP code is {otp}. It is valid for 10 minutes.\n\nBest regards,\nYour Team"
    html = f"""
    <html>
    <body>
        <p>Hi {user_email},</p>
        <p>Your OTP code is {otp}. It is valid for 10 minutes.</p>
        <p>Best regards,<br>Your Team</p>
    </body>
    </html>
    """
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    msg.attach(part1)
    msg.attach(part2)
    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.EMAIL_HOST_USER, user_email, msg.as_string())
        server.quit()
        print(f"OTP email sent to {user_email}")
    except Exception as e:
        print(f"Failed to send OTP email: {e}")
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])  
def register(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')
        account_number = request.data.get('account_number')
        if not email or not password or not account_number:
            return Response({'error': 'Email, password, and account number are required'}, status=status.HTTP_400_BAD_REQUEST)
        bank_account = BankAccount.objects.filter(account_number=account_number).first()
        if not bank_account:
            return Response({'error': 'The account number is not associated with any bank account'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'A user with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        bank_account.user = user
        bank_account.save()    
        otp = generate_otp()
        send_otp_email(user.email, otp)
        cache.set(f'otp_{user.email}', otp, timeout=600) 
        return Response({'message': 'Signup successful! Please check your email for the OTP.','isOTPSent': True}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny]) 
def verify_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    if not email or not otp:
        return JsonResponse({'error': 'Email and OTP are required.'}, status=400)
    cached_otp = cache.get(f'otp_{email}')
    if cached_otp and str(cached_otp) == str(otp):
        return JsonResponse({'message': 'OTP verified successfully!'})
    else:
        return JsonResponse({'error': 'Invalid OTP or OTP has expired.'}, status=400) 






@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)
            if user:
                django_login(request, user)

                token = AccessToken.for_user(user)

                response = JsonResponse({"message": "Login successful!"})

                response.set_cookie(
                    key='access_token',  
                    value=str(token), 
                    httponly=True,  
                    samesite='None', 
                    secure=True, 
                )

                response.set_cookie(
                    key='csrftoken', 
                    value=request.COOKIES.get('csrftoken'),
                    httponly=False, 
                    samesite='None',  
                    secure=True, 
                )
                
                response.set_cookie(
                    key='sessionid', 
                    value=request.COOKIES.get('sessionid'),
                    httponly=True,  
                    samesite='None',
                    secure=True,  
                )

                return response
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)






from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
def user_info(request):
    if request.user.is_authenticated:
        logger.info(f"Authenticated user: {request.user.username}")
        return Response({'username': request.user.username})
    else:
        logger.warning("User is not authenticated.")
        return Response({'error': 'Unauthorized'}, status=401)
    


@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


logger = logging.getLogger(__name__)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def send_money_view(request):
    sender_account_number = request.data.get('sender_account_number')
    recipient_account_number = request.data.get('recipient_account_number')
    amount = request.data.get('amount')
    
    if not sender_account_number or not recipient_account_number or not amount:
        return Response({'error': 'Sender account number, recipient account number, and amount are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        amount = Decimal(amount)
    except (ValueError, InvalidOperation):
        return Response({'error': 'Invalid amount.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        sender = get_object_or_404(BankAccount, account_number=sender_account_number)
        recipient = get_object_or_404(BankAccount, account_number=recipient_account_number)
        
        if sender.balance < amount:
            return Response({'error': 'Insufficient funds.'}, status=status.HTTP_400_BAD_REQUEST)
        
        sender.balance -= amount
        recipient.balance += amount
        sender.save()
        recipient.save()
        
        transaction = Transaction(sender=sender, receiver=recipient, amount=amount, status='Completed')
        transaction.save()
        
        return Response({'message': 'Transaction successful.'}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error during transaction: {e}")
        return Response({'error': 'Internal server error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)@api_view(['POST'])

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import BankAccountSerializer

class CreateBankAccountView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = BankAccountSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Bank account created successfully'}, status=status.HTTP_201_CREATED)
        else:
            # Print or log the errors for debugging
            print(serializer.errors)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def profile_view(request):
    user = request.user
    bank_account = get_object_or_404(BankAccount, user=user)
    return JsonResponse({
        'account_holder_name': bank_account.account_holder_name,
        'account_number': bank_account.account_number,
        'date_of_birth': bank_account.date_of_birth,
        'current_address': bank_account.current_address,
        'permanent_address': bank_account.Permanent_Address,
        'sex': bank_account.sex,
        'annual_income': bank_account.annual_income,
        'occupation': bank_account.occupation,
        'country': bank_account.country,
        'state': bank_account.state,
        'city': bank_account.city,
        'street': bank_account.street,
        'pincode': bank_account.pincode,
        'phone_number': bank_account.phone_number,
        'email': bank_account.email,
        'aadhar_number': bank_account.aadhar_number,
        'passport_number': bank_account.passport_number,
        'voter_id_number': bank_account.voter_id_number,
        'pan_card_number': bank_account.pan_card_number,
        'photo': bank_account.photo.url if bank_account.photo else None,
        'created_at': bank_account.created_at
    })
@csrf_exempt
@api_view(['PUT'])
def update_profile(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    bank_account = get_object_or_404(BankAccount, user=user)
    serializer = BankAccountSerializer(bank_account, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'message': 'Profile updated successfully'})
    return JsonResponse({'error': serializer.errors}, status=400)
@csrf_exempt
@api_view(['GET', 'POST'])
def edit_profile_view(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    bank_account = get_object_or_404(BankAccount, user=user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=bank_account)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Profile updated successfully'})
        return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'bank_account': {
        'account_holder_name': bank_account.account_holder_name,
        'account_number': bank_account.account_number,
        'date_of_birth': bank_account.date_of_birth,
        'current_address': bank_account.current_address,
        'permanent_address': bank_account.Permanent_Address,
        'sex': bank_account.sex,
        'annual_income': bank_account.annual_income,
        'occupation': bank_account.occupation,
        'country': bank_account.country,
        'state': bank_account.state,
        'city': bank_account.city,
        'street': bank_account.street,
        'pincode': bank_account.pincode,
        'phone_number': bank_account.phone_number,
        'email': bank_account.email,
        'aadhar_number': bank_account.aadhar_number,
        'passport_number': bank_account.passport_number,
        'voter_id_number': bank_account.voter_id_number,
        'pan_card_number': bank_account.pan_card_number,
        'photo': bank_account.photo.url if bank_account.photo else None,
        'created_at': bank_account.created_at
    }})
@method_decorator(csrf_exempt, name='dispatch')
class CreateBankAccount(APIView):
    def post(self, request):
        serializer = BankAccountSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            photo = validated_data.get('photo')
            aadhar_number = validated_data.get('aadhar_number')
            account_holder_name = validated_data.get('account_holder_name')
            if photo:
                try:
                    image = Image.open(photo)
                    extracted_text = pytesseract.image_to_string(image)
                    errors = []
                    if aadhar_number and aadhar_number not in extracted_text:
                        errors.append("Aadhar number does not match the one in the photo.")
                    if account_holder_name and account_holder_name not in extracted_text:
                        errors.append("Account holder name does not match the one in the photo.")
                    if errors:
                        return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    logger.error(f"Error processing image: {e}")
                    return Response({"error": "Error processing image."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"error": "Photo is required for verification"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CreateBankAccountForMinor(APIView):
    def post(self, request):
        serializer = BankAccountminorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CreateBankAccountForSenior(APIView):
    def post(self, request):
        serializer = BankAccountseniorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def balance_view(request):
    try:
        user = request.user
        bank_account = BankAccount.objects.get(user=user)
        balance = bank_account.balance

        return Response({'balance': str(balance)}, status=status.HTTP_200_OK)
    
    except BankAccount.DoesNotExist:
        return Response({'error': 'Bank account not found for the user'}, status=status.HTTP_404_NOT_FOUND)
    
    except AttributeError:
        return Response({'error': 'Balance attribute not found on the user model'}, status=status.HTTP_400_BAD_REQUEST)