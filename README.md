# MyBank — Full-Stack Banking Application

A full-featured digital banking platform built with **Django REST Framework** (backend) and **Vue 3** (frontend). Covers everything from account creation and money transfers to loans, fixed deposits, card management, notifications, and customer support.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5, Django REST Framework, SimpleJWT |
| Frontend | Vue 3 (Options API), Vue Router 4, Vuex 4, Axios |
| Database | SQLite (dev) |
| Auth | JWT tokens + OTP via email |
| Styling | Scoped CSS, CSS custom properties, no external UI library |

---

## Project Structure

```
banknov/
├── mybank/                  # Django project root
│   ├── account/             # Core banking app
│   │   ├── models.py        # All models
│   │   ├── views.py         # All account/feature views
│   │   ├── urls.py          # URL patterns
│   │   └── migrations/      # 17 migrations
│   ├── transaction/         # Transaction app
│   │   ├── models.py        # Transaction, Beneficiary, ScheduledTransfer
│   │   ├── views.py         # Send money, beneficiaries, scheduled transfers
│   │   └── urls.py
│   └── mybank/              # Django settings & root urls
└── ui/                      # Vue 3 frontend
    └── src/
        ├── views/           # All page components
        ├── router/          # Vue Router config
        ├── store/           # Vuex store
        └── App.vue          # Shell layout (customer + admin)
```

---

## Features

### Authentication & Security

| Feature | Details |
|---------|---------|
| Registration | OTP verified via email |
| Login | Username/password + OTP second factor + CAPTCHA |
| Forgot Password | OTP-based reset flow |
| Change Password | In-app with current password verification |
| Transaction PIN | 4-digit PIN, bcrypt-hashed, required for all outgoing transfers |
| JWT Auth | Access tokens stored in `localStorage`, sent as `Bearer` header |
| Rate Limiting | Cache-based limiting on login attempts and PIN entries |
| Session Management | List all active sessions with device/IP info, revoke individually |
| Login History | Full timestamped login log with success/failure reasons |

---

### Account Management

- **Account Types** — Regular, Minor, Senior (separate creation flows)
- **Account Details page** — Balance (show/hide toggle), account number + IFSC copy buttons, branch, account type, status, date opened
- **Profile** — View and edit personal details (name, address, contact, photo)
- **Admin: Freeze / Unfreeze** — Admin can freeze accounts; frozen accounts block all outgoing transactions

---

### Transfers & Payments

- **Send Money** — Instant transfer with transaction PIN verification; atomic balance update with `select_for_update`
- **Beneficiaries** — Save, list, and delete frequent recipients; quick-select chips on Send Money page
- **Scheduled Transfers** — Future-dated transfers; PIN verified at creation time; cancellable while pending
- **Transaction Statement** — Full history with date-range filter, CSV export, and browser print

---

### My Cards

- **Request Cards** — Classic, Gold, Platinum; one per type; pending / approved / rejected status
- **Card Details** — Card number, expiry date, CVV (admin-generated on approval)
- **Block / Unblock** — Toggle card block status instantly
- **Card Controls** — Per-card toggle switches for International, Online, and Contactless transactions

---

### Loans

- **Loan Types** — Personal (12%), Home (8.5%), Car (9%), Education (8%)
- **Apply** — Amount, tenure (months), purpose; max 3 active/pending loans at once
- **Live EMI Calculator** — Updates instantly using `P × r(1+r)^n / ((1+r)^n - 1)`
- **Admin Review** — Approve with a custom approved amount (disbursed directly to balance) or reject with a note
- **Loan Disbursal** — Atomic balance credit + `LOAN_DISBURSAL` transaction record on approval

---

### Fixed Deposits

- **Tenure Options** — 3 / 6 / 12 / 24 / 36 / 60 months
- **Interest Rates** — 4.5% → 7.5% (compound, annually)
- **Open FD** — Deducted atomically from balance; `FD_OPENING` transaction created
- **Live Maturity Preview** — Shows maturity amount and date before opening
- **Maturity Progress Bar** — Visual progress on each active FD card
- **Close FD** — Full maturity amount at or after maturity date; 1% penalty on interest if premature

---

### Notifications & Alerts

- **Bell Icon** — Topbar badge showing unread count; polls every 30 seconds
- **Dropdown** — Last 6 notifications with type-coloured icons; click marks as read and navigates
- **Full Notifications Page** — All / Unread tabs, type filter (Transaction / Loan / FD / Card / Security / System)
- **Mark All Read** — Single button to clear all unread
- **Delete** — Per-notification delete; clear-all with confirmation modal
- **Auto-triggered for:**
  - Money sent (sender) and money received (recipient)
  - Card request submitted, approved, or rejected
  - Loan application submitted, approved, or rejected
  - Fixed deposit opened, closed, or matured
  - Support ticket created, staff replied, status changed

---

### Customer Support

- **Raise a Ticket** — Category (Account / Transaction / Card / Loan / FD / Technical / Other), subject, description
- **Ticket Numbers** — Auto-generated `TKT-XXXXXXXX` format
- **Threaded Chat View** — Customer messages and staff replies in a chat-style thread
- **Status Tracking** — Open → In Progress → Resolved / Closed
- **Reply** — Customer can reply to open/in-progress tickets; Ctrl+Enter shortcut
- **FAQ Accordion** — 5 built-in common questions to reduce ticket volume
- **Admin: Support Tickets** — Filter by status, priority, category; inline status/priority dropdowns; staff reply with indigo-style bubbles

---

### Admin Portal

