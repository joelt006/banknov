<template>
  <div class="page">

    <!-- Tabs -->
    <div class="tab-bar">
      <button class="tab" :class="{ active: tab === 'list' }" @click="tab = 'list'">My Loans</button>
      <button class="tab" :class="{ active: tab === 'apply' }" @click="tab = 'apply'">Apply for Loan</button>
    </div>

    <!-- ── My Loans ── -->
    <template v-if="tab === 'list'">
      <div v-if="loading" class="state-load"><div class="spinner"></div> Loading…</div>
      <div v-else-if="loans.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="#cbd5e1" stroke-width="1.5"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
        <p>No loan applications yet.</p>
        <button class="btn-primary" @click="tab = 'apply'">Apply Now</button>
      </div>
      <div v-else class="loans-list">
        <div v-for="l in loans" :key="l.id" class="loan-card" :class="l.status">
          <div class="loan-top">
            <div class="loan-type-badge" :class="'type-' + l.loan_type">
              {{ loanLabel(l.loan_type) }}
            </div>
            <span class="status-badge" :class="'s-' + l.status">{{ capitalize(l.status) }}</span>
          </div>
          <div class="loan-amount">₹ {{ fmt(l.approved_amount || l.amount) }}</div>
          <div class="loan-meta-grid">
            <div class="meta-item"><span>Applied Amount</span><strong>₹ {{ fmt(l.amount) }}</strong></div>
            <div class="meta-item"><span>Tenure</span><strong>{{ l.tenure_months }} months</strong></div>
            <div class="meta-item"><span>Interest Rate</span><strong>{{ l.interest_rate }}% p.a.</strong></div>
            <div class="meta-item"><span>Monthly EMI</span><strong>₹ {{ fmt(l.monthly_emi) }}</strong></div>
          </div>
          <div v-if="l.purpose" class="loan-purpose">Purpose: {{ l.purpose }}</div>
          <div v-if="l.admin_note" class="loan-note">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            {{ l.admin_note }}
          </div>
          <div class="loan-footer">Applied {{ formatDate(l.applied_at) }}
            <span v-if="l.reviewed_at"> · Reviewed {{ formatDate(l.reviewed_at) }}</span>
          </div>
        </div>
      </div>
    </template>

    <!-- ── Apply ── -->
    <template v-else>
      <div class="apply-layout">
        <!-- Form -->
        <div class="form-card">
          <div class="card-icon green">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
          </div>
          <h2 class="form-title">Loan Application</h2>
          <p class="form-sub">Fill in the details and we'll review your application</p>

          <form @submit.prevent="applyLoan" class="form">
            <div class="field">
              <label>Loan Type</label>
              <select v-model="form.loan_type" required>
                <option value="">Select type</option>
                <option value="personal">Personal Loan — 12% p.a.</option>
                <option value="home">Home Loan — 8.5% p.a.</option>
                <option value="car">Car Loan — 9% p.a.</option>
                <option value="education">Education Loan — 8% p.a.</option>
              </select>
            </div>
            <div class="field">
              <label>Loan Amount (₹)</label>
              <input v-model="form.amount" type="number" min="1000" step="1000" placeholder="Min ₹1,000" required />
            </div>
            <div class="field">
              <label>Tenure</label>
              <select v-model="form.tenure_months" required>
                <option value="">Select tenure</option>
                <option :value="12">1 Year (12 months)</option>
                <option :value="24">2 Years (24 months)</option>
                <option :value="36">3 Years (36 months)</option>
                <option :value="60">5 Years (60 months)</option>
                <option :value="84">7 Years (84 months)</option>
                <option :value="120">10 Years (120 months)</option>
              </select>
            </div>
            <div class="field">
              <label>Purpose <span class="optional">(optional)</span></label>
              <textarea v-model="form.purpose" rows="2" placeholder="Briefly describe the purpose…"></textarea>
            </div>

            <!-- Live EMI preview -->
            <div v-if="emiPreview" class="emi-preview">
              <div class="emi-row"><span>Interest Rate</span><strong>{{ rateFor(form.loan_type) }}% p.a.</strong></div>
              <div class="emi-row"><span>Estimated Monthly EMI</span><strong class="emi-val">₹ {{ emiPreview }}</strong></div>
              <div class="emi-row"><span>Total Payable</span><strong>₹ {{ totalPayable }}</strong></div>
            </div>

            <div v-if="form.error" class="alert-error">{{ form.error }}</div>
            <div v-if="form.success" class="alert-success">{{ form.success }}</div>

            <button type="submit" class="btn-submit" :disabled="form.loading">
              <span v-if="form.loading" class="btn-spinner"></span>
              {{ form.loading ? 'Submitting…' : 'Submit Application' }}
            </button>
          </form>
        </div>

        <!-- Info panel -->
        <div class="info-panel">
          <h3 class="info-title">Loan Products</h3>
          <div v-for="p in loanProducts" :key="p.type" class="product-row">
            <div class="product-icon" :class="'pi-' + p.type">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" v-html="p.icon"></svg>
            </div>
            <div>
              <div class="product-name">{{ p.name }}</div>
              <div class="product-rate">{{ p.rate }}% p.a. · Up to {{ p.max }}</div>
            </div>
          </div>
          <div class="info-note">
            Applications are reviewed within 2–3 business days. Approved loan amount is credited directly to your account.
          </div>
        </div>
      </div>
    </template>

  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

