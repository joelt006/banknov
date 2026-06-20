from .serializers import BankAccountSerializer, BankAccountminorSerializer, BankAccountseniorSerializer
from django.contrib.auth import authenticate, login as django_login
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from email.mime.multipart import MIMEMultipart
from rest_framework.response import Response
from django.middleware.csrf import get_token
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.http import JsonResponse, FileResponse
from email.mime.text import MIMEText
from django.core.cache import cache
from .forms import EditProfileForm
from rest_framework import status
from django.conf import settings
from .models import BankAccount, CardRequest, LoginHistory, UserSession
from .utils import rate_limit
from django.contrib.auth.hashers import make_password, check_password as check_pw
from PIL import Image
import pytesseract
import logging
import smtplib
import random
import secrets
import uuid
import json
from rest_framework_simplejwt.tokens import AccessToken



logger = logging.getLogger(__name__)


def _rate_limit(key, max_attempts=5, window_seconds=900):
    attempts = cache.get(key, 0)
    if attempts >= max_attempts:
        return False
    cache.set(key, attempts + 1, timeout=window_seconds)
    return True


def generate_otp():
    return secrets.randbelow(900000) + 100000
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
    if not _rate_limit(f'otp_attempts_{email}', max_attempts=5, window_seconds=600):
        return JsonResponse({'error': 'Too many attempts. Try again later.'}, status=429)
    cached_otp = cache.get(f'otp_{email}')
    if cached_otp and str(cached_otp) == str(otp):
        cache.delete(f'otp_{email}')
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
            username = data.get('username', '')
            password = data.get('password', '')
            captcha_id = data.get('captcha_id', '')
            captcha_answer = data.get('captcha_answer', '')
            ip = request.META.get('REMOTE_ADDR', 'unknown')

            if not _rate_limit(f'login_{ip}', max_attempts=5, window_seconds=900):
                return JsonResponse({'error': 'Too many login attempts. Try again later.'}, status=429)

            expected = cache.get(f'captcha_{captcha_id}')
            if not captcha_id or expected is None or not captcha_answer:
                return JsonResponse({'error': 'CAPTCHA is required.'}, status=400)
            try:
                if int(captcha_answer) != expected:
                    cache.delete(f'captcha_{captcha_id}')
                    return JsonResponse({'error': 'Incorrect CAPTCHA answer.'}, status=400)
            except (ValueError, TypeError):
                return JsonResponse({'error': 'Invalid CAPTCHA answer.'}, status=400)
            cache.delete(f'captcha_{captcha_id}')

            user = authenticate(request, username=username, password=password)
            if user:
                otp = generate_otp()
                temp_token = str(uuid.uuid4())
                cache.set(f'login_otp_{temp_token}', {'user_id': user.id, 'otp': otp}, timeout=300)
                send_otp_email(user.email, otp)
                return JsonResponse({'requires_otp': True, 'temp_token': temp_token})
            else:
                LoginHistory.objects.create(
                    user=User.objects.filter(username=username).first(),
                    ip_address=ip,
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    success=False,
                    failure_reason='Invalid credentials',
                )
                return JsonResponse({'error': 'Invalid credentials.'}, status=401)
        except Exception:
            return JsonResponse({'error': 'Login failed. Please try again.'}, status=500)


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


# ── CAPTCHA ───────────────────────────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([AllowAny])
def get_captcha(request):
    a = random.randint(1, 15)
    b = random.randint(1, 15)
    captcha_id = str(uuid.uuid4())
    cache.set(f'captcha_{captcha_id}', a + b, timeout=300)
    return JsonResponse({'captcha_id': captcha_id, 'question': f'{a} + {b} = ?'})


# ── Login OTP verify ──────────────────────────────────────────────────────────
@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login_otp_verify(request):
    temp_token = request.data.get('temp_token', '')
    otp = request.data.get('otp', '')
    if not temp_token or not otp:
        return JsonResponse({'error': 'Token and OTP are required.'}, status=400)
    if not _rate_limit(f'login_otp_verify_{temp_token}', max_attempts=5, window_seconds=300):
        return JsonResponse({'error': 'Too many attempts. Please login again.'}, status=429)
    data = cache.get(f'login_otp_{temp_token}')
    if not data:
        return JsonResponse({'error': 'Session expired. Please login again.'}, status=400)
    if str(data['otp']) != str(otp):
        return JsonResponse({'error': 'Invalid OTP.'}, status=400)
    cache.delete(f'login_otp_{temp_token}')
    try:
        user = User.objects.get(id=data['user_id'])
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=400)
    ip = request.META.get('REMOTE_ADDR', 'unknown')
    ua = request.META.get('HTTP_USER_AGENT', '')
    session = UserSession.objects.create(
        user=user, ip_address=ip, user_agent=ua,
    )
    token = AccessToken.for_user(user)
    token['session_key'] = str(session.session_key)
    django_login(request, user)
    LoginHistory.objects.create(user=user, ip_address=ip, user_agent=ua, success=True)
    return JsonResponse({'message': 'Login successful!', 'token': str(token), 'username': user.username})


