<template>
  <div class="page">

    <!-- Tabs -->
    <div class="tab-bar">
      <button class="tab" :class="{ active: tab === 'list' }" @click="tab = 'list'">My FDs</button>
      <button class="tab" :class="{ active: tab === 'open' }" @click="tab = 'open'">Open New FD</button>
    </div>

    <!-- ── My FDs ── -->
    <template v-if="tab === 'list'">
      <div v-if="loading" class="state-load"><div class="spinner"></div> Loading…</div>
      <div v-else-if="fds.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="#cbd5e1" stroke-width="1.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        <p>No fixed deposits yet.</p>
        <button class="btn-primary" @click="tab = 'open'">Open FD</button>
      </div>
      <div v-else class="fd-grid">
        <div v-for="fd in fds" :key="fd.id" class="fd-card" :class="fd.status">
          <div class="fd-top">
            <div class="fd-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            </div>
            <div>
              <div class="fd-label">Fixed Deposit</div>
              <div class="fd-tenure">{{ tenureLabel(fd.tenure_months) }} · {{ fd.interest_rate }}% p.a.</div>
            </div>
            <span class="fd-status-badge" :class="'fs-' + fd.status">{{ capitalize(fd.status) }}</span>
          </div>

          <div class="fd-amounts">
            <div class="fd-amt-item">
              <span>Principal</span>
              <strong>₹ {{ fmt(fd.amount) }}</strong>
            </div>
            <div class="fd-amt-sep">→</div>
            <div class="fd-amt-item">
              <span>At Maturity</span>
              <strong class="maturity-val">₹ {{ fmt(fd.maturity_amount) }}</strong>
            </div>
          </div>

          <div class="fd-dates">
            <div class="fd-date-item">
              <span>Start Date</span>
              <strong>{{ fd.start_date }}</strong>
            </div>
            <div class="fd-date-item">
              <span>Maturity Date</span>
              <strong>{{ fd.maturity_date }}</strong>
            </div>
            <div class="fd-date-item">
              <span>Interest Earned</span>
              <strong class="interest-val">+ ₹ {{ fmt((parseFloat(fd.maturity_amount) - parseFloat(fd.amount)).toFixed(2)) }}</strong>
            </div>
          </div>

          <div v-if="fd.status === 'active'" class="fd-progress">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: progressPct(fd) + '%' }"></div>
            </div>
            <div class="progress-label">{{ progressPct(fd) }}% complete · {{ daysLeft(fd) }} days remaining</div>
          </div>

          <button
            v-if="fd.status === 'active'"
            class="btn-close-fd"
            @click="closeFD(fd)"
            :disabled="closing === fd.id"
          >
            {{ closing === fd.id ? 'Processing…' : (isPremature(fd) ? 'Close Prematurely (1% penalty)' : 'Claim Maturity Amount') }}
          </button>
        </div>
      </div>
    </template>

    <!-- ── Open FD ── -->
    <template v-else>
      <div class="apply-layout">
        <div class="form-card">
          <div class="card-icon amber">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          </div>
          <h2 class="form-title">Open Fixed Deposit</h2>
          <p class="form-sub">Earn guaranteed returns on your savings</p>

          <form @submit.prevent="openFD" class="form">
            <div class="field">
              <label>Deposit Amount (₹)</label>
              <input v-model="form.amount" type="number" min="1000" step="500" placeholder="Min ₹1,000" required />
            </div>
            <div class="field">
              <label>Tenure</label>
              <div class="tenure-chips">
                <button
                  v-for="opt in tenureOptions" :key="opt.value"
                  type="button"
                  class="tenure-chip"
                  :class="{ selected: form.tenure_months === opt.value }"
                  @click="form.tenure_months = opt.value"
                >
                  <span class="chip-label">{{ opt.label }}</span>
                  <span class="chip-rate">{{ opt.rate }}%</span>
                </button>
              </div>
            </div>

            <!-- Live preview -->
            <div v-if="fdPreview" class="fd-preview">
              <div class="preview-row"><span>Principal Amount</span><strong>₹ {{ fmtN(form.amount) }}</strong></div>
              <div class="preview-row"><span>Interest Rate</span><strong>{{ fdPreview.rate }}% p.a.</strong></div>
              <div class="preview-row"><span>Maturity Date</span><strong>{{ fdPreview.maturityDate }}</strong></div>
              <div class="preview-row highlight"><span>Maturity Amount</span><strong>₹ {{ fdPreview.maturityAmt }}</strong></div>
              <div class="preview-row earn"><span>You Earn</span><strong>+ ₹ {{ fdPreview.interest }}</strong></div>
            </div>

            <div v-if="form.error" class="alert-error">{{ form.error }}</div>
            <div v-if="form.success" class="alert-success">{{ form.success }}</div>

            <button type="submit" class="btn-submit" :disabled="form.loading || !form.tenure_months">
              <span v-if="form.loading" class="btn-spinner"></span>
              {{ form.loading ? 'Opening FD…' : 'Open Fixed Deposit' }}
            </button>
            <p class="deduct-note">Amount will be deducted from your account balance.</p>
          </form>
        </div>

        <!-- Rate card -->
        <div class="rate-card">
          <h3 class="rate-title">Interest Rates</h3>
          <table class="rate-table">
            <thead><tr><th>Tenure</th><th>Rate (p.a.)</th></tr></thead>
            <tbody>
              <tr v-for="opt in tenureOptions" :key="opt.value" :class="{ 'row-selected': form.tenure_months === opt.value }">
                <td>{{ opt.label }}</td>
                <td class="rate-val">{{ opt.rate }}%</td>
              </tr>
            </tbody>
          </table>
          <div class="rate-note">Interest compounded annually. Early closure incurs a 1% penalty on interest earned.</div>
        </div>
      </div>
    </template>

  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

