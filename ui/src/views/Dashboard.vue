<template>
  <div class="dashboard">

    <!-- Hero balance card -->
    <div class="hero-card">
      <div class="hero-left">
        <p class="greeting">Good {{ timeOfDay }}, <strong>{{ username }}</strong> 👋</p>
        <p class="hero-label">Available Balance</p>
        <h1 class="hero-balance">₹ {{ formatAmount(balance) }}</h1>
        <div class="acct-badge">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
          {{ accountNumber || '—' }}
        </div>
      </div>
      <div class="hero-right">
        <div class="stat-pill">
          <span class="pill-label">Total Sent</span>
          <span class="pill-value debit">- ₹{{ formatAmount(totalSent) }}</span>
        </div>
        <div class="stat-pill">
          <span class="pill-label">Total Received</span>
          <span class="pill-value credit">+ ₹{{ formatAmount(totalReceived) }}</span>
        </div>
        <div class="stat-pill">
          <span class="pill-label">Transactions</span>
          <span class="pill-value">{{ transactions.length }}</span>
        </div>
      </div>
    </div>

    <!-- No account linked banner -->
    <div v-if="noAccount" class="no-account-banner">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      <div>
        <strong>No bank account linked to your login.</strong>
        To see your balance, first
        <RouterLink to="/CreateAccountoption">create a bank account</RouterLink>,
        then register with that account number — this links the account to your login.
      </div>
    </div>

    <!-- Quick actions -->
    <div class="section-title">Quick Actions</div>
    <div class="actions-grid">
      <RouterLink to="/SendMoney" class="action-card">
        <div class="action-icon blue">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
        </div>
        <span class="action-label">Send Money</span>
      </RouterLink>
      <RouterLink to="/DepositMoney" class="action-card">
        <div class="action-icon green">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></svg>
        </div>
        <span class="action-label">Deposit</span>
      </RouterLink>
      <RouterLink to="/TransactionStatement" class="action-card">
        <div class="action-icon purple">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
        </div>
        <span class="action-label">History</span>
      </RouterLink>
      <RouterLink to="/Profile" class="action-card">
        <div class="action-icon gold">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        </div>
        <span class="action-label">Profile</span>
      </RouterLink>
    </div>

    <!-- Recent transactions -->
    <div class="section-header">
      <span class="section-title" style="margin:0">Recent Transactions</span>
      <RouterLink to="/TransactionStatement" class="view-all">View all →</RouterLink>
    </div>

    <div class="txn-card">
      <div v-if="loading" class="state-empty">
        <div class="spinner-lg"></div>
        <p>Loading transactions…</p>
      </div>
      <div v-else-if="recentTxns.length === 0" class="state-empty">
        <svg viewBox="0 0 24 24" fill="none" stroke="#cbd5e1" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        <p>No transactions yet</p>
      </div>
      <div v-else>
        <div v-for="txn in recentTxns" :key="txn.id" class="txn-row">
          <div class="txn-icon-wrap" :class="isSent(txn) ? 'sent' : 'received'">
            <svg v-if="isSent(txn)" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></svg>
          </div>
          <div class="txn-info">
            <p class="txn-title">{{ isSent(txn) ? 'Sent to ' + txn.receiver : 'Received from ' + txn.sender }}</p>
            <p class="txn-date">{{ formatDate(txn.date) }} · {{ txn.status }}</p>
          </div>
          <div class="txn-amount" :class="isSent(txn) ? 'debit' : 'credit'">
            {{ isSent(txn) ? '−' : '+' }} ₹{{ formatAmount(txn.amount) }}
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

export default {
  data() {
    return {
      username: '',
      balance: '0',
      accountNumber: '',
      transactions: [],
      loading: true,
      noAccount: false,
    };
  },
  computed: {
    timeOfDay() {
      const h = new Date().getHours();
      if (h < 12) return 'morning';
      if (h < 17) return 'afternoon';
      return 'evening';
    },
    recentTxns() {
      return this.transactions.slice(0, 6);
    },
    totalSent() {
      return this.transactions
        .filter(t => this.isSent(t))
        .reduce((s, t) => s + parseFloat(t.amount || 0), 0)
        .toFixed(2);
    },
    totalReceived() {
      return this.transactions
        .filter(t => !this.isSent(t))
        .reduce((s, t) => s + parseFloat(t.amount || 0), 0)
        .toFixed(2);
    },
  },
  async created() {
    await Promise.all([this.fetchUserData(), this.fetchTransactions()]);
    this.loading = false;
  },
  methods: {
    async fetchUserData() {
      try {
        const res = await apiClient.get('/accounts/balance/');
        this.balance = res.data.balance;
        this.accountNumber = res.data.account_number || '';
        this.username = res.data.account_holder_name || '';
        this.noAccount = false;
      } catch (err) {
        this.noAccount = true;
        console.error('[Dashboard] balance endpoint:', err.response?.status, err.response?.data);
        const userRes = await apiClient.get('/accounts/user/').catch(() => null);
        if (userRes) this.username = userRes.data.username || '';
      }
    },
    async fetchTransactions() {
      try {
        const res = await apiClient.get('/transactions/statement/');
        this.transactions = res.data;
      } catch { this.transactions = []; }
    },
    isSent(txn) {
      return txn.sender && txn.sender.includes(this.accountNumber);
    },
    formatAmount(val) {
      return parseFloat(val || 0).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },
    formatDate(d) {
      return new Date(d).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
    },
  },
};
</script>

