<template>
  <div class="page">

    <!-- Account card -->
    <div class="hero-card" v-if="account">
      <div class="hero-top">
        <div class="acct-type-badge">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
          {{ account.account_type }}
        </div>
        <span class="status-chip" :class="account.is_frozen ? 'frozen' : 'active'">
          {{ account.is_frozen ? '● Frozen' : '● Active' }}
        </span>
      </div>
      <div class="balance-label">Available Balance</div>
      <div class="balance-val" v-if="showBalance">₹ {{ formatAmount(account.balance) }}</div>
      <div class="balance-val masked" v-else>₹ ••••••</div>
      <button class="toggle-balance" @click="showBalance = !showBalance">
        <svg v-if="showBalance" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
        {{ showBalance ? 'Hide Balance' : 'Show Balance' }}
      </button>
      <div class="holder-name">{{ account.account_holder_name }}</div>
    </div>

    <!-- Details grid -->
    <div class="details-card" v-if="account">
      <h3 class="section-title">Account Information</h3>
      <div class="details-grid">

        <div class="detail-item">
          <div class="detail-label">Account Number</div>
          <div class="detail-value mono">
            {{ formatAcct(account.account_number) }}
            <button class="copy-btn" @click="copy(account.account_number, 'acct')" title="Copy">
              <svg v-if="copied === 'acct'" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
            </button>
          </div>
        </div>

        <div class="detail-item">
          <div class="detail-label">IFSC Code</div>
          <div class="detail-value mono">
            {{ account.ifsc_code }}
            <button class="copy-btn" @click="copy(account.ifsc_code, 'ifsc')" title="Copy">
              <svg v-if="copied === 'ifsc'" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
            </button>
          </div>
        </div>

        <div class="detail-item">
          <div class="detail-label">Account Type</div>
          <div class="detail-value">{{ account.account_type }}</div>
        </div>

        <div class="detail-item">
          <div class="detail-label">Account Status</div>
          <div class="detail-value">
            <span class="status-chip" :class="account.is_frozen ? 'frozen' : 'active'">
              {{ account.is_frozen ? 'Frozen' : 'Active' }}
            </span>
          </div>
        </div>

        <div class="detail-item">
          <div class="detail-label">Branch</div>
          <div class="detail-value">{{ account.branch }}</div>
        </div>

        <div class="detail-item">
          <div class="detail-label">Date Opened</div>
          <div class="detail-value">{{ formatDate(account.created_at) }}</div>
        </div>

      </div>
    </div>

    <!-- Quick actions -->
    <div class="actions-card" v-if="account">
      <h3 class="section-title">Quick Actions</h3>
      <div class="actions-row">
        <RouterLink to="/SendMoney" class="action-btn blue">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          Send Money
        </RouterLink>
        <RouterLink to="/TransactionStatement" class="action-btn purple">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
          Statements
        </RouterLink>
        <RouterLink to="/MyCards" class="action-btn amber">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
          My Cards
        </RouterLink>
        <RouterLink to="/Security" class="action-btn green">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          Security
        </RouterLink>
      </div>
    </div>

    <!-- Frozen warning -->
    <div v-if="account && account.is_frozen" class="frozen-banner">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
      Your account is currently <strong>frozen</strong>. Transfers and withdrawals are not allowed. Please contact support to unfreeze your account.
    </div>

    <!-- Loading / error -->
    <div v-if="loading" class="state-loading">
      <div class="spinner"></div> Loading account details…
    </div>
    <div v-if="error" class="state-error">{{ error }}</div>

  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

export default {
  data() {
    return { account: null, loading: true, error: '', showBalance: true, copied: '' };
  },
  async created() {
    try {
      const res = await apiClient.get('/accounts/balance/');
      this.account = res.data;
    } catch (err) {
      this.error = err.response?.data?.error || 'Failed to load account details.';
    } finally {
      this.loading = false;
    }
  },
  methods: {
    formatAmount(v) {
      return parseFloat(v || 0).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },
    formatAcct(n) {
      return (n || '').replace(/(.{4})/g, '$1 ').trim();
    },
    formatDate(iso) {
      if (!iso) return '—';
      return new Date(iso).toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' });
    },
    async copy(text, key) {
      try {
        await navigator.clipboard.writeText(text);
        this.copied = key;
        setTimeout(() => { this.copied = ''; }, 2000);
      } catch { /* fallback — browser may not support clipboard */ }
    },
  },
};
</script>

<style scoped>
.page { max-width: 720px; margin: 0 auto; display: flex; flex-direction: column; gap: 20px; }

