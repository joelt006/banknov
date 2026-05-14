# MyBank — Full-Stack Banking Application

A full-stack banking web application built with **Django REST Framework** (backend) and **Vue 3** (frontend). It supports customer banking operations and a dedicated staff admin portal.

---

## Tech Stack

| Layer     | Technology                                      |
|-----------|-------------------------------------------------|
| Backend   | Python 3, Django 5, Django REST Framework       |
| Auth      | SimpleJWT (Bearer tokens)                       |
| Database  | SQLite (dev) — swap for PostgreSQL in prod      |
| Frontend  | Vue 3, Vue Router 4, Vuex 4                     |
| HTTP      | Axios                                           |
| Build     | Vite 5                                          |

---

## Project Structure

banknov/
├── mybank/                  # Django backend
│   ├── account/             # Accounts, auth, card requests app
│   │   ├── models.py        # BankAccount, CardRequest, ...
│   │   ├── views.py         # All API views
│   │   ├── urls.py          # Account + admin API routes
│   │   └── migrations/
│   ├── transaction/         # Transactions app
│   ├── mybank/              # Django project settings
│   │   ├── settings.py
│   │   └── urls.py
│   └── manage.py
└── ui/                      # Vue 3 frontend
└── src/
├── views/           # All page components
├── services/        # apiClient.js, adminApiClient.js
├── router/          # Vue Router with auth guards
├── store/           # Vuex store
└── App.vue          # Shell layouts (customer + admin)



---

## Features

### Customer Portal
- **Register** — Create a bank account first, then register with that account number
- **OTP Verification** — Email OTP on registration
- **Login / Logout** — JWT authentication
- **Dashboard** — Account balance, account number, recent overview
- **Send Money** — Transfer funds to another account number
- **Deposit Money** — Add funds to your account
- **Transaction History** — Full statement of all transactions
- **Profile & Edit Profile** — View and update personal details
- **My Cards** — View Classic / Gold / Platinum card designs and **request a card**
  - Card request shows live status: Pending / Approved / Rejected
  - Full request history with admin notes

### Staff Admin Portal (separate login at `/AdminLogin`)
- **Dashboard** — KPI cards (customers, accounts, balance, transactions), 7-day transaction bar chart, account type donut chart, recent transactions table
- **Account Management** — View all accounts (Standard / Minor / Senior), freeze/unfreeze accounts, edit balances inline
- **Card Requests** — Approve or reject customer card requests with optional staff notes; red badge on sidebar shows pending count

---

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- pip

### Backend Setup

```bash
cd mybank

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# Install dependencies
pip install django djangorestframework djangorestframework-simplejwt \
            django-cors-headers pillow pytesseract

# Copy env file and fill in values
cp .env.example .env

# Run migrations
python manage.py migrate

# Create a superuser (for admin portal access)
python manage.py createsuperuser

# Start server
python manage.py runserver
Backend runs at http://127.0.0.1:8000

Frontend Setup

cd ui
npm install
npm run dev
Frontend runs at http://localhost:5173

Environment Variables
Create mybank/.env (see .env.example):


SECRET_KEY=your-django-secret-key
DEBUG=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your-app-password
Account Types
Type	Description
Standard	Regular adult account with balance
Minor	Account for minors (under 18)
Senior	Account for senior citizens
API Overview
Customer Endpoints (/accounts/)
Method	Endpoint	Description	Auth
POST	CreateBankAccount/	Create bank account	Public
POST	register/	Register user	Public
POST	verify_otp/	Verify email OTP	Public
POST	login/	Customer login	Public
GET	profile/	Get profile	Required
POST	edit-profile/	Update profile	Required
GET	balance/	Get balance + account #	Required
POST	send-money/	Send money	Required
GET/POST	card-requests/	List / create card requests	Required
Admin Endpoints (/accounts/admin/)
Method	Endpoint	Description	Auth
POST	login/	Staff login	Public
GET	stats/	Dashboard KPIs + chart data	Staff only
GET	accounts/	List all accounts	Staff only
PATCH	accounts/<id>/	Freeze / edit balance	Staff only
GET	card-requests/	List card requests	Staff only
PATCH	card-requests/<id>/	Approve / reject request	Staff only
Transaction Endpoints (/transactions/)
Method	Endpoint	Description	Auth
GET	statement/	Transaction history	Required
POST	deposit/	Deposit money	Required
Admin Portal Access
Navigate to http://localhost:5173/AdminLogin
Sign in with your Django superuser or staff account
You'll land on the admin dashboard
To make a user staff via Django shell:


python manage.py shell
>>> from django.contrib.auth.models import User
>>> u = User.objects.get(username='yourusername')
>>> u.is_staff = True
>>> u.save()
Card Request Flow

Customer selects card type (Classic / Gold / Platinum)
        ↓
Clicks "Request Card" on My Cards page
        ↓
Request saved as "Pending"
        ↓
Admin reviews at /Admin/CardRequests
        ↓
Admin approves or rejects with optional note
        ↓
Customer sees updated status on My Cards page
Registration Flow

Create Bank Account → receive account number
        ↓
Register with that account number + email + password
        ↓
Verify OTP sent to email
        ↓
Login → JWT token stored → access dashboard
Notes
db.sqlite3 is excluded from git — each developer gets their own local database
Run python manage.py migrate after pulling new migrations
The admin portal uses a completely separate JWT token (adminToken) from the customer portal (token)
All admin endpoints require is_staff=True on the Django user
