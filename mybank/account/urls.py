from django.urls import path
from .views import CreateBankAccountView , CreateBankAccountForMinor , CreateBankAccountForSenior , register , verify_otp , profile_view , edit_profile_view ,  login_view ,user_info,balance_view,send_money_view,get_csrf_token
from . import views
urlpatterns = [
    path('CreateBankAccount/', CreateBankAccountView.as_view(), name='CreateBankAccountView'),    path('CreateBankAccountForMinor/', CreateBankAccountForMinor.as_view(), name='CreateBankAccountForMinor'),
    path('create_bank_account_senior/', CreateBankAccountForSenior.as_view(), name='create_bank_account_senior'),
    path('register/', register, name='register'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),
    path('profile/', profile_view, name='profile'),
    path('login/', login_view, name='login_view'),
    path('user/', user_info, name='user_info'),
    path('balance/', balance_view, name='balance_view'),
    path('send-money/', send_money_view, name='send_money'),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token')
    

]