# ── Logout ────────────────────────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    session_key = request.auth.get('session_key') if request.auth else None
    if session_key:
        UserSession.objects.filter(session_key=session_key).update(is_active=False)
    return Response({'message': 'Logged out successfully.'})


# ── Forgot password ───────────────────────────────────────────────────────────
@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get('email', '').strip()
    if not email:
        return Response({'error': 'Email is required.'}, status=400)
    if not _rate_limit(f'forgot_pw_{email}', max_attempts=3, window_seconds=900):
        return Response({'error': 'Too many requests. Try again later.'}, status=429)
    user = User.objects.filter(email=email).first()
    if user:
        otp = generate_otp()
        cache.set(f'reset_otp_{email}', otp, timeout=600)
        send_otp_email(email, otp)
    return Response({'message': 'If an account with that email exists, an OTP has been sent.'})


@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def reset_password(request):
    email = request.data.get('email', '').strip()
    otp = request.data.get('otp', '').strip()
    new_password = request.data.get('new_password', '')
    if not email or not otp or not new_password:
        return Response({'error': 'Email, OTP, and new password are required.'}, status=400)
    if not _rate_limit(f'reset_otp_attempts_{email}', max_attempts=5, window_seconds=600):
        return Response({'error': 'Too many attempts. Try again later.'}, status=429)
    cached_otp = cache.get(f'reset_otp_{email}')
    if not cached_otp or str(cached_otp) != str(otp):
        return Response({'error': 'Invalid or expired OTP.'}, status=400)
    user = User.objects.filter(email=email).first()
    if not user:
        return Response({'error': 'User not found.'}, status=404)
    if len(new_password) < 8:
        return Response({'error': 'Password must be at least 8 characters.'}, status=400)
    user.set_password(new_password)
    user.save()
    cache.delete(f'reset_otp_{email}')
    UserSession.objects.filter(user=user, is_active=True).update(is_active=False)
    return Response({'message': 'Password reset successful. Please login again.'})


# ── Change password (authenticated) ──────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    current_password = request.data.get('current_password', '')
    new_password = request.data.get('new_password', '')
    if not current_password or not new_password:
        return Response({'error': 'Current and new password are required.'}, status=400)
    user = request.user
    if not user.check_password(current_password):
        return Response({'error': 'Current password is incorrect.'}, status=400)
    if len(new_password) < 8:
        return Response({'error': 'New password must be at least 8 characters.'}, status=400)
    if current_password == new_password:
        return Response({'error': 'New password must be different.'}, status=400)
    user.set_password(new_password)
    user.save()
    session_key = request.auth.get('session_key') if request.auth else None
    qs = UserSession.objects.filter(user=user, is_active=True)
    if session_key:
        qs = qs.exclude(session_key=session_key)
    qs.update(is_active=False)
    return Response({'message': 'Password changed. Other sessions have been logged out.'})


