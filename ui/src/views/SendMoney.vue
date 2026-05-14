<template>
  <div class="page">
    <div class="transfer-layout">

      <!-- Left: form -->
      <div class="form-card">
        <div class="card-icon blue">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
        </div>
        <h2 class="card-title">Send Money</h2>
        <p class="card-sub">Transfer funds instantly to any account</p>

        <form @submit.prevent="sendMoney" class="form">
          <div class="amount-field">
            <label>Amount</label>
            <div class="amount-wrap">
              <span class="currency">₹</span>
              <input v-model="amount" type="number" min="1" step="0.01" placeholder="0.00" required class="amount-input" />
            </div>
          </div>

          <div class="field">
            <label>Recipient Account Number</label>
            <input v-model="recipient" type="text" placeholder="16-digit account number" maxlength="16" required />
            <span class="hint">Double-check the account number before sending</span>
          </div>

          <div v-if="error" class="alert-error">{{ error }}</div>

          <button type="submit" class="btn-send" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
            {{ loading ? 'Processing…' : 'Send Money' }}
          </button>
        </form>
      </div>

      <!-- Right: success state or info -->
      <div v-if="success" class="success-card">
        <div class="success-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        </div>
        <h3>Transfer Successful!</h3>
        <p>₹ {{ formatAmount(lastAmount) }} sent to</p>
        <div class="success-acct">{{ lastRecipient }}</div>
        <p class="success-time">{{ new Date().toLocaleString('en-IN') }}</p>
        <button class="btn-new" @click="resetForm">Make Another Transfer</button>
        <RouterLink to="/TransactionStatement" class="link-stmt">View Transaction History →</RouterLink>
      </div>

      <div v-else class="info-panel">
        <h3 class="info-title">Transfer Details</h3>
        <div class="info-rows">
          <div class="info-row"><span>Processing Time</span><span class="val">Instant</span></div>
          <div class="info-row"><span>Transfer Limit</span><span class="val">No limit</span></div>
          <div class="info-row"><span>Charges</span><span class="val free">Free</span></div>
          <div class="info-row"><span>Availability</span><span class="val">24 × 7</span></div>
        </div>
        <div class="warning-box">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          Always verify the recipient's account number. Transfers cannot be reversed.
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

export default {
  data() {
    return { amount: '', recipient: '', error: '', loading: false, success: false, lastAmount: '', lastRecipient: '' };
  },
  methods: {
    async sendMoney() {
      this.error = '';
      this.loading = true;
      try {
        await apiClient.post('/transactions/send-money/', {
          recipient_account_number: this.recipient,
          amount: this.amount,
        });
        this.lastAmount = this.amount;
        this.lastRecipient = this.recipient;
        this.success = true;
      } catch (err) {
        this.error = err.response?.data?.error || 'Transfer failed. Please try again.';
      } finally {
        this.loading = false;
      }
    },
    resetForm() {
      this.amount = ''; this.recipient = ''; this.success = false; this.error = '';
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
.card-icon {
  width: 52px; height: 52px; border-radius: 14px;
  display: flex; align-items: center; justify-content: center; margin-bottom: 20px;
}
.card-icon svg { width: 24px; height: 24px; }
.card-icon.blue { background: #eff6ff; color: #2563eb; }

.card-title { font-size: 22px; font-weight: 800; color: #1e293b; margin-bottom: 6px; }
.card-sub { font-size: 13px; color: #64748b; margin-bottom: 28px; }

.form { display: flex; flex-direction: column; gap: 20px; }

.amount-field { display: flex; flex-direction: column; gap: 6px; }
.amount-field label { font-size: 12px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: .6px; }
.amount-wrap {
  display: flex; align-items: center;
  border: 2px solid #2563eb; border-radius: 12px;
  background: #eff6ff; overflow: hidden;
}
.currency {
  padding: 0 16px; font-size: 22px; font-weight: 700; color: #2563eb;
  border-right: 2px solid #bfdbfe;
}
.amount-input {
  flex: 1; border: none; background: transparent;
  padding: 16px 16px; font-size: 26px; font-weight: 700; color: #1e293b;
  outline: none; min-width: 0;
}
.amount-input::placeholder { color: #cbd5e1; }

.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 12px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: .6px; }
.field input {
  padding: 12px 14px; border: 1.5px solid #e2e8f0; border-radius: 10px;
  font-size: 15px; color: #1e293b; background: #f8fafc;
  outline: none; transition: border-color .18s, box-shadow .18s;
}
.field input:focus { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,.1); background: #fff; }
.hint { font-size: 11px; color: #94a3b8; }

.alert-error { padding: 11px 14px; border-radius: 8px; font-size: 13px; background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }

.btn-send {
  width: 100%; padding: 14px; background: #2563eb; color: #fff;
  border: none; border-radius: 10px; font-size: 15px; font-weight: 700;
  cursor: pointer; transition: background .18s, transform .1s;
  display: flex; align-items: center; justify-content: center; gap: 8px;
}
.btn-send svg { width: 18px; height: 18px; }
.btn-send:hover:not(:disabled) { background: #1d4ed8; }
.btn-send:active:not(:disabled) { transform: scale(.98); }
.btn-send:disabled { opacity: .6; cursor: not-allowed; }

/* Success */
.success-card {
  background: #fff; border-radius: 20px; padding: 40px 32px;
  box-shadow: 0 2px 16px rgba(15,32,68,.08); border: 1.5px solid #bbf7d0;
  text-align: center; display: flex; flex-direction: column; align-items: center; gap: 12px;
}
.success-icon {
  width: 72px; height: 72px; border-radius: 50%;
  background: #f0fdf4; color: #16a34a;
  display: flex; align-items: center; justify-content: center; margin-bottom: 4px;
}
.success-icon svg { width: 36px; height: 36px; }
.success-card h3 { font-size: 22px; font-weight: 800; color: #16a34a; }
.success-card p { font-size: 14px; color: #64748b; }
.success-acct {
  background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px;
  padding: 10px 20px; font-size: 15px; font-weight: 700; color: #1e293b;
  letter-spacing: 1px;
}
.success-time { font-size: 12px; color: #94a3b8; }

.btn-new {
  width: 100%; padding: 12px; background: #f0fdf4; color: #16a34a;
  border: 1.5px solid #bbf7d0; border-radius: 10px; font-size: 14px; font-weight: 600;
  cursor: pointer; transition: background .18s;
}
.btn-new:hover { background: #dcfce7; }
.link-stmt { font-size: 13px; color: #2563eb; font-weight: 600; }

/* Info panel */
.info-panel {
  background: #fff; border-radius: 20px; padding: 28px;
  box-shadow: 0 2px 16px rgba(15,32,68,.08); border: 1.5px solid #e2e8f0;
}
.info-title { font-size: 16px; font-weight: 700; color: #1e293b; margin-bottom: 16px; }
.info-rows { display: flex; flex-direction: column; gap: 0; }
.info-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 12px 0; border-bottom: 1px solid #f1f5f9;
  font-size: 14px; color: #475569;
}
.info-row:last-child { border-bottom: none; }
.val { font-weight: 600; color: #1e293b; }
.val.free { color: #16a34a; }

.warning-box {
  margin-top: 20px; padding: 14px 16px; background: #fffbeb;
  border: 1px solid #fde68a; border-radius: 10px;
  font-size: 13px; color: #92400e; display: flex; gap: 10px; align-items: flex-start;
}
.warning-box svg { width: 18px; height: 18px; flex-shrink: 0; margin-top: 1px; color: #d97706; }

.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,.3); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 700px) {
  .transfer-layout { grid-template-columns: 1fr; }
}
</style>