Separate login flow (OTP-protected), distinct sidebar and shell styling.

| Section | Capabilities |
|---------|-------------|
| Dashboard | Total accounts, balance, transactions, pending card requests |
| Account Management | List all accounts, freeze/unfreeze, manual deposit |
| Transactions | View all transactions across accounts |
| Card Requests | Approve (generates card number, expiry, CVV) or reject with note |
| Loan Applications | Filter by status; approve with custom amount (auto-disburses); reject with note |
| Support Tickets | Full ticket list with filters; reply as staff; update status and priority |

---

## API Endpoints

### Auth & Profile (`/accounts/`)
```
POST   register/                  Register new user
POST   verify_otp/                Verify registration OTP
POST   login/                     Login (returns JWT)
POST   login/verify-otp/          Verify login OTP
POST   logout/                    Invalidate token
GET    captcha/                   Get CAPTCHA challenge
POST   forgot-password/           Send reset OTP
POST   reset-password/            Reset with OTP
POST   change-password/           Change password (auth required)
GET    profile/                   Get profile
PATCH  edit-profile/              Update profile
GET    user/                      Get logged-in user info
GET    balance/                   Get balance + account details
GET/POST pin-status/ set-pin/     Transaction PIN management
GET    sessions/                  List active sessions
DELETE sessions/<key>/            Revoke a session
GET    login-history/             Login log
```

### Cards (`/accounts/`)
```
GET/POST  card-requests/                    List / request a card
GET/PATCH card-requests/<id>/settings/      Get / update card controls
```

### Loans & FDs (`/accounts/`)
```
GET/POST  loans/                            List / apply for loan
GET/POST  fixed-deposits/                   List / open FD
POST      fixed-deposits/<id>/close/        Close / claim FD
```

### Notifications (`/accounts/`)
```
GET/POST  notifications/                    List / mark all read
GET       notifications/unread-count/       Unread count (for polling)
PATCH     notifications/<id>/              Mark one as read
DELETE    notifications/<id>/              Delete one
```

### Support (`/accounts/`)
```
GET/POST  support/                          List tickets / create ticket
GET/POST  support/<id>/                     Get ticket + messages / reply
```

### Transactions (`/transactions/`)
```
POST      send-money/                       Instant transfer
GET       statement/                        Transaction history
GET/POST  beneficiaries/                    List / add beneficiary
DELETE    beneficiaries/<id>/               Remove beneficiary
GET/POST  scheduled/                        List / create scheduled transfer
DELETE    scheduled/<id>/                   Cancel scheduled transfer
```

### Admin (`/accounts/admin/`)
```
POST      login/                            Admin login
POST      login/verify-otp/                 Verify admin OTP
GET       stats/                            Dashboard stats
GET       accounts/                         List all accounts
PATCH     accounts/<id>/                    Freeze / deposit
GET       transactions/                     All transactions
GET       card-requests/                    List card requests
PATCH     card-requests/<id>/               Approve / reject card
GET       loans/                            List loan applications
PATCH     loans/<id>/                       Approve / reject loan
GET       support/                          List all tickets
GET/PATCH/POST support/<id>/               View / update / reply to ticket
```

---

## Setup & Running

### Backend

```bash
cd mybank
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # for admin portal access
python manage.py runserver
```

**Email config** — set in `settings.py`:
```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your@email.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

**Process scheduled transfers** (run via cron or manually):
```bash
python manage.py process_scheduled_transfers
```

### Frontend

```bash
cd ui
npm install
npm run dev
```

App runs at `http://localhost:5173`, API at `http://127.0.0.1:8000`.

---

## Database Models

| Model | App | Purpose |
|-------|-----|---------|
| `BankAccount` | account | Main savings account |
| `BankAccountminor` | account | Minor account |
| `BankAccountsenior` | account | Senior account |
| `CardRequest` | account | Card request + controls |
| `LoanApplication` | account | Loan application lifecycle |
| `FixedDeposit` | account | FD record |
| `Notification` | account | In-app alerts |
| `SupportTicket` | account | Customer support ticket |
| `TicketMessage` | account | Threaded ticket messages |
| `LoginHistory` | account | Login audit log |
| `UserSession` | account | Active session tracking |
| `Transaction` | transaction | Money movement record |
| `Beneficiary` | transaction | Saved recipients |
| `ScheduledTransfer` | transaction | Future-dated transfers |

---

## Frontend Routes

### Customer (requires auth)
| Route | Page |
|-------|------|
| `/Dashboard` | Balance overview, quick actions |
| `/AccountDetails` | Full account info |
| `/SendMoney` | Transfer with beneficiary quick-select |
| `/Beneficiaries` | Manage saved recipients |
| `/ScheduledTransfers` | View / cancel scheduled transfers |
| `/TransactionStatement` | History with filter, CSV, print |
| `/MyCards` | Card management + controls |
| `/Loans` | Loan list + apply with EMI preview |
| `/FixedDeposits` | FD list + open new FD |
| `/Notifications` | Full notification centre |
| `/Support` | Raise tickets + chat thread |
| `/Profile` | View profile |
| `/EditProfile` | Edit personal details |
| `/Security` | Password, PIN, sessions, login history |

### Admin (requires admin auth)
| Route | Page |
|-------|------|
| `/AdminLogin` | Admin login |
| `/Admin/Dashboard` | Stats overview |
| `/Admin/Accounts` | Account management |
| `/Admin/CardRequests` | Card request review |
| `/Admin/Loans` | Loan application review |
| `/Admin/Support` | Support ticket management |