/* Hero */
.hero-card {
  background: linear-gradient(135deg, #1a2f5e 0%, #2563eb 100%);
  border-radius: 20px; padding: 32px 36px; color: #fff;
  box-shadow: 0 8px 32px rgba(37,99,235,.3);
}
.hero-top { display: flex; align-items: center; gap: 12px; margin-bottom: 24px; }
.acct-type-badge {
  display: flex; align-items: center; gap: 7px;
  background: rgba(255,255,255,.15); border-radius: 20px;
  padding: 6px 14px; font-size: 13px; font-weight: 600;
}
.acct-type-badge svg { width: 15px; height: 15px; }
.balance-label { font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,.6); margin-bottom: 6px; }
.balance-val { font-size: 44px; font-weight: 800; letter-spacing: -1px; margin-bottom: 14px; }
.balance-val.masked { letter-spacing: 2px; }
.toggle-balance {
  display: inline-flex; align-items: center; gap: 7px;
  background: rgba(255,255,255,.12); border: 1.5px solid rgba(255,255,255,.2);
  color: rgba(255,255,255,.85); border-radius: 8px; padding: 7px 14px;
  font-size: 13px; font-weight: 600; cursor: pointer; margin-bottom: 20px; transition: background .15s;
}
.toggle-balance svg { width: 15px; height: 15px; }
.toggle-balance:hover { background: rgba(255,255,255,.2); }
.holder-name { font-size: 18px; font-weight: 700; color: rgba(255,255,255,.9); }

/* Details card */
.details-card {
  background: #fff; border-radius: 20px; padding: 28px;
  box-shadow: 0 2px 16px rgba(15,32,68,.08); border: 1.5px solid #e2e8f0;
}
.section-title { font-size: 15px; font-weight: 800; color: #1e293b; margin-bottom: 20px; }
.details-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.detail-item { display: flex; flex-direction: column; gap: 5px; }
.detail-label { font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: .6px; }
.detail-value { font-size: 15px; font-weight: 600; color: #1e293b; display: flex; align-items: center; gap: 8px; }
.detail-value.mono { font-family: 'Courier New', monospace; letter-spacing: 1px; font-size: 14px; }

.copy-btn {
  width: 28px; height: 28px; border-radius: 7px; border: 1.5px solid #e2e8f0;
  background: #f8fafc; display: flex; align-items: center; justify-content: center;
  cursor: pointer; flex-shrink: 0; transition: background .15s;
}
.copy-btn svg { width: 14px; height: 14px; stroke: #64748b; }
.copy-btn:hover { background: #eff6ff; }

/* Status chip */
.status-chip { padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; }
.status-chip.active { background: #dcfce7; color: #16a34a; }
.status-chip.frozen { background: #dbeafe; color: #1d4ed8; }

/* Actions */
.actions-card {
  background: #fff; border-radius: 20px; padding: 28px;
  box-shadow: 0 2px 16px rgba(15,32,68,.08); border: 1.5px solid #e2e8f0;
}
.actions-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.action-btn {
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  padding: 18px 12px; border-radius: 12px; text-decoration: none;
  font-size: 13px; font-weight: 600; transition: transform .15s, box-shadow .15s;
  border: 1.5px solid transparent;
}
.action-btn svg { width: 20px; height: 20px; }
.action-btn:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,.1); }
.action-btn.blue   { background: #eff6ff; color: #2563eb; border-color: #bfdbfe; }
.action-btn.purple { background: #f5f3ff; color: #7c3aed; border-color: #ddd6fe; }
.action-btn.amber  { background: #fffbeb; color: #d97706; border-color: #fde68a; }
.action-btn.green  { background: #f0fdf4; color: #16a34a; border-color: #bbf7d0; }

/* Frozen banner */
.frozen-banner {
  display: flex; align-items: flex-start; gap: 12px;
  background: #eff6ff; border: 1.5px solid #bfdbfe; border-radius: 14px;
  padding: 16px 20px; color: #1d4ed8; font-size: 14px; line-height: 1.5;
}
.frozen-banner svg { width: 20px; height: 20px; flex-shrink: 0; margin-top: 1px; }

/* State */
.state-loading { display: flex; align-items: center; gap: 12px; color: #64748b; font-size: 14px; padding: 24px 0; }
.state-error { padding: 16px; background: #fef2f2; color: #b91c1c; border-radius: 10px; font-size: 14px; border: 1px solid #fecaca; }
.spinner { width: 20px; height: 20px; border: 2px solid #e2e8f0; border-top-color: #2563eb; border-radius: 50%; animation: spin .6s linear infinite; display: inline-block; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 600px) {
  .details-grid { grid-template-columns: 1fr; }
  .actions-row { grid-template-columns: repeat(2, 1fr); }
  .hero-card { padding: 24px 20px; }
  .balance-val { font-size: 32px; }
}
</style>
