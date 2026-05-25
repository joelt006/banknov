from django.urls import path
from .views import (
    CreateBankAccountView, CreateBankAccountForMinor, CreateBankAccountForSenior,
    register, verify_otp, profile_view, edit_profile_view, login_view,
    user_info, balance_view, get_csrf_token,
    get_captcha, login_otp_verify, logout_view,
    forgot_password, reset_password, change_password,
    pin_status, set_transaction_pin,
    list_sessions, revoke_session, login_history_view,
    admin_login, admin_login_otp_verify,
    admin_stats, admin_list_accounts, admin_update_account, admin_list_transactions,
    card_requests, admin_list_card_requests, admin_review_card_request,
    card_settings_view,
    loans_view, admin_list_loans, admin_review_loan,
    fixed_deposits_view, close_fixed_deposit,
    notifications_view, unread_count_view, notification_detail_view,
    support_tickets_view, support_ticket_detail_view,
    admin_support_tickets_view, admin_support_ticket_detail_view,
)

urlpatterns = [
    # Account creation
    path('CreateBankAccount/', CreateBankAccountView.as_view(), name='CreateBankAccountView'),
    path('CreateBankAccountForMinor/', CreateBankAccountForMinor.as_view(), name='CreateBankAccountForMinor'),
    path('create_bank_account_senior/', CreateBankAccountForSenior.as_view(), name='create_bank_account_senior'),

    # Auth
    path('register/', register, name='register'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('login/', login_view, name='login_view'),
    path('login/verify-otp/', login_otp_verify, name='login_otp_verify'),
    path('logout/', logout_view, name='logout_view'),
    path('captcha/', get_captcha, name='get_captcha'),

    # Password management
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/', reset_password, name='reset_password'),
    path('change-password/', change_password, name='change_password'),

    # Transaction PIN
    path('pin-status/', pin_status, name='pin_status'),
    path('set-pin/', set_transaction_pin, name='set_transaction_pin'),

    # Session & history
    path('sessions/', list_sessions, name='list_sessions'),
    path('sessions/<str:session_key>/', revoke_session, name='revoke_session'),
    path('login-history/', login_history_view, name='login_history_view'),

    # Profile
    path('profile/', profile_view, name='profile'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),
    path('user/', user_info, name='user_info'),
    path('balance/', balance_view, name='balance_view'),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),

    # Admin
    path('admin/login/', admin_login, name='admin_login'),
    path('admin/login/verify-otp/', admin_login_otp_verify, name='admin_login_otp_verify'),
    path('admin/stats/', admin_stats, name='admin_stats'),
    path('admin/accounts/', admin_list_accounts, name='admin_list_accounts'),
    path('admin/accounts/<int:pk>/', admin_update_account, name='admin_update_account'),
    path('admin/transactions/', admin_list_transactions, name='admin_list_transactions'),

    # Cards
    path('card-requests/', card_requests, name='card_requests'),
    path('card-requests/<int:pk>/settings/', card_settings_view, name='card_settings'),
    path('admin/card-requests/', admin_list_card_requests, name='admin_list_card_requests'),
    path('admin/card-requests/<int:pk>/', admin_review_card_request, name='admin_review_card_request'),

    # Loans
    path('loans/', loans_view, name='loans'),
    path('admin/loans/', admin_list_loans, name='admin_list_loans'),
    path('admin/loans/<int:pk>/', admin_review_loan, name='admin_review_loan'),

    # Fixed Deposits
    path('fixed-deposits/', fixed_deposits_view, name='fixed_deposits'),
    path('fixed-deposits/<int:pk>/close/', close_fixed_deposit, name='close_fixed_deposit'),

    # Notifications
    path('notifications/', notifications_view, name='notifications'),
    path('notifications/unread-count/', unread_count_view, name='unread_count'),
    path('notifications/<int:pk>/', notification_detail_view, name='notification_detail'),

    # Support
    path('support/', support_tickets_view, name='support_tickets'),
    path('support/<int:pk>/', support_ticket_detail_view, name='support_ticket_detail'),
    path('admin/support/', admin_support_tickets_view, name='admin_support_tickets'),
    path('admin/support/<int:pk>/', admin_support_ticket_detail_view, name='admin_support_ticket_detail'),
]
