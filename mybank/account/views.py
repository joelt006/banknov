from decimal import Decimal, InvalidOperation
from .serializers import BankAccountSerializer, BankAccountminorSerializer, BankAccountseniorSerializer, UserSerializer
from django.contrib.auth import authenticate,  login as django_login
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes, authentication_classes
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
from .models import BankAccount, CardRequest
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
@authentication_classes([])
@permission_classes([AllowAny])
def register(request):
    from django.db import transaction as db_tx
    email = request.data.get('email', '').strip()
    password = request.data.get('password', '')
    username = request.data.get('username', '').strip()
    account_number = request.data.get('account_number', '').strip()

    if not email or not password or not username or not account_number:
        return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    bank_account = BankAccount.objects.filter(account_number=account_number).first()
    if not bank_account:
        return Response({'error': 'Account number not found. Please create a bank account first.'}, status=status.HTTP_400_BAD_REQUEST)

    if bank_account.user_id is not None:
        return Response({'error': 'This bank account is already linked to another user.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'A user with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'This username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with db_tx.atomic():
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            bank_account.user = user
            bank_account.save()

        otp = generate_otp()
        send_otp_email(user.email, otp)
        cache.set(f'otp_{user.email}', otp, timeout=600)
        return Response({'message': 'Registration successful! Check your email for the OTP.', 'isOTPSent': True}, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f'Registration error: {e}')
        return Response({'error': 'Registration failed. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([])
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






# @csrf_exempt
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_view(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             username = data.get('username')
#             password = data.get('password')

#             user = authenticate(request, username=username, password=password)
#             if user:
#                 django_login(request, user)

#                 token = AccessToken.for_user(user)

#                 response = JsonResponse({"message": "Login successful!"})

#                 response.set_cookie(
#                     key='access_token',  
#                     value=str(token), 
#                     httponly=True,  
#                     samesite='None', 
#                     secure=True, 
#                 )

#                 response.set_cookie(
#                     key='csrftoken', 
#                     value=request.COOKIES.get('csrftoken'),
#                     httponly=False, 
#                     samesite='None',  
#                     secure=True, 
#                 )
                
#                 response.set_cookie(
#                     key='sessionid', 
#                     value=request.COOKIES.get('sessionid'),
#                     httponly=True,  
#                     samesite='None',
#                     secure=True,  
#                 )

#                 return response
#             else:
#                 return JsonResponse({'error': 'Invalid credentials'}, status=401)
#         except Exception as e:
#             return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)



@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
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
                return JsonResponse({"message": "Login successful!", "token": str(token)})
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)


from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = BankAccountSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            return Response({
                'message': 'Bank account created successfully.',
                'account_number': account.account_number,
            }, status=status.HTTP_201_CREATED)
        logger.error('CreateBankAccount validation errors: %s', serializer.errors)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    try:
        bank_account = BankAccount.objects.get(user=user)
    except BankAccount.DoesNotExist:
        return Response({'error': 'No bank account linked to this user.'}, status=status.HTTP_404_NOT_FOUND)
    return JsonResponse({
        'account_holder_name': bank_account.account_holder_name,
        'account_number': bank_account.account_number,
        'date_of_birth': str(bank_account.date_of_birth) if bank_account.date_of_birth else None,
        'current_address': bank_account.current_address,
        'permanent_address': bank_account.Permanent_Address,
        'sex': bank_account.sex,
        'annual_income': str(bank_account.annual_income),
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
        'created_at': str(bank_account.created_at) if bank_account.created_at else None,
    })
@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    try:
        bank_account = BankAccount.objects.get(user=user)
    except BankAccount.DoesNotExist:
        return Response({'error': 'No bank account linked to this user.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = BankAccountSerializer(bank_account, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'message': 'Profile updated successfully'})
    return JsonResponse({'error': serializer.errors}, status=400)
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def edit_profile_view(request):
    user = request.user
    try:
        bank_account = BankAccount.objects.get(user=user)
    except BankAccount.DoesNotExist:
        return Response({'error': 'No bank account linked to this user.'}, status=status.HTTP_404_NOT_FOUND)
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
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = BankAccountminorSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            return Response({
                'message': 'Minor account created successfully.',
                'account_number': account.account_number,
            }, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CreateBankAccountForSenior(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = BankAccountseniorSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            return Response({
                'message': 'Senior account created successfully.',
                'account_number': account.account_number,
            }, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def balance_view(request):
    try:
        bank_account = BankAccount.objects.get(user=request.user)
        return Response({
            'balance': str(bank_account.balance),
            'account_number': bank_account.account_number,
            'account_holder_name': bank_account.account_holder_name,
        }, status=status.HTTP_200_OK)
    except BankAccount.DoesNotExist:
        return Response({'error': 'No bank account linked to this user.'}, status=status.HTTP_404_NOT_FOUND)


from rest_framework.permissions import IsAdminUser
from .models import BankAccountminor, BankAccountsenior


# ── Admin Login ──────────────────────────────────────────────────────────────
@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def admin_login(request):
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '')
    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    if not (user.is_staff or user.is_superuser):
        return Response({'error': 'Access denied. Staff account required.'}, status=status.HTTP_403_FORBIDDEN)
    token = AccessToken.for_user(user)
    return Response({'token': str(token), 'username': user.username}, status=status.HTTP_200_OK)


# ── Admin Stats ──────────────────────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_stats(request):
    from transaction.models import Transaction
    from django.db.models import Sum, Count
    from django.utils import timezone
    from datetime import timedelta

    accounts = BankAccount.objects.all()
    total_balance = accounts.aggregate(s=Sum('balance'))['s'] or 0

    # Last 7 days transaction chart data
    today = timezone.now().date()
    daily = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        qs = Transaction.objects.filter(date__date=day)
        daily.append({
            'date': day.strftime('%d %b'),
            'count': qs.count(),
            'amount': float(qs.aggregate(s=Sum('amount'))['s'] or 0),
        })

    return Response({
        'total_accounts': accounts.count(),
        'frozen_accounts': accounts.filter(is_frozen=True).count(),
        'total_minor_accounts': BankAccountminor.objects.count(),
        'total_senior_accounts': BankAccountsenior.objects.count(),
        'total_customers': User.objects.filter(is_staff=False, is_superuser=False).count(),
        'total_transactions': Transaction.objects.count(),
        'total_balance': float(total_balance),
        'daily_chart': daily,
    })


# ── Admin Accounts ───────────────────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_list_accounts(request):
    accounts = BankAccount.objects.select_related('user').order_by('-created_at')
    data = [{
        'id': a.id,
        'account_holder_name': a.account_holder_name,
        'account_number': a.account_number,
        'balance': float(a.balance),
        'is_frozen': a.is_frozen,
        'email': a.email,
        'phone_number': a.phone_number,
        'city': a.city,
        'country': a.country,
        'created_at': str(a.created_at) if a.created_at else None,
        'username': a.user.username if a.user else None,
        'account_type': 'Standard',
    } for a in accounts]

    for m in BankAccountminor.objects.order_by('-created_at'):
        data.append({
            'id': f'M{m.id}',
            'account_holder_name': m.account_holder_name,
            'account_number': m.account_number,
            'balance': 0.0,
            'is_frozen': False,
            'email': m.email,
            'phone_number': m.phone_number,
            'city': m.city,
            'country': m.country,
            'created_at': str(m.created_at) if m.created_at else None,
            'username': None,
            'account_type': 'Minor',
        })

    for s in BankAccountsenior.objects.order_by('-created_at'):
        data.append({
            'id': f'S{s.id}',
            'account_holder_name': s.account_holder_name,
            'account_number': s.account_number,
            'balance': 0.0,
            'is_frozen': False,
            'email': s.email,
            'phone_number': s.phone_number,
            'city': s.city,
            'country': s.country,
            'created_at': str(s.created_at) if s.created_at else None,
            'username': None,
            'account_type': 'Senior',
        })

    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def admin_update_account(request, pk):
    try:
        account = BankAccount.objects.get(pk=pk)
    except BankAccount.DoesNotExist:
        return Response({'error': 'Account not found.'}, status=status.HTTP_404_NOT_FOUND)

    if 'is_frozen' in request.data:
        account.is_frozen = bool(request.data['is_frozen'])

    if 'balance' in request.data:
        try:
            account.balance = Decimal(str(request.data['balance']))
        except (ValueError, InvalidOperation):
            return Response({'error': 'Invalid balance value.'}, status=status.HTTP_400_BAD_REQUEST)

    account.save()
    return Response({
        'message': 'Account updated successfully.',
        'is_frozen': account.is_frozen,
        'balance': float(account.balance),
    })


# ── Admin Transactions ───────────────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_list_transactions(request):
    from transaction.models import Transaction
    txns = Transaction.objects.select_related('sender', 'receiver').order_by('-date')[:500]
    return Response([{
        'id': t.id,
        'sender': str(t.sender) if t.sender else None,
        'receiver': str(t.receiver) if t.receiver else None,
        'amount': float(t.amount),
        'status': t.status,
        'transaction_type': t.TransactionType,
        'date': str(t.date),
    } for t in txns])


# ── Card Requests (Customer) ──────────────────────────────────────────────────
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def card_requests(request):
    try:
        account = BankAccount.objects.get(user=request.user)
    except BankAccount.DoesNotExist:
        return Response({'error': 'No bank account linked to your account.'}, status=404)

    if request.method == 'GET':
        reqs = CardRequest.objects.filter(bank_account=account)
        return Response([{
            'id': r.id,
            'card_type': r.card_type,
            'status': r.status,
            'requested_at': r.requested_at.isoformat(),
            'reviewed_at': r.reviewed_at.isoformat() if r.reviewed_at else None,
            'admin_note': r.admin_note,
        } for r in reqs])

    card_type = request.data.get('card_type', '').lower()
    if card_type not in ['classic', 'gold', 'platinum']:
        return Response({'error': 'Invalid card type. Choose classic, gold, or platinum.'}, status=400)

    existing = CardRequest.objects.filter(
        bank_account=account, card_type=card_type, status__in=['pending', 'approved']
    ).first()
    if existing:
        msg = f'You already have an approved {card_type} card.' if existing.status == 'approved' \
              else f'A {card_type} card request is already pending review.'
        return Response({'error': msg}, status=400)

    req = CardRequest.objects.create(bank_account=account, card_type=card_type)
    return Response({
        'id': req.id,
        'card_type': req.card_type,
        'status': req.status,
        'requested_at': req.requested_at.isoformat(),
    }, status=201)


# ── Card Requests (Admin) ─────────────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_list_card_requests(request):
    status_filter = request.query_params.get('status', '')
    qs = CardRequest.objects.select_related('bank_account', 'reviewed_by').order_by('-requested_at')
    if status_filter:
        qs = qs.filter(status=status_filter)

    return Response([{
        'id': r.id,
        'card_type': r.card_type,
        'status': r.status,
        'account_holder_name': r.bank_account.account_holder_name,
        'account_number': r.bank_account.account_number,
        'email': r.bank_account.email,
        'requested_at': r.requested_at.isoformat(),
        'reviewed_at': r.reviewed_at.isoformat() if r.reviewed_at else None,
        'reviewed_by': r.reviewed_by.username if r.reviewed_by else None,
        'admin_note': r.admin_note,
    } for r in qs])


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def admin_review_card_request(request, pk):
    from django.utils import timezone
    try:
        req = CardRequest.objects.select_related('bank_account').get(pk=pk)
    except CardRequest.DoesNotExist:
        return Response({'error': 'Card request not found.'}, status=404)

    if req.status != 'pending':
        return Response({'error': 'Only pending requests can be reviewed.'}, status=400)

    action = request.data.get('action', '')
    if action not in ['approve', 'reject']:
        return Response({'error': 'action must be approve or reject.'}, status=400)

    req.status = 'approved' if action == 'approve' else 'rejected'
    req.reviewed_at = timezone.now()
    req.reviewed_by = request.user
    req.admin_note = request.data.get('admin_note', '')
    req.save()

    return Response({
        'id': req.id,
        'status': req.status,
        'reviewed_at': req.reviewed_at.isoformat(),
        'reviewed_by': req.reviewed_by.username,
        'admin_note': req.admin_note,
    })