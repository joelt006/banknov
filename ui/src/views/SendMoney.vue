<template>
  <div class="page">
    <div class="transfer-layout">

      <!-- Left: form -->
      <div class="form-card">
        <div class="card-icon blue">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
        </div>
        <h2 class="card-title">Send Money</h2>
        <p class="card-sub">Transfer funds instantly or schedule for later</p>

        <!-- Beneficiary quick-select -->
        <div v-if="beneficiaries.length > 0" class="bene-strip">
          <div class="bene-strip-label">Quick Select</div>
          <div class="bene-chips">
            <button
              v-for="b in beneficiaries" :key="b.id"
              type="button"
              class="bene-chip"
              :class="{ selected: recipient === b.account_number }"
              @click="selectBeneficiary(b)"
            >
              <span class="bene-chip-avatar">{{ b.nickname[0].toUpperCase() }}</span>
              {{ b.nickname }}
            </button>
          </div>
        </div>

        <form @submit.prevent="submitForm" class="form">
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

          <div class="field">
            <label>Transaction PIN</label>
            <input v-model="transactionPin" type="password" maxlength="4" placeholder="Enter your 4-digit PIN" required inputmode="numeric" />
            <span class="hint">
              Don't have a PIN?
              <RouterLink to="/Security" style="color:#2563eb;font-weight:600">Set one in Security Settings</RouterLink>
            </span>
          </div>

          <!-- Schedule toggle -->
          <div class="schedule-toggle">
            <label class="toggle-label">
              <input type="checkbox" v-model="isScheduled" />
              <span class="toggle-track">
                <span class="toggle-thumb"></span>
              </span>
              Schedule for later
            </label>
          </div>

          <div v-if="isScheduled" class="field">
            <label>Date &amp; Time</label>
            <input v-model="scheduledAt" type="datetime-local" :min="minDateTime" required />
            <span class="hint">Transfer will be processed automatically at this time</span>
          </div>

          <div v-if="error" class="alert-error">{{ error }}</div>

          <button type="submit" class="btn-send" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <template v-if="isScheduled">
                <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
              </template>
              <template v-else>
                <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
              </template>
            </svg>
            {{ loading ? 'Processing…' : (isScheduled ? 'Schedule Transfer' : 'Send Money') }}
          </button>
        </form>
      </div>

      <!-- Right: success or info -->
      <div v-if="success" class="success-card">
        <div class="success-icon" :class="{ scheduled: lastScheduled }">
          <svg v-if="lastScheduled" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        </div>
        <h3>{{ lastScheduled ? 'Transfer Scheduled!' : 'Transfer Successful!' }}</h3>
        <p v-if="lastScheduled">₹ {{ formatAmount(lastAmount) }} will be sent to</p>
        <p v-else>₹ {{ formatAmount(lastAmount) }} sent to</p>
        <div class="success-acct">{{ lastRecipient }}</div>
        <p v-if="lastScheduled" class="success-time">Scheduled for: {{ formatScheduled(lastScheduledAt) }}</p>
        <p v-else class="success-time">{{ new Date().toLocaleString('en-IN') }}</p>
        <button class="btn-new" @click="resetForm">Make Another Transfer</button>
        <RouterLink v-if="!lastScheduled" to="/TransactionStatement" class="link-stmt">View Transaction History →</RouterLink>
        <RouterLink v-else to="/ScheduledTransfers" class="link-stmt">View Scheduled Transfers →</RouterLink>
      </div>

      <div v-else class="info-panel">
        <h3 class="info-title">Transfer Details</h3>
        <div class="info-rows">
          <div class="info-row"><span>Processing Time</span><span class="val">Instant</span></div>
          <div class="info-row"><span>Transfer Limit</span><span class="val">No limit</span></div>
          <div class="info-row"><span>Charges</span><span class="val free">Free</span></div>
          <div class="info-row"><span>Availability</span><span class="val">24 × 7</span></div>
        </div>
        <div class="info-tip">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          Save frequent recipients as <RouterLink to="/Beneficiaries" style="color:#2563eb;font-weight:600">Beneficiaries</RouterLink> for quick selection.
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
    return {
      amount: '', recipient: '', transactionPin: '', error: '', loading: false, success: false,
      lastAmount: '', lastRecipient: '', lastScheduled: false, lastScheduledAt: '',
      isScheduled: false, scheduledAt: '',
      beneficiaries: [],
    };
  },
  computed: {
    minDateTime() {
      const d = new Date(Date.now() + 60000);
      return d.toISOString().slice(0, 16);
    },
  },
  mounted() {
    this.fetchBeneficiaries();
    const toAcct = this.$route.query.to;
    if (toAcct) this.recipient = toAcct;
  },
  methods: {
    async fetchBeneficiaries() {
      try {
        const res = await apiClient.get('/transactions/beneficiaries/');
        this.beneficiaries = res.data;
      } catch { /* silent */ }
    },
    selectBeneficiary(b) {
      this.recipient = b.account_number;
    },
    async submitForm() {
      this.error = '';
      this.loading = true;
      try {
        if (this.isScheduled) {
          await apiClient.post('/transactions/scheduled/', {
            recipient_account_number: this.recipient,
            amount: this.amount,
            scheduled_at: this.scheduledAt,
            transaction_pin: this.transactionPin,
          });
          this.lastAmount = this.amount;
          this.lastRecipient = this.recipient;
          this.lastScheduled = true;
          this.lastScheduledAt = this.scheduledAt;
        } else {
          await apiClient.post('/transactions/send-money/', {
            recipient_account_number: this.recipient,
            amount: this.amount,
            transaction_pin: this.transactionPin,
          });
          this.lastAmount = this.amount;
          this.lastRecipient = this.recipient;
          this.lastScheduled = false;
        }
        this.success = true;
      } catch (err) {
        this.error = err.response?.data?.error || 'Transfer failed. Please try again.';
      } finally {
        this.loading = false;
      }
    },
    resetForm() {
      this.amount = ''; this.recipient = ''; this.transactionPin = '';
      this.success = false; this.error = ''; this.isScheduled = false; this.scheduledAt = '';
    },
    formatAmount(val) {
      return parseFloat(val || 0).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },
    formatScheduled(iso) {
      if (!iso) return '';
      return new Date(iso).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' });
    },
  },
};
</script>