<style scoped>
.dashboard { display: flex; flex-direction: column; gap: 24px; }

/* Hero */
.hero-card {
  background: linear-gradient(135deg, #1a2f5e 0%, #2563eb 100%);
  border-radius: 20px; padding: 32px 36px;
  display: flex; justify-content: space-between; align-items: center;
  color: #fff; box-shadow: 0 8px 32px rgba(37,99,235,.3);
  flex-wrap: wrap; gap: 24px;
}
.greeting { font-size: 15px; color: rgba(255,255,255,.75); margin-bottom: 12px; }
.greeting strong { color: #fff; }
.hero-label { font-size: 13px; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,.6); margin-bottom: 6px; }
.hero-balance { font-size: 42px; font-weight: 800; letter-spacing: -1px; margin-bottom: 16px; }
.acct-badge {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(255,255,255,.12); border-radius: 40px;
  padding: 7px 16px; font-size: 14px; font-weight: 600; letter-spacing: .5px;
}
.acct-badge svg { width: 16px; height: 16px; }

.hero-right { display: flex; flex-direction: column; gap: 12px; }
.stat-pill {
  background: rgba(255,255,255,.1); border-radius: 12px;
  padding: 14px 20px; display: flex; flex-direction: column; gap: 4px; min-width: 170px;
}
.pill-label { font-size: 11px; text-transform: uppercase; letter-spacing: .8px; color: rgba(255,255,255,.6); }
.pill-value { font-size: 18px; font-weight: 700; color: #fff; }
.pill-value.debit { color: #fca5a5; }
.pill-value.credit { color: #6ee7b7; }

/* Section titles */
.section-title { font-size: 16px; font-weight: 700; color: #1e293b; }
.section-header { display: flex; align-items: center; justify-content: space-between; }
.view-all { font-size: 13px; font-weight: 600; color: #2563eb; transition: color .15s; }
.view-all:hover { color: #1d4ed8; }

/* Quick actions */
.actions-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.action-card {
  background: #fff; border-radius: 14px; padding: 24px 16px;
  display: flex; flex-direction: column; align-items: center; gap: 12px;
  text-decoration: none; color: #1e293b;
  box-shadow: 0 2px 8px rgba(15,32,68,.06);
  border: 1.5px solid #e2e8f0;
  transition: transform .18s, box-shadow .18s, border-color .18s;
}
.action-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(15,32,68,.1); border-color: #bfdbfe; }

.action-icon {
  width: 52px; height: 52px; border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
}
.action-icon svg { width: 22px; height: 22px; }
.action-icon.blue  { background: #eff6ff; color: #2563eb; }
.action-icon.green { background: #f0fdf4; color: #16a34a; }
.action-icon.purple{ background: #faf5ff; color: #7c3aed; }
.action-icon.gold  { background: #fffbeb; color: #d97706; }

.action-label { font-size: 13px; font-weight: 600; color: #475569; }

/* Transactions */
.txn-card {
  background: #fff; border-radius: 16px; overflow: hidden;
  box-shadow: 0 2px 8px rgba(15,32,68,.06); border: 1.5px solid #e2e8f0;
}
.state-empty {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 48px 24px; gap: 12px; color: #94a3b8; font-size: 14px;
}
.state-empty svg { width: 48px; height: 48px; }
.spinner-lg {
  width: 36px; height: 36px; border: 3px solid #e2e8f0; border-top-color: #2563eb;
  border-radius: 50%; animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.txn-row {
  display: flex; align-items: center; gap: 14px;
  padding: 16px 20px; border-bottom: 1px solid #f1f5f9;
  transition: background .15s;
}
.txn-row:last-child { border-bottom: none; }
.txn-row:hover { background: #f8fafc; }

.txn-icon-wrap {
  width: 40px; height: 40px; border-radius: 12px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
}
.txn-icon-wrap svg { width: 18px; height: 18px; }
.txn-icon-wrap.sent     { background: #fef2f2; color: #ef4444; }
.txn-icon-wrap.received { background: #f0fdf4; color: #16a34a; }

.txn-info { flex: 1; min-width: 0; }
.txn-title { font-size: 13px; font-weight: 600; color: #1e293b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.txn-date { font-size: 12px; color: #94a3b8; margin-top: 2px; }

.txn-amount { font-size: 14px; font-weight: 700; white-space: nowrap; }
.txn-amount.debit  { color: #ef4444; }
.txn-amount.credit { color: #16a34a; }

.no-account-banner {
  display: flex; align-items: flex-start; gap: 12px;
  background: #fffbeb; border: 1.5px solid #fde68a; border-radius: 14px;
  padding: 16px 20px; color: #78350f; font-size: 14px; line-height: 1.5;
}
.no-account-banner svg { width: 20px; height: 20px; flex-shrink: 0; margin-top: 2px; }
.no-account-banner a { color: #2563eb; font-weight: 600; text-decoration: underline; }

@media (max-width: 640px) {
  .hero-card { flex-direction: column; padding: 24px 20px; }
  .hero-balance { font-size: 30px; }
  .actions-grid { grid-template-columns: repeat(2, 1fr); }
  .hero-right { flex-direction: row; flex-wrap: wrap; }
  .stat-pill { min-width: 0; flex: 1; }
}
</style>