# ── Transaction PIN ───────────────────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pin_status(request):
    try:
        account = BankAccount.objects.get(user=request.user)
        return Response({'has_pin': bool(account.transaction_pin)})
    except BankAccount.DoesNotExist:
        return Response({'error': 'No bank account linked.'}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_transaction_pin(request):
    new_pin = request.data.get('new_pin', '')
    current_pin = request.data.get('current_pin', '')
    if not new_pin or not new_pin.isdigit() or len(new_pin) != 4:
        return Response({'error': 'PIN must be exactly 4 digits.'}, status=400)
    try:
        account = BankAccount.objects.get(user=request.user)
    except BankAccount.DoesNotExist:
        return Response({'error': 'No bank account linked.'}, status=404)
    if account.transaction_pin:
        if not current_pin:
            return Response({'error': 'Current PIN is required to change PIN.'}, status=400)
        if not check_pw(current_pin, account.transaction_pin):
            return Response({'error': 'Current PIN is incorrect.'}, status=400)
    account.transaction_pin = make_password(new_pin)
    account.save()
    return Response({'message': 'Transaction PIN set successfully.'})


# ── Session management ────────────────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_sessions(request):
    current_key = request.auth.get('session_key') if request.auth else None
    sessions = UserSession.objects.filter(user=request.user, is_active=True)
    return Response([{
        'id': s.id,
        'session_key': s.session_key,
        'ip_address': s.ip_address,
        'user_agent': s.user_agent,
        'created_at': s.created_at.isoformat(),
        'last_seen': s.last_seen.isoformat(),
        'is_current': s.session_key == current_key,
    } for s in sessions])


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def revoke_session(request, session_key):
    session = UserSession.objects.filter(
        user=request.user, session_key=session_key, is_active=True
    ).first()
    if not session:
        return Response({'error': 'Session not found.'}, status=404)
    session.is_active = False
    session.save()
    return Response({'message': 'Session revoked.'})


# ── Login history ─────────────────────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def login_history_view(request):
    history = LoginHistory.objects.filter(user=request.user)[:20]
    return Response([{
        'ip_address': h.ip_address,
        'user_agent': h.user_agent,
        'timestamp': h.timestamp.isoformat(),
        'success': h.success,
        'failure_reason': h.failure_reason,
    } for h in history])


logger = logging.getLogger(__name__)


from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import BankAccountSerializer

def _verify_identity_photo(photo, aadhar_number, account_holder_name):
    """OCR-checks that the uploaded ID photo's text contains the submitted
    Aadhar number and name. Returns a list of error strings (empty = passed)."""
    import re
    try:
        image = Image.open(photo)
        extracted_text = pytesseract.image_to_string(image)
    except Exception as e:
        logger.error(f"Error processing identity photo: {e}")
        return ["Could not process the uploaded photo. Please upload a clear image."]

    extracted_normalized = extracted_text.lower()
    extracted_digits = re.sub(r'\D', '', extracted_text)
    errors = []
    if aadhar_number:
        aadhar_digits = re.sub(r'\D', '', str(aadhar_number))
        if not aadhar_digits or aadhar_digits not in extracted_digits:
            errors.append("Aadhar number does not match the one in the photo.")
    if account_holder_name:
        name_normalized = ' '.join(account_holder_name.lower().split())
        if name_normalized not in ' '.join(extracted_normalized.split()):
            errors.append("Account holder name does not match the one in the photo.")
    return errors


class CreateBankAccountView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        ip = request.META.get('REMOTE_ADDR', 'unknown')
        if not _rate_limit(f'create_account_{ip}', max_attempts=3, window_seconds=3600):
            return Response({'error': 'Too many account creation attempts. Try again later.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        serializer = BankAccountSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error('CreateBankAccount validation errors: %s', serializer.errors)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        photo = serializer.validated_data.get('photo')
        if not photo:
            return Response({'error': 'Photo is required for identity verification.'}, status=status.HTTP_400_BAD_REQUEST)
        errors = _verify_identity_photo(
            photo,
            serializer.validated_data.get('aadhar_number'),
            serializer.validated_data.get('account_holder_name'),
        )
        if errors:
            return Response({'error': errors}, status=status.HTTP_400_BAD_REQUEST)

        account = serializer.save()
        return Response({
            'message': 'Bank account created successfully.',
            'account_number': account.account_number,
        }, status=status.HTTP_201_CREATED)


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
        'aadhar_number': f'XXXX XXXX {bank_account.aadhar_number[-4:]}' if bank_account.aadhar_number else None,
        'passport_number': f'XXXXX{bank_account.passport_number[-4:]}' if bank_account.passport_number else None,
        'voter_id_number': f'XXXXXXX{bank_account.voter_id_number[-3:]}' if bank_account.voter_id_number else None,
        'pan_card_number': bank_account.pan_card_number,
        'photo': '/accounts/identity-photo/' if bank_account.photo else None,
        'created_at': str(bank_account.created_at) if bank_account.created_at else None,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def identity_photo_view(request):
    """Serves the caller's own identity photo. Never exposed via a public
    media URL — access requires a valid JWT for the account that owns the photo."""
    try:
        bank_account = BankAccount.objects.get(user=request.user)
    except BankAccount.DoesNotExist:
        return Response({'error': 'No bank account linked to this user.'}, status=status.HTTP_404_NOT_FOUND)
    if not bank_account.photo:
        return Response({'error': 'No photo on file.'}, status=status.HTTP_404_NOT_FOUND)
    return FileResponse(bank_account.photo.open('rb'), content_type='image/jpeg')


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
        'photo': '/accounts/identity-photo/' if bank_account.photo else None,
        'created_at': bank_account.created_at
    }})