const FD_RATES = { 3: 4.5, 6: 5.5, 12: 6.5, 24: 7.0, 36: 7.25, 60: 7.5 };

export default {
  data() {
    return {
      tab: 'list',
      fds: [],
      loading: true,
      closing: null,
      form: { amount: '', tenure_months: null, error: '', success: '', loading: false },
      tenureOptions: [
        { value: 3,  label: '3 Months', rate: 4.5 },
        { value: 6,  label: '6 Months', rate: 5.5 },
        { value: 12, label: '1 Year',   rate: 6.5 },
        { value: 24, label: '2 Years',  rate: 7.0 },
        { value: 36, label: '3 Years',  rate: 7.25 },
        { value: 60, label: '5 Years',  rate: 7.5 },
      ],
    };
  },
  computed: {
    fdPreview() {
      const p = parseFloat(this.form.amount);
      const t = this.form.tenure_months;
      if (!p || !t || p <= 0) return null;
      const rate = FD_RATES[t];
      const years = t / 12;
      const maturity = p * Math.pow(1 + rate / 100, years);
      const today = new Date();
      const matDate = new Date(today);
      matDate.setMonth(matDate.getMonth() + t);
      return {
        rate,
        maturityDate: matDate.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }),
        maturityAmt: maturity.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
        interest: (maturity - p).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
      };
    },
  },
  async created() { await this.fetchFDs(); },
  methods: {
    async fetchFDs() {
      this.loading = true;
      try {
        const res = await apiClient.get('/accounts/fixed-deposits/');
        this.fds = res.data;
      } catch { this.fds = []; } finally { this.loading = false; }
    },
    async openFD() {
      this.form.error = ''; this.form.success = '';
      this.form.loading = true;
      try {
        const res = await apiClient.post('/accounts/fixed-deposits/', {
          amount: this.form.amount,
          tenure_months: this.form.tenure_months,
        });
        this.fds.unshift(res.data);
        this.form.success = 'Fixed deposit opened successfully!';
        this.form.amount = ''; this.form.tenure_months = null;
        setTimeout(() => { this.tab = 'list'; }, 1500);
      } catch (err) {
        this.form.error = err.response?.data?.error || 'Failed to open FD.';
      } finally { this.form.loading = false; }
    },
    async closeFD(fd) {
      const msg = this.isPremature(fd)
        ? 'Close this FD early? A 1% penalty on interest will be applied.'
        : 'Claim maturity amount and close this FD?';
      if (!confirm(msg)) return;
      this.closing = fd.id;
      try {
        const res = await apiClient.post(`/accounts/fixed-deposits/${fd.id}/close/`);
        fd.status = res.data.status;
        alert(`₹ ${parseFloat(res.data.credited).toLocaleString('en-IN', { minimumFractionDigits: 2 })} credited to your account.`);
      } catch (err) {
        alert(err.response?.data?.error || 'Failed to close FD.');
      } finally { this.closing = null; }
    },
    isPremature(fd) { return new Date() < new Date(fd.maturity_date); },
    progressPct(fd) {
      const start = new Date(fd.start_date).getTime();
      const end = new Date(fd.maturity_date).getTime();
      const now = Date.now();
      return Math.min(100, Math.round(((now - start) / (end - start)) * 100));
    },
    daysLeft(fd) {
      return Math.max(0, Math.ceil((new Date(fd.maturity_date) - Date.now()) / 86400000));
    },
    tenureLabel(m) { return { 3: '3 Months', 6: '6 Months', 12: '1 Year', 24: '2 Years', 36: '3 Years', 60: '5 Years' }[m] || `${m}M`; },
    fmt(v) { return v != null ? parseFloat(v).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : '—'; },
    fmtN(v) { return v ? parseFloat(v).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : '0.00'; },
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
.spinner { width: 18px; height: 18px; border: 2px solid #e2e8f0; border-top-color: #f59e0b; border-radius: 50%; animation: spin .6s linear infinite; display: inline-block; }
@keyframes spin { to { transform: rotate(360deg); } }

.empty-state { display: flex; flex-direction: column; align-items: center; gap: 14px; padding: 60px 0; color: #94a3b8; font-size: 14px; }
.empty-state svg { width: 56px; height: 56px; }
.btn-primary { padding: 10px 24px; background: #f59e0b; color: #fff; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; }

.fd-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 20px; }
.fd-card { background: #fff; border-radius: 16px; padding: 24px; border: 1.5px solid #e2e8f0; box-shadow: 0 2px 8px rgba(15,32,68,.06); display: flex; flex-direction: column; gap: 16px; }
.fd-card.active  { border-color: #fde68a; }
.fd-card.matured { border-color: #bbf7d0; }
.fd-card.closed  { border-color: #e2e8f0; opacity: .7; }

.fd-top { display: flex; align-items: center; gap: 12px; }
.fd-icon { width: 42px; height: 42px; border-radius: 12px; background: #fffbeb; color: #d97706; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.fd-icon svg { width: 20px; height: 20px; }
.fd-label { font-size: 14px; font-weight: 700; color: #1e293b; }
.fd-tenure { font-size: 12px; color: #64748b; margin-top: 2px; }
.fd-status-badge { margin-left: auto; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; }
.fs-active  { background: #fef3c7; color: #d97706; }
.fs-matured { background: #dcfce7; color: #16a34a; }
.fs-closed  { background: #f1f5f9; color: #64748b; }

.fd-amounts { display: flex; align-items: center; gap: 12px; padding: 14px; background: #f8fafc; border-radius: 10px; }
.fd-amt-item { flex: 1; display: flex; flex-direction: column; gap: 3px; }
.fd-amt-item span { font-size: 11px; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: .4px; }
.fd-amt-item strong { font-size: 18px; font-weight: 800; color: #1e293b; }
.maturity-val { color: #16a34a !important; }
.fd-amt-sep { font-size: 18px; color: #cbd5e1; }

.fd-dates { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.fd-date-item { display: flex; flex-direction: column; gap: 3px; }
.fd-date-item span { font-size: 11px; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: .4px; }
.fd-date-item strong { font-size: 13px; font-weight: 700; color: #1e293b; }
.interest-val { color: #16a34a !important; }

.fd-progress { display: flex; flex-direction: column; gap: 6px; }
.progress-bar { height: 6px; background: #f1f5f9; border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #f59e0b, #d97706); border-radius: 3px; transition: width .3s; }
.progress-label { font-size: 11px; color: #94a3b8; }

.btn-close-fd { padding: 10px; border-radius: 8px; border: 1.5px solid #fde68a; background: #fffbeb; color: #92400e; font-size: 13px; font-weight: 600; cursor: pointer; transition: background .15s; }
.btn-close-fd:hover:not(:disabled) { background: #fef3c7; }
.btn-close-fd:disabled { opacity: .6; cursor: not-allowed; }

/* Apply */
.apply-layout { display: grid; grid-template-columns: 1fr 280px; gap: 24px; align-items: start; }
.form-card { background: #fff; border-radius: 20px; padding: 28px; border: 1.5px solid #e2e8f0; box-shadow: 0 2px 12px rgba(15,32,68,.07); }
.card-icon { width: 48px; height: 48px; border-radius: 13px; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; }
.card-icon svg { width: 22px; height: 22px; }
.card-icon.amber { background: #fffbeb; color: #d97706; }
.form-title { font-size: 20px; font-weight: 800; color: #1e293b; margin-bottom: 4px; }
.form-sub { font-size: 13px; color: #64748b; margin-bottom: 24px; }
.form { display: flex; flex-direction: column; gap: 16px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 12px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: .6px; }
.field input { padding: 11px 14px; border: 1.5px solid #e2e8f0; border-radius: 10px; font-size: 14px; color: #1e293b; background: #f8fafc; outline: none; transition: border-color .18s; }
.field input:focus { border-color: #f59e0b; box-shadow: 0 0 0 3px rgba(245,158,11,.1); background: #fff; }

.tenure-chips { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.tenure-chip { padding: 10px 8px; border-radius: 10px; border: 1.5px solid #e2e8f0; background: #f8fafc; cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: 2px; transition: all .15s; }
.tenure-chip:hover { border-color: #fde68a; background: #fffbeb; }
.tenure-chip.selected { border-color: #f59e0b; background: #fffbeb; box-shadow: 0 0 0 3px rgba(245,158,11,.12); }
.chip-label { font-size: 12px; font-weight: 700; color: #1e293b; }
.chip-rate  { font-size: 11px; color: #d97706; font-weight: 600; }

.fd-preview { background: #fffbeb; border: 1.5px solid #fde68a; border-radius: 10px; padding: 14px 16px; display: flex; flex-direction: column; gap: 8px; }
.preview-row { display: flex; justify-content: space-between; font-size: 13px; color: #475569; }
.preview-row.highlight strong { font-size: 16px; color: #1e293b; }
.preview-row.earn strong { color: #16a34a; }

.alert-error   { padding: 10px 14px; border-radius: 8px; font-size: 13px; background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
.alert-success { padding: 10px 14px; border-radius: 8px; font-size: 13px; background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }

.btn-submit { width: 100%; padding: 13px; background: #f59e0b; color: #fff; border: none; border-radius: 10px; font-size: 15px; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; transition: background .18s; }
.btn-submit:hover:not(:disabled) { background: #d97706; }
.btn-submit:disabled { opacity: .6; cursor: not-allowed; }
.btn-spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,.3); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; }
.deduct-note { font-size: 12px; color: #94a3b8; text-align: center; margin-top: -8px; }

.rate-card { background: #fff; border-radius: 20px; padding: 24px; border: 1.5px solid #e2e8f0; box-shadow: 0 2px 12px rgba(15,32,68,.07); }
.rate-title { font-size: 15px; font-weight: 800; color: #1e293b; margin-bottom: 14px; }
.rate-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.rate-table th { text-align: left; padding: 8px 10px; font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: .5px; border-bottom: 1.5px solid #e2e8f0; }
.rate-table td { padding: 10px; border-bottom: 1px solid #f1f5f9; color: #475569; }
.rate-table tr:last-child td { border-bottom: none; }
.rate-table .row-selected td { background: #fffbeb; color: #92400e; font-weight: 700; }
.rate-val { font-weight: 700; color: #d97706; }
.rate-note { margin-top: 14px; font-size: 11px; color: #94a3b8; line-height: 1.5; }

@media (max-width: 700px) {
  .apply-layout { grid-template-columns: 1fr; }
  .fd-grid { grid-template-columns: 1fr; }
  .tenure-chips { grid-template-columns: repeat(2, 1fr); }
  .fd-dates { grid-template-columns: repeat(2, 1fr); }
}
</style>