const RATES = { personal: 12, home: 8.5, car: 9, education: 8 };

export default {
  data() {
    return {
      tab: 'list',
      loans: [],
      loading: true,
      form: { loan_type: '', amount: '', tenure_months: '', purpose: '', error: '', success: '', loading: false },
      loanProducts: [
        { type: 'personal', name: 'Personal Loan', rate: 12,  max: '₹25L', icon: '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>' },
        { type: 'home',     name: 'Home Loan',     rate: 8.5, max: '₹1Cr', icon: '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>' },
        { type: 'car',      name: 'Car Loan',      rate: 9,   max: '₹50L', icon: '<rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>' },
        { type: 'education',name: 'Education Loan',rate: 8,   max: '₹20L', icon: '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>' },
      ],
    };
  },
  computed: {
    emiPreview() {
      if (!this.form.loan_type || !this.form.amount || !this.form.tenure_months) return null;
      const p = parseFloat(this.form.amount);
      const r = RATES[this.form.loan_type] / 100 / 12;
      const n = parseInt(this.form.tenure_months);
      if (!p || !n || p <= 0) return null;
      const emi = p * r * Math.pow(1 + r, n) / (Math.pow(1 + r, n) - 1);
      return isNaN(emi) ? null : emi.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },
    totalPayable() {
      if (!this.emiPreview) return null;
      const emi = parseFloat(this.emiPreview.replace(/,/g, ''));
      const total = emi * parseInt(this.form.tenure_months);
      return total.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },
  },
  async created() {
    await this.fetchLoans();
  },
  methods: {
    async fetchLoans() {
      this.loading = true;
      try {
        const res = await apiClient.get('/accounts/loans/');
        this.loans = res.data;
      } catch { this.loans = []; } finally { this.loading = false; }
    },
    async applyLoan() {
      this.form.error = ''; this.form.success = '';
      this.form.loading = true;
      try {
        const res = await apiClient.post('/accounts/loans/', {
          loan_type: this.form.loan_type,
          amount: this.form.amount,
          tenure_months: this.form.tenure_months,
          purpose: this.form.purpose,
        });
        this.loans.unshift(res.data);
        this.form.success = 'Application submitted! We'll review it within 2–3 business days.';
        this.form.loan_type = ''; this.form.amount = ''; this.form.tenure_months = ''; this.form.purpose = '';
        setTimeout(() => { this.tab = 'list'; }, 1500);
      } catch (err) {
        this.form.error = err.response?.data?.error || 'Failed to submit application.';
      } finally { this.form.loading = false; }
    },
    loanLabel(t) { return { personal: 'Personal', home: 'Home', car: 'Car', education: 'Education' }[t] || t; },
    rateFor(t) { return RATES[t] || ''; },
    fmt(v) { return v ? parseFloat(v).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : '—'; },
    formatDate(iso) { return new Date(iso).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }); },
    capitalize(s) { return s.charAt(0).toUpperCase() + s.slice(1); },
  },
};
</script>

<style scoped>
.page { display: flex; flex-direction: column; gap: 20px; max-width: 900px; margin: 0 auto; }