class CreateBankAccountForMinor(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        ip = request.META.get('REMOTE_ADDR', 'unknown')
        if not _rate_limit(f'create_account_{ip}', max_attempts=3, window_seconds=3600):
            return Response({'error': 'Too many account creation attempts. Try again later.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
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
        ip = request.META.get('REMOTE_ADDR', 'unknown')
        if not _rate_limit(f'create_account_{ip}', max_attempts=3, window_seconds=3600):
            return Response({'error': 'Too many account creation attempts. Try again later.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
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
            'is_frozen': bank_account.is_frozen,
            'created_at': bank_account.created_at.isoformat(),
            'ifsc_code': 'MYBK0001234',
            'account_type': 'Savings Account',
            'branch': 'MyBank Main Branch, New Delhi',
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
    ip = request.META.get('REMOTE_ADDR', 'unknown')
    if not _rate_limit(f'admin_login_{ip}', max_attempts=5, window_seconds=900):
        return Response({'error': 'Too many login attempts. Try again later.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    if not (user.is_staff or user.is_superuser):
        return Response({'error': 'Access denied. Staff account required.'}, status=status.HTTP_403_FORBIDDEN)
    otp = generate_otp()
    temp_token = str(uuid.uuid4())
    cache.set(f'admin_login_otp_{temp_token}', {'user_id': user.id, 'otp': otp}, timeout=300)
    send_otp_email(user.email, otp)
    return Response({'requires_otp': True, 'temp_token': temp_token}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def admin_login_otp_verify(request):
    temp_token = request.data.get('temp_token', '')
    otp = request.data.get('otp', '')
    if not temp_token or not otp:
        return Response({'error': 'Token and OTP are required.'}, status=400)
    if not _rate_limit(f'admin_otp_verify_{temp_token}', max_attempts=5, window_seconds=300):
        return Response({'error': 'Too many attempts. Please login again.'}, status=429)
    data = cache.get(f'admin_login_otp_{temp_token}')
    if not data:
        return Response({'error': 'Session expired. Please login again.'}, status=400)
    if str(data['otp']) != str(otp):
        return Response({'error': 'Invalid OTP.'}, status=400)
    cache.delete(f'admin_login_otp_{temp_token}')
    try:
        user = User.objects.get(id=data['user_id'])
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=400)
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


# ── CVV encryption helpers ───────────────────────────────────────────────────
# Uses Fernet symmetric encryption (account/encryption_key.key) instead of
# Django's signing.dumps, which is HMAC-signed but NOT confidential — the
# CVV was trivially recoverable from the stored value without the SECRET_KEY.
def _encrypt_cvv(cvv_plain):
    from .serializers import encrypt_data
    return encrypt_data(cvv_plain).decode()


def _decrypt_cvv(encrypted_cvv):
    from .serializers import decrypt_data
    try:
        return decrypt_data(encrypted_cvv.encode())
    except Exception:
        return None


# ── Card number generator (Luhn-valid 16-digit number) ───────────────────────
def _generate_card_number(card_type):
    prefixes = {'classic': '4111', 'gold': '5200', 'platinum': '3782'}
    prefix = prefixes.get(card_type, '4111')
    while True:
        partial = prefix + ''.join([str(secrets.randbelow(10)) for _ in range(11)])
        total = sum(
            (n * 2 - 9 if n * 2 > 9 else n * 2) if i % 2 == 0 else n
            for i, n in enumerate(int(d) for d in reversed(partial))
        )
        check = (10 - (total % 10)) % 10
        number = partial + str(check)
        if not CardRequest.objects.filter(card_number=number).exists():
            return number


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
            'card_number': r.card_number if r.status == 'approved' else None,
            'expiry_date': r.expiry_date.strftime('%m/%y') if r.expiry_date else None,
            'cvv': _decrypt_cvv(r.cvv) if r.status == 'approved' and r.cvv else None,
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
    _notify(request.user, 'Card Request Submitted',
            f'Your {card_type.capitalize()} card request has been submitted and is under review.',
            'card', '/MyCards')
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

    if req.status == 'approved':
        from datetime import date
        req.card_number = _generate_card_number(req.card_type)
        req.expiry_date = date(timezone.now().year + 4, timezone.now().month, 1)
        req.cvv = _encrypt_cvv(str(secrets.randbelow(900) + 100))

    req.save()

    if req.bank_account.user:
        if req.status == 'approved':
            _notify(req.bank_account.user, 'Card Request Approved',
                    f'Your {req.card_type.capitalize()} card has been approved! Card ending in {req.card_number[-4:]} is ready.',
                    'card', '/MyCards')
        else:
            note_suffix = f' Reason: {req.admin_note}' if req.admin_note else ''
            _notify(req.bank_account.user, 'Card Request Rejected',
                    f'Your {req.card_type.capitalize()} card request was not approved.{note_suffix}',
                    'card', '/MyCards')

    return Response({
        'id': req.id,
        'status': req.status,
        'reviewed_at': req.reviewed_at.isoformat(),
        'reviewed_by': req.reviewed_by.username,
        'admin_note': req.admin_note,
        'card_number': req.card_number,
        'expiry_date': req.expiry_date.strftime('%m/%y') if req.expiry_date else None,
    })


# ── Card Controls (Customer) ──────────────────────────────────────────────────
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def card_settings_view(request, pk):
    try:
        account = BankAccount.objects.get(user=request.user)
        req = CardRequest.objects.get(pk=pk, bank_account=account, status='approved')
    except (BankAccount.DoesNotExist, CardRequest.DoesNotExist):
        return Response({'error': 'Card not found.'}, status=404)

    if request.method == 'GET':
        return Response({
            'id': req.id,
            'is_blocked': req.is_blocked,
            'allow_international': req.allow_international,
            'allow_online': req.allow_online,
            'allow_contactless': req.allow_contactless,
        })

    allowed_fields = {'is_blocked', 'allow_international', 'allow_online', 'allow_contactless'}
    for field in allowed_fields:
        if field in request.data:
            setattr(req, field, bool(request.data[field]))
    req.save()
    return Response({
        'id': req.id,
        'is_blocked': req.is_blocked,
        'allow_international': req.allow_international,
        'allow_online': req.allow_online,
        'allow_contactless': req.allow_contactless,
    })


# ── Loan interest rates ───────────────────────────────────────────────────────
_LOAN_RATES = {
    'personal': 12.0,
    'home': 8.5,
    'car': 9.0,
    'education': 8.0,
}

def _calc_emi(principal, annual_rate, months):
    r = float(annual_rate) / 100 / 12
    n = months
    if r == 0:
        return round(float(principal) / n, 2)
    emi = float(principal) * r * (1 + r)**n / ((1 + r)**n - 1)
    return round(emi, 2)


# ── Loans (Customer) ──────────────────────────────────────────────────────────
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def loans_view(request):
    from .models import LoanApplication
    try:
        account = BankAccount.objects.get(user=request.user)
    except BankAccount.DoesNotExist:
        return Response({'error': 'No bank account linked.'}, status=404)

    if request.method == 'GET':
        loans = LoanApplication.objects.filter(bank_account=account)
        return Response([{
            'id': l.id,
            'loan_type': l.loan_type,
            'amount': str(l.amount),
            'tenure_months': l.tenure_months,
            'interest_rate': str(l.interest_rate),
            'purpose': l.purpose,
            'status': l.status,
            'monthly_emi': str(l.monthly_emi) if l.monthly_emi else None,
            'approved_amount': str(l.approved_amount) if l.approved_amount else None,
            'admin_note': l.admin_note,
            'applied_at': l.applied_at.isoformat(),
            'reviewed_at': l.reviewed_at.isoformat() if l.reviewed_at else None,
        } for l in loans])

    loan_type = request.data.get('loan_type', '').lower()
    if loan_type not in _LOAN_RATES:
        return Response({'error': 'Invalid loan type.'}, status=400)

    try:
        amount = Decimal(str(request.data.get('amount', 0)))
        if amount < 1000:
            return Response({'error': 'Minimum loan amount is ₹1,000.'}, status=400)
    except Exception:
        return Response({'error': 'Invalid amount.'}, status=400)

    valid_tenures = [12, 24, 36, 60, 84, 120]
    try:
        tenure = int(request.data.get('tenure_months', 0))
        if tenure not in valid_tenures:
            return Response({'error': f'Tenure must be one of {valid_tenures} months.'}, status=400)
    except Exception:
        return Response({'error': 'Invalid tenure.'}, status=400)

    from .models import LoanApplication
    active = LoanApplication.objects.filter(bank_account=account, status__in=['pending', 'approved', 'active']).count()
    if active >= 3:
        return Response({'error': 'You already have 3 active/pending loan applications.'}, status=400)

    rate = _LOAN_RATES[loan_type]
    emi = _calc_emi(amount, rate, tenure)
    loan = LoanApplication.objects.create(
        bank_account=account,
        loan_type=loan_type,
        amount=amount,
        tenure_months=tenure,
        interest_rate=Decimal(str(rate)),
        purpose=request.data.get('purpose', '').strip(),
        monthly_emi=Decimal(str(emi)),
    )
    _notify(request.user, 'Loan Application Submitted',
            f'Your ₹{float(amount):,.2f} {loan_type.capitalize()} Loan application is under review.',
            'loan', '/Loans')
    return Response({
        'id': loan.id,
        'loan_type': loan.loan_type,
        'amount': str(loan.amount),
        'tenure_months': loan.tenure_months,
        'interest_rate': str(loan.interest_rate),
        'monthly_emi': str(loan.monthly_emi),
        'status': loan.status,
        'applied_at': loan.applied_at.isoformat(),
    }, status=201)


# ── Loans (Admin) ─────────────────────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_list_loans(request):
    from .models import LoanApplication
    status_filter = request.query_params.get('status', '')
    qs = LoanApplication.objects.select_related('bank_account', 'reviewed_by').order_by('-applied_at')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return Response([{
        'id': l.id,
        'loan_type': l.loan_type,
        'amount': str(l.amount),
        'tenure_months': l.tenure_months,
        'interest_rate': str(l.interest_rate),
        'monthly_emi': str(l.monthly_emi) if l.monthly_emi else None,
        'purpose': l.purpose,
        'status': l.status,
        'account_holder_name': l.bank_account.account_holder_name,
        'account_number': l.bank_account.account_number,
        'email': l.bank_account.email,
        'approved_amount': str(l.approved_amount) if l.approved_amount else None,
        'admin_note': l.admin_note,
        'applied_at': l.applied_at.isoformat(),
        'reviewed_at': l.reviewed_at.isoformat() if l.reviewed_at else None,
        'reviewed_by': l.reviewed_by.username if l.reviewed_by else None,
    } for l in qs])


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def admin_review_loan(request, pk):
    from .models import LoanApplication
    from django.utils import timezone as tz
    from django.db import transaction as db_tx
    try:
        loan = LoanApplication.objects.select_related('bank_account').get(pk=pk)
    except LoanApplication.DoesNotExist:
        return Response({'error': 'Loan not found.'}, status=404)

    if loan.status not in ('pending',):
        return Response({'error': 'Only pending loans can be reviewed.'}, status=400)

    action = request.data.get('action', '')
    if action not in ('approve', 'reject'):
        return Response({'error': 'action must be approve or reject.'}, status=400)

    loan.admin_note = request.data.get('admin_note', '')
    loan.reviewed_at = tz.now()
    loan.reviewed_by = request.user

    if action == 'approve':
        try:
            approved_amt = Decimal(str(request.data.get('approved_amount', loan.amount)))
        except Exception:
            return Response({'error': 'Invalid approved_amount.'}, status=400)
        emi = _calc_emi(approved_amt, float(loan.interest_rate), loan.tenure_months)
        loan.approved_amount = approved_amt
        loan.monthly_emi = Decimal(str(emi))
        loan.status = 'active'
        with db_tx.atomic():
            loan.save()
            account = BankAccount.objects.select_for_update().get(pk=loan.bank_account_id)
            account.balance += approved_amt
            account.save()
            from transaction.models import Transaction
            Transaction.objects.create(
                sender=None,
                receiver=account,
                amount=approved_amt,
                status='Completed',
                TransactionType='LOAN_DISBURSAL',
            )
    else:
        loan.status = 'rejected'
        loan.save()

    if loan.bank_account.user:
        if action == 'approve':
            _notify(loan.bank_account.user, 'Loan Approved & Disbursed',
                    f'Your {loan.loan_type.capitalize()} Loan of ₹{float(approved_amt):,.2f} has been approved and credited to your account!',
                    'loan', '/Loans')
        else:
            note_suffix = f' Reason: {loan.admin_note}' if loan.admin_note else ''
            _notify(loan.bank_account.user, 'Loan Application Rejected',
                    f'Your {loan.loan_type.capitalize()} Loan application was not approved.{note_suffix}',
                    'loan', '/Loans')

    return Response({'id': loan.id, 'status': loan.status, 'approved_amount': str(loan.approved_amount) if loan.approved_amount else None})


# ── Fixed Deposits ────────────────────────────────────────────────────────────
_FD_RATES = {3: 4.5, 6: 5.5, 12: 6.5, 24: 7.0, 36: 7.25, 60: 7.5}

def _calc_fd_maturity(principal, annual_rate, tenure_months):
    years = tenure_months / 12
    maturity = float(principal) * (1 + float(annual_rate) / 100) ** years
    return round(maturity, 2)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def fixed_deposits_view(request):
    from .models import FixedDeposit
    from datetime import date
    from dateutil.relativedelta import relativedelta
    try:
        account = BankAccount.objects.get(user=request.user)
    except BankAccount.DoesNotExist:
        return Response({'error': 'No bank account linked.'}, status=404)

    if request.method == 'GET':
        fds = FixedDeposit.objects.filter(bank_account=account)
        return Response([{
            'id': f.id,
            'amount': str(f.amount),
            'tenure_months': f.tenure_months,
            'interest_rate': str(f.interest_rate),
            'start_date': str(f.start_date),
            'maturity_date': str(f.maturity_date),
            'maturity_amount': str(f.maturity_amount),
            'status': f.status,
        } for f in fds])

    try:
        amount = Decimal(str(request.data.get('amount', 0)))
        if amount < 1000:
            return Response({'error': 'Minimum FD amount is ₹1,000.'}, status=400)
    except Exception:
        return Response({'error': 'Invalid amount.'}, status=400)

    try:
        tenure = int(request.data.get('tenure_months', 0))
        if tenure not in _FD_RATES:
            return Response({'error': f'Tenure must be one of {list(_FD_RATES.keys())} months.'}, status=400)
    except Exception:
        return Response({'error': 'Invalid tenure.'}, status=400)

    if account.balance < amount:
        return Response({'error': 'Insufficient balance to open this FD.'}, status=400)
    if account.is_frozen:
        return Response({'error': 'Your account is frozen.'}, status=403)

    rate = _FD_RATES[tenure]
    maturity_amount = _calc_fd_maturity(amount, rate, tenure)
    today = date.today()
    maturity_date = today + relativedelta(months=tenure)

    from django.db import transaction as db_tx
    with db_tx.atomic():
        account_locked = BankAccount.objects.select_for_update().get(pk=account.pk)
        if account_locked.balance < amount:
            return Response({'error': 'Insufficient balance.'}, status=400)
        account_locked.balance -= amount
        account_locked.save()
        fd = FixedDeposit.objects.create(
            bank_account=account_locked,
            amount=amount,
            tenure_months=tenure,
            interest_rate=Decimal(str(rate)),
            maturity_date=maturity_date,
            maturity_amount=Decimal(str(maturity_amount)),
        )
        from transaction.models import Transaction
        Transaction.objects.create(
            sender=account_locked,
            receiver=None,
            amount=amount,
            status='Completed',
            TransactionType='FD_OPENING',
        )

    _notify(request.user, 'Fixed Deposit Opened',
            f'FD of ₹{float(amount):,.2f} for {tenure} months opened. Matures on {maturity_date}.',
            'fd', '/FixedDeposits')
    return Response({
        'id': fd.id,
        'amount': str(fd.amount),
        'tenure_months': fd.tenure_months,
        'interest_rate': str(fd.interest_rate),
        'start_date': str(fd.start_date),
        'maturity_date': str(fd.maturity_date),
        'maturity_amount': str(fd.maturity_amount),
        'status': fd.status,
    }, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def close_fixed_deposit(request, pk):
    from .models import FixedDeposit
    from django.utils import timezone as tz
    from django.db import transaction as db_tx
    try:
        account = BankAccount.objects.get(user=request.user)
        fd = FixedDeposit.objects.get(pk=pk, bank_account=account, status='active')
    except (BankAccount.DoesNotExist, FixedDeposit.DoesNotExist):
        return Response({'error': 'FD not found or already closed.'}, status=404)

    today = tz.now().date()
    is_premature = today < fd.maturity_date
    if is_premature:
        # 1% penalty on interest
        interest_earned = float(fd.maturity_amount) - float(fd.amount)
        penalty = interest_earned * 0.01
        credit_amount = Decimal(str(round(float(fd.amount) + interest_earned - penalty, 2)))
    else:
        credit_amount = fd.maturity_amount

    with db_tx.atomic():
        account_locked = BankAccount.objects.select_for_update().get(pk=account.pk)
        account_locked.balance += credit_amount
        account_locked.save()
        fd.status = 'closed' if is_premature else 'matured'
        fd.save()
        from transaction.models import Transaction
        Transaction.objects.create(
            sender=None,
            receiver=account_locked,
            amount=credit_amount,
            status='Completed',
            TransactionType='FD_CLOSURE',
        )

    label = 'Closed Early' if is_premature else 'Matured'
    _notify(request.user, f'Fixed Deposit {label}',
            f'Your FD of ₹{float(fd.amount):,.2f} has been closed. ₹{float(credit_amount):,.2f} credited to your account.',
            'fd', '/FixedDeposits')
    return Response({
        'credited': str(credit_amount),
        'premature': is_premature,
        'status': fd.status,
    })


# ── Notification helper ───────────────────────────────────────────────────────
def _notify(user, title, message, ntype='system', link=''):
    from .models import Notification
    try:
        Notification.objects.create(
            user=user, title=title, message=message,
            notification_type=ntype, link=link,
        )
    except Exception:
        pass


# ── Notifications (Customer) ──────────────────────────────────────────────────
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def notifications_view(request):
    from .models import Notification
    if request.method == 'GET':
        unread_only = request.query_params.get('unread_only') == '1'
        qs = Notification.objects.filter(user=request.user)
        if unread_only:
            qs = qs.filter(is_read=False)
        return Response([{
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'notification_type': n.notification_type,
            'is_read': n.is_read,
            'link': n.link,
            'created_at': n.created_at.isoformat(),
        } for n in qs[:50]])

    # POST — mark all as read
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return Response({'status': 'ok'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_count_view(request):
    from .models import Notification
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return Response({'count': count})


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def notification_detail_view(request, pk):
    from .models import Notification
    try:
        n = Notification.objects.get(pk=pk, user=request.user)
    except Notification.DoesNotExist:
        return Response({'error': 'Not found.'}, status=404)
    if request.method == 'DELETE':
        n.delete()
        return Response(status=204)
    n.is_read = True
    n.save()
    return Response({'id': n.id, 'is_read': n.is_read})


# ── Support Tickets ───────────────────────────────────────────────────────────
def _ticket_number():
    import string
    chars = string.ascii_uppercase + string.digits
    from .models import SupportTicket
    while True:
        num = 'TKT-' + ''.join(random.choices(chars, k=8))
        if not SupportTicket.objects.filter(ticket_number=num).exists():
            return num


def _ticket_data(t, include_messages=False):
    d = {
        'id': t.id,
        'ticket_number': t.ticket_number,
        'subject': t.subject,
        'category': t.category,
        'status': t.status,
        'priority': t.priority,
        'created_at': t.created_at.isoformat(),
        'updated_at': t.updated_at.isoformat(),
        'message_count': t.messages.count(),
    }
    if include_messages:
        d['messages'] = [{
            'id': m.id,
            'sender': m.sender.get_full_name() or m.sender.username,
            'is_staff': m.is_staff,
            'body': m.body,
            'created_at': m.created_at.isoformat(),
        } for m in t.messages.all()]
    return d


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def support_tickets_view(request):
    from .models import SupportTicket, TicketMessage
    if request.method == 'GET':
        tickets = SupportTicket.objects.filter(user=request.user).prefetch_related('messages')
        return Response([_ticket_data(t) for t in tickets])

    subject = request.data.get('subject', '').strip()
    category = request.data.get('category', 'other')
    body = request.data.get('body', '').strip()

    if not subject:
        return Response({'error': 'Subject is required.'}, status=400)
    if not body:
        return Response({'error': 'Please describe your issue.'}, status=400)
    if len(subject) > 150:
        return Response({'error': 'Subject must be under 150 characters.'}, status=400)

    ticket = SupportTicket.objects.create(
        user=request.user,
        ticket_number=_ticket_number(),
        subject=subject,
        category=category,
    )
    TicketMessage.objects.create(ticket=ticket, sender=request.user, is_staff=False, body=body)
    _notify(request.user, 'Support Ticket Created',
            f'Ticket {ticket.ticket_number} has been created. We\'ll get back to you soon.',
            'system', '/Support')
    return Response(_ticket_data(ticket, include_messages=True), status=201)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def support_ticket_detail_view(request, pk):
    from .models import SupportTicket, TicketMessage
    try:
        ticket = SupportTicket.objects.prefetch_related('messages').get(pk=pk, user=request.user)
    except SupportTicket.DoesNotExist:
        return Response({'error': 'Ticket not found.'}, status=404)

    if request.method == 'GET':
        return Response(_ticket_data(ticket, include_messages=True))

    if ticket.status in ('resolved', 'closed'):
        return Response({'error': 'This ticket is closed. Please open a new ticket.'}, status=400)

    body = request.data.get('body', '').strip()
    if not body:
        return Response({'error': 'Message cannot be empty.'}, status=400)

    TicketMessage.objects.create(ticket=ticket, sender=request.user, is_staff=False, body=body)
    ticket.status = 'open'
    ticket.save()
    return Response(_ticket_data(ticket, include_messages=True))


# ── Support Tickets (Admin) ───────────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_support_tickets_view(request):
    from .models import SupportTicket
    qs = SupportTicket.objects.select_related('user').prefetch_related('messages').order_by('-created_at')
    status_filter = request.query_params.get('status', '')
    priority_filter = request.query_params.get('priority', '')
    category_filter = request.query_params.get('category', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    if priority_filter:
        qs = qs.filter(priority=priority_filter)
    if category_filter:
        qs = qs.filter(category=category_filter)
    result = []
    for t in qs:
        d = _ticket_data(t)
        d['username'] = t.user.username
        d['user_email'] = t.user.email
        result.append(d)
    return Response(result)


@api_view(['GET', 'PATCH', 'POST'])
@permission_classes([IsAdminUser])
def admin_support_ticket_detail_view(request, pk):
    from .models import SupportTicket, TicketMessage
    try:
        ticket = SupportTicket.objects.select_related('user').prefetch_related('messages').get(pk=pk)
    except SupportTicket.DoesNotExist:
        return Response({'error': 'Ticket not found.'}, status=404)

    if request.method == 'GET':
        d = _ticket_data(ticket, include_messages=True)
        d['username'] = ticket.user.username
        d['user_email'] = ticket.user.email
        return Response(d)

    if request.method == 'PATCH':
        new_status = request.data.get('status', ticket.status)
        new_priority = request.data.get('priority', ticket.priority)
        ticket.status = new_status
        ticket.priority = new_priority
        ticket.save()
        status_labels = {'open': 'Open', 'in_progress': 'In Progress', 'resolved': 'Resolved', 'closed': 'Closed'}
        if new_status in ('resolved', 'closed'):
            _notify(ticket.user, f'Ticket {ticket.ticket_number} {status_labels.get(new_status, new_status)}',
                    f'Your support ticket "{ticket.subject}" has been marked as {status_labels.get(new_status, new_status)}.',
                    'system', '/Support')
        return Response(_ticket_data(ticket))

    # POST — admin reply
    body = request.data.get('body', '').strip()
    if not body:
        return Response({'error': 'Reply cannot be empty.'}, status=400)
    TicketMessage.objects.create(ticket=ticket, sender=request.user, is_staff=True, body=body)
    ticket.status = 'in_progress'
    ticket.save()
    _notify(ticket.user, f'Support Reply on {ticket.ticket_number}',
            f'Staff replied to your ticket: "{ticket.subject}".',
            'system', '/Support')
    return Response(_ticket_data(ticket, include_messages=True))