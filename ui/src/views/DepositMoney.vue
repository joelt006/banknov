<template>
  <div class="page">
    <div class="transfer-layout">

      <div class="form-card">
        <div class="card-icon green">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></svg>
        </div>
        <h2 class="card-title">Deposit Money</h2>
        <p class="card-sub">Add funds to any bank account</p>

        <form @submit.prevent="depositMoney" class="form">
          <div class="amount-field">
            <label>Amount to Deposit</label>
            <div class="amount-wrap green">
              <span class="currency">₹</span>
              <input v-model="amount" type="number" min="1" step="0.01" placeholder="0.00" required class="amount-input" />
            </div>
          </div>

          <div class="field">
            <label>Account Number</label>
            <input v-model="account_number" type="text" placeholder="16-digit account number" maxlength="16" required />
          </div>

          <div v-if="error" class="alert-error">{{ error }}</div>

          <button type="submit" class="btn-deposit" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></svg>
            {{ loading ? 'Processing…' : 'Deposit Now' }}
          </button>
        </form>
      </div>

      <!-- Success / Info -->
      <div v-if="success" class="success-card">
        <div class="success-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        </div>
        <h3>Deposit Successful!</h3>
        <p>₹ {{ formatAmount(lastAmount) }} added to</p>
        <div class="success-acct">{{ lastAccount }}</div>
        <div class="new-balance">
          <span class="bal-label">New Balance</span>
          <span class="bal-value">₹ {{ formatAmount(newBalance) }}</span>
        </div>
        <button class="btn-new" @click="resetForm">Make Another Deposit</button>
        <RouterLink to="/Dashboard" class="link-dash">Back to Dashboard →</RouterLink>
      </div>

      <div v-else class="info-panel">
        <h3 class="info-title">Deposit Information</h3>
        <div class="info-rows">
          <div class="info-row"><span>Processing Time</span><span class="val">Instant</span></div>
          <div class="info-row"><span>Minimum Amount</span><span class="val">₹ 1</span></div>
          <div class="info-row"><span>Charges</span><span class="val free">Free</span></div>
          <div class="info-row"><span>Availability</span><span class="val">24 × 7</span></div>
        </div>
        <div class="tip-box">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          You can deposit to any account number registered in MyBank.
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

export default {
  data() {
    return { amount: '', account_number: '', error: '', loading: false, success: false, newBalance: '', lastAmount: '', lastAccount: '' };
  },
  methods: {
    async depositMoney() {
      this.error = '';
      this.loading = true;
      try {
        const res = await apiClient.post('/transactions/deposit-money/', {
          account_number: this.account_number,
          amount: this.amount,
        });
        this.lastAmount = this.amount;
        this.lastAccount = this.account_number;
        this.newBalance = res.data.new_balance || '';
        this.success = true;
      } catch (err) {
        this.error = err.response?.data?.error || 'Deposit failed. Please try again.';
      } finally {
        this.loading = false;
      }
    },
    resetForm() {
      this.amount = ''; this.account_number = ''; this.success = false; this.error = '';
    },
    formatAmount(val) {
      return parseFloat(val || 0).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },
  },
};
</script>

<style scoped>
.page { max-width: 860px; margin: 0 auto; }
.transfer-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: start; }

.form-card {
  background: #fff; border-radius: 20px; padding: 32px;
  box-shadow: 0 2px 16px rgba(15,32,68,.08); border: 1.5px solid #e2e8f0;
}
.card-icon { width: 52px; height: 52px; border-radius: 14px; display: flex; align-items: center; justify-content: center; margin-bottom: 20px; }
.card-icon svg { width: 24px; height: 24px; }
.card-icon.green { background: #f0fdf4; color: #16a34a; }
.card-title { font-size: 22px; font-weight: 800; color: #1e293b; margin-bottom: 6px; }
.card-sub { font-size: 13px; color: #64748b; margin-bottom: 28px; }

.form { display: flex; flex-direction: column; gap: 20px; }

.amount-field { display: flex; flex-direction: column; gap: 6px; }
.amount-field label { font-size: 12px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: .6px; }
.amount-wrap { display: flex; align-items: center; border: 2px solid #16a34a; border-radius: 12px; background: #f0fdf4; overflow: hidden; }
.currency { padding: 0 16px; font-size: 22px; font-weight: 700; border-right: 2px solid #bbf7d0; color: #16a34a; }
.amount-input { flex: 1; border: none; background: transparent; padding: 16px; font-size: 26px; font-weight: 700; color: #1e293b; outline: none; min-width: 0; }
.amount-input::placeholder { color: #cbd5e1; }

.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 12px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: .6px; }
.field input { padding: 12px 14px; border: 1.5px solid #e2e8f0; border-radius: 10px; font-size: 15px; color: #1e293b; background: #f8fafc; outline: none; transition: border-color .18s, box-shadow .18s; }
.field input:focus { border-color: #16a34a; box-shadow: 0 0 0 3px rgba(22,163,74,.1); background: #fff; }

.alert-error { padding: 11px 14px; border-radius: 8px; font-size: 13px; background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }

.btn-deposit {
  width: 100%; padding: 14px; background: #16a34a; color: #fff;
  border: none; border-radius: 10px; font-size: 15px; font-weight: 700;
  cursor: pointer; transition: background .18s; display: flex; align-items: center; justify-content: center; gap: 8px;
}
.btn-deposit svg { width: 18px; height: 18px; }
.btn-deposit:hover:not(:disabled) { background: #15803d; }
.btn-deposit:disabled { opacity: .6; cursor: not-allowed; }

.success-card {
  background: #fff; border-radius: 20px; padding: 40px 32px;
  box-shadow: 0 2px 16px rgba(15,32,68,.08); border: 1.5px solid #bbf7d0;
  text-align: center; display: flex; flex-direction: column; align-items: center; gap: 12px;
}
.success-icon { width: 72px; height: 72px; border-radius: 50%; background: #f0fdf4; color: #16a34a; display: flex; align-items: center; justify-content: center; }
.success-icon svg { width: 36px; height: 36px; }
.success-card h3 { font-size: 22px; font-weight: 800; color: #16a34a; }
.success-card p { font-size: 14px; color: #64748b; }
.success-acct { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 10px 20px; font-size: 15px; font-weight: 700; color: #1e293b; letter-spacing: 1px; }
.new-balance { background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 10px; padding: 14px 24px; display: flex; flex-direction: column; align-items: center; gap: 4px; }
.bal-label { font-size: 11px; text-transform: uppercase; letter-spacing: .8px; color: #0284c7; font-weight: 600; }
.bal-value { font-size: 24px; font-weight: 800; color: #0f172a; }
.btn-new { width: 100%; padding: 12px; background: #f0fdf4; color: #16a34a; border: 1.5px solid #bbf7d0; border-radius: 10px; font-size: 14px; font-weight: 600; cursor: pointer; transition: background .18s; }
.btn-new:hover { background: #dcfce7; }
.link-dash { font-size: 13px; color: #2563eb; font-weight: 600; }

.info-panel { background: #fff; border-radius: 20px; padding: 28px; box-shadow: 0 2px 16px rgba(15,32,68,.08); border: 1.5px solid #e2e8f0; }
.info-title { font-size: 16px; font-weight: 700; color: #1e293b; margin-bottom: 16px; }
.info-rows { display: flex; flex-direction: column; }
.info-row { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #f1f5f9; font-size: 14px; color: #475569; }
.info-row:last-child { border-bottom: none; }
.val { font-weight: 600; color: #1e293b; }
.val.free { color: #16a34a; }
.tip-box { margin-top: 20px; padding: 14px 16px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 10px; font-size: 13px; color: #1d4ed8; display: flex; gap: 10px; align-items: flex-start; }
.tip-box svg { width: 18px; height: 18px; flex-shrink: 0; margin-top: 1px; }

.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,.3); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 700px) { .transfer-layout { grid-template-columns: 1fr; } }
</style>