.tab-bar { display: flex; gap: 4px; background: #f1f5f9; border-radius: 10px; padding: 4px; width: fit-content; }
.tab { padding: 8px 20px; border-radius: 8px; border: none; font-size: 14px; font-weight: 600; color: #64748b; cursor: pointer; background: transparent; transition: all .15s; }
.tab.active { background: #fff; color: #1e293b; box-shadow: 0 1px 4px rgba(0,0,0,.08); }

.state-load { display: flex; align-items: center; gap: 10px; color: #64748b; font-size: 14px; padding: 32px 0; }
.spinner { width: 18px; height: 18px; border: 2px solid #e2e8f0; border-top-color: #2563eb; border-radius: 50%; animation: spin .6s linear infinite; display: inline-block; }
@keyframes spin { to { transform: rotate(360deg); } }

.empty-state { display: flex; flex-direction: column; align-items: center; gap: 14px; padding: 60px 0; color: #94a3b8; font-size: 14px; }
.empty-state svg { width: 56px; height: 56px; }

.loans-list { display: flex; flex-direction: column; gap: 16px; }
.loan-card { background: #fff; border-radius: 16px; padding: 24px; border: 1.5px solid #e2e8f0; box-shadow: 0 2px 8px rgba(15,32,68,.06); }
.loan-card.active   { border-color: #bbf7d0; }
.loan-card.approved { border-color: #bbf7d0; }
.loan-card.rejected { border-color: #fecaca; }
.loan-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.loan-type-badge { padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; }
.type-personal  { background: #eff6ff; color: #2563eb; }
.type-home      { background: #f0fdf4; color: #16a34a; }
.type-car       { background: #fffbeb; color: #d97706; }
.type-education { background: #f5f3ff; color: #7c3aed; }
.status-badge { padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; }
.s-pending  { background: #fef3c7; color: #d97706; }
.s-approved, .s-active { background: #dcfce7; color: #16a34a; }
.s-rejected { background: #fee2e2; color: #dc2626; }
.s-closed   { background: #f1f5f9; color: #64748b; }
.loan-amount { font-size: 32px; font-weight: 800; color: #1e293b; margin-bottom: 16px; }
.loan-meta-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 12px; }
.meta-item { display: flex; flex-direction: column; gap: 3px; }
.meta-item span { font-size: 11px; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: .4px; }
.meta-item strong { font-size: 14px; color: #1e293b; font-weight: 700; }
.loan-purpose { font-size: 13px; color: #64748b; margin-bottom: 8px; }
.loan-note { display: flex; align-items: flex-start; gap: 8px; padding: 10px 14px; background: #fffbeb; border-radius: 8px; font-size: 13px; color: #92400e; margin-bottom: 8px; }
.loan-note svg { width: 15px; height: 15px; flex-shrink: 0; margin-top: 1px; }
.loan-footer { font-size: 12px; color: #94a3b8; }

/* Apply layout */
.apply-layout { display: grid; grid-template-columns: 1fr 340px; gap: 24px; align-items: start; }
.form-card { background: #fff; border-radius: 20px; padding: 28px; border: 1.5px solid #e2e8f0; box-shadow: 0 2px 12px rgba(15,32,68,.07); }
.card-icon { width: 48px; height: 48px; border-radius: 13px; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; }
.card-icon svg { width: 22px; height: 22px; }
.card-icon.green { background: #f0fdf4; color: #16a34a; }
.form-title { font-size: 20px; font-weight: 800; color: #1e293b; margin-bottom: 4px; }
.form-sub { font-size: 13px; color: #64748b; margin-bottom: 24px; }
.form { display: flex; flex-direction: column; gap: 16px; }
.field { display: flex; flex-direction: column; gap: 5px; }
.field label { font-size: 12px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: .6px; }
.optional { text-transform: none; font-weight: 400; color: #94a3b8; }
.field input, .field select, .field textarea {
  padding: 11px 14px; border: 1.5px solid #e2e8f0; border-radius: 10px;
  font-size: 14px; color: #1e293b; background: #f8fafc; outline: none; transition: border-color .18s; font-family: inherit;
}
.field input:focus, .field select:focus, .field textarea:focus { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,.1); background: #fff; }
.field textarea { resize: vertical; min-height: 60px; }

.emi-preview { background: #f0fdf4; border: 1.5px solid #bbf7d0; border-radius: 10px; padding: 14px 16px; display: flex; flex-direction: column; gap: 8px; }
.emi-row { display: flex; justify-content: space-between; font-size: 13px; color: #475569; }
.emi-val { color: #16a34a; font-size: 16px; }

.alert-error   { padding: 10px 14px; border-radius: 8px; font-size: 13px; background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
.alert-success { padding: 10px 14px; border-radius: 8px; font-size: 13px; background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }

.btn-submit { width: 100%; padding: 13px; background: #16a34a; color: #fff; border: none; border-radius: 10px; font-size: 15px; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; transition: background .18s; }
.btn-submit:hover:not(:disabled) { background: #15803d; }
.btn-submit:disabled { opacity: .6; cursor: not-allowed; }
.btn-spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,.3); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; }

.btn-primary { padding: 10px 24px; background: #2563eb; color: #fff; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; }

/* Info panel */
.info-panel { background: #fff; border-radius: 20px; padding: 24px; border: 1.5px solid #e2e8f0; box-shadow: 0 2px 12px rgba(15,32,68,.07); }
.info-title { font-size: 15px; font-weight: 800; color: #1e293b; margin-bottom: 16px; }
.product-row { display: flex; align-items: center; gap: 12px; padding: 12px 0; border-bottom: 1px solid #f1f5f9; }
.product-row:last-of-type { border-bottom: none; }
.product-icon { width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.product-icon svg { width: 18px; height: 18px; }
.pi-personal  { background: #eff6ff; color: #2563eb; }
.pi-home      { background: #f0fdf4; color: #16a34a; }
.pi-car       { background: #fffbeb; color: #d97706; }
.pi-education { background: #f5f3ff; color: #7c3aed; }
.product-name { font-size: 14px; font-weight: 700; color: #1e293b; }
.product-rate { font-size: 12px; color: #64748b; margin-top: 2px; }
.info-note { margin-top: 16px; padding: 12px 14px; background: #f8fafc; border-radius: 8px; font-size: 12px; color: #64748b; line-height: 1.5; }

@media (max-width: 720px) {
  .apply-layout { grid-template-columns: 1fr; }
  .loan-meta-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