<style scoped>
.page { max-width: 900px; margin: 0 auto; }

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
.card-sub { font-size: 13px; color: #64748b; margin-bottom: 20px; }

/* Beneficiary chips */
.bene-strip { margin-bottom: 20px; }
.bene-strip-label { font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: .6px; margin-bottom: 8px; }
.bene-chips { display: flex; flex-wrap: wrap; gap: 8px; }
.bene-chip {
  display: flex; align-items: center; gap: 6px;
  padding: 6px 12px 6px 6px; border-radius: 20px;
  border: 1.5px solid #e2e8f0; background: #f8fafc;
  font-size: 13px; font-weight: 600; color: #334155; cursor: pointer; transition: all .15s;
}
.bene-chip-avatar {
  width: 24px; height: 24px; border-radius: 50%;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  color: #fff; font-size: 11px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
.bene-chip:hover { border-color: #93c5fd; background: #eff6ff; }
.bene-chip.selected { border-color: #2563eb; background: #eff6ff; color: #2563eb; }

.form { display: flex; flex-direction: column; gap: 20px; }

.amount-field { display: flex; flex-direction: column; gap: 6px; }
.amount-field label { font-size: 12px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: .6px; }
.amount-wrap {
  display: flex; align-items: center;
  border: 2px solid #2563eb; border-radius: 12px;
  background: #eff6ff; overflow: hidden;
}
.currency { padding: 0 16px; font-size: 22px; font-weight: 700; color: #2563eb; border-right: 2px solid #bfdbfe; }
.amount-input { flex: 1; border: none; background: transparent; padding: 16px; font-size: 26px; font-weight: 700; color: #1e293b; outline: none; min-width: 0; }
.amount-input::placeholder { color: #cbd5e1; }

.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 12px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: .6px; }
.field input {
  padding: 12px 14px; border: 1.5px solid #e2e8f0; border-radius: 10px;
  font-size: 15px; color: #1e293b; background: #f8fafc; outline: none; transition: border-color .18s;
}
.field input:focus { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,.1); background: #fff; }
.hint { font-size: 11px; color: #94a3b8; }

/* Schedule toggle */
.schedule-toggle { display: flex; align-items: center; }
.toggle-label { display: flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 600; color: #334155; cursor: pointer; }
.toggle-label input[type="checkbox"] { display: none; }
.toggle-track {
  width: 42px; height: 24px; background: #e2e8f0; border-radius: 12px;
  position: relative; transition: background .2s; flex-shrink: 0;
}
.toggle-thumb {
  width: 18px; height: 18px; background: #fff; border-radius: 50%;
  position: absolute; top: 3px; left: 3px; transition: transform .2s;
  box-shadow: 0 1px 4px rgba(0,0,0,.2);
}
.toggle-label input:checked + .toggle-track { background: #2563eb; }
.toggle-label input:checked + .toggle-track .toggle-thumb { transform: translateX(18px); }

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
.success-icon.scheduled { background: #eff6ff; color: #2563eb; }
.success-icon svg { width: 36px; height: 36px; }
.success-card h3 { font-size: 22px; font-weight: 800; color: #16a34a; }
.success-icon.scheduled + h3 { color: #2563eb; }
.success-card p { font-size: 14px; color: #64748b; }
.success-acct {
  background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px;
  padding: 10px 20px; font-size: 15px; font-weight: 700; color: #1e293b; letter-spacing: 1px;
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
  padding: 12px 0; border-bottom: 1px solid #f1f5f9; font-size: 14px; color: #475569;
}
.info-row:last-child { border-bottom: none; }
.val { font-weight: 600; color: #1e293b; }
.val.free { color: #16a34a; }

.info-tip {
  margin-top: 16px; padding: 12px 14px; background: #eff6ff;
  border: 1px solid #bfdbfe; border-radius: 10px;
  font-size: 13px; color: #1e40af; display: flex; gap: 8px; align-items: flex-start;
}
.info-tip svg { width: 16px; height: 16px; flex-shrink: 0; margin-top: 1px; }

.warning-box {
  margin-top: 14px; padding: 14px 16px; background: #fffbeb;
  border: 1px solid #fde68a; border-radius: 10px;
  font-size: 13px; color: #92400e; display: flex; gap: 10px; align-items: flex-start;
}
.warning-box svg { width: 18px; height: 18px; flex-shrink: 0; margin-top: 1px; color: #d97706; }

.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,.3); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 700px) { .transfer-layout { grid-template-columns: 1fr; } }
</style>
