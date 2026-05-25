<template>
  <div class="page">
    <div class="card">
      <div class="card-header">
        <div class="card-icon amber">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        </div>
        <div>
          <h2 class="card-title">Scheduled Transfers</h2>
          <p class="card-sub">All your upcoming and past scheduled transfers</p>
        </div>
      </div>

      <div v-if="loading" class="loading-row">
        <span class="spinner"></span> Loading…
      </div>
      <div v-else-if="transfers.length === 0" class="empty">
        No scheduled transfers yet.
        <RouterLink to="/SendMoney" class="link">Schedule one now →</RouterLink>
      </div>
      <div v-else class="transfer-list">
        <div v-for="t in transfers" :key="t.id" class="transfer-row" :class="t.status">
          <div class="transfer-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          </div>
          <div class="transfer-info">
            <div class="transfer-acct">To: {{ formatAcct(t.recipient_account_number) }}</div>
            <div class="transfer-meta">
              Scheduled: {{ formatDate(t.scheduled_at) }}
            </div>
            <div v-if="t.failure_reason" class="transfer-fail">{{ t.failure_reason }}</div>
          </div>
          <div class="transfer-right">
            <div class="transfer-amount">₹ {{ formatAmount(t.amount) }}</div>
            <span class="badge" :class="`badge-${t.status}`">{{ capitalize(t.status) }}</span>
            <button v-if="t.status === 'pending'" class="btn-cancel" @click="cancel(t.id)">Cancel</button>
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
    return { transfers: [], loading: true };
  },
  mounted() {
    this.fetch();
  },
  methods: {
    async fetch() {
      this.loading = true;
      try {
        const res = await apiClient.get('/transactions/scheduled/');
        this.transfers = res.data;
      } catch { /* silent */ } finally {
        this.loading = false;
      }
    },
    async cancel(id) {
      if (!confirm('Cancel this scheduled transfer?')) return;
      try {
        await apiClient.delete(`/transactions/scheduled/${id}/`);
        const t = this.transfers.find(x => x.id === id);
        if (t) t.status = 'cancelled';
      } catch (err) {
        alert(err.response?.data?.error || 'Failed to cancel.');
      }
    },
    formatAcct(n) { return n.replace(/(.{4})/g, '$1 ').trim(); },
    formatAmount(v) { return parseFloat(v || 0).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); },
    formatDate(iso) { return new Date(iso).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' }); },
    capitalize(s) { return s.charAt(0).toUpperCase() + s.slice(1); },
  },
};
</script>

<style scoped>
.page { max-width: 720px; margin: 0 auto; }

.card { background: #fff; border-radius: 20px; padding: 28px; box-shadow: 0 2px 16px rgba(15,32,68,.08); border: 1.5px solid #e2e8f0; }
.card-header { display: flex; align-items: center; gap: 14px; margin-bottom: 24px; }
.card-icon { width: 48px; height: 48px; border-radius: 13px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.card-icon svg { width: 22px; height: 22px; }
.card-icon.amber { background: #fffbeb; color: #d97706; }
.card-title { font-size: 17px; font-weight: 800; color: #1e293b; margin-bottom: 2px; }
.card-sub { font-size: 13px; color: #64748b; }

.loading-row { display: flex; align-items: center; gap: 10px; color: #64748b; font-size: 14px; padding: 24px 0; }
.empty { color: #94a3b8; font-size: 14px; text-align: center; padding: 40px 0; display: flex; flex-direction: column; align-items: center; gap: 10px; }
.link { color: #2563eb; font-weight: 600; font-size: 14px; }

.transfer-list { display: flex; flex-direction: column; gap: 10px; }
.transfer-row {
  display: flex; align-items: center; gap: 14px;
  padding: 16px; border-radius: 12px; background: #f8fafc; border: 1.5px solid #e2e8f0;
}
.transfer-row.processed { border-color: #bbf7d0; background: #f0fdf4; }
.transfer-row.failed { border-color: #fecaca; background: #fef2f2; }
.transfer-row.cancelled { opacity: .6; }

.transfer-icon { width: 40px; height: 40px; border-radius: 10px; background: #fff; border: 1.5px solid #e2e8f0; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.transfer-icon svg { width: 18px; height: 18px; stroke: #d97706; }

.transfer-info { flex: 1; min-width: 0; }
.transfer-acct { font-size: 14px; font-weight: 700; color: #1e293b; font-family: monospace; letter-spacing: .5px; }
.transfer-meta { font-size: 12px; color: #64748b; margin-top: 2px; }
.transfer-fail { font-size: 12px; color: #dc2626; margin-top: 4px; }

.transfer-right { display: flex; flex-direction: column; align-items: flex-end; gap: 6px; flex-shrink: 0; }
.transfer-amount { font-size: 16px; font-weight: 800; color: #1e293b; }

.badge { padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; }
.badge-pending { background: #fef3c7; color: #d97706; }
.badge-processed { background: #dcfce7; color: #16a34a; }
.badge-failed { background: #fef2f2; color: #dc2626; }
.badge-cancelled { background: #f1f5f9; color: #64748b; }

.btn-cancel {
  padding: 5px 12px; background: #fef2f2; color: #dc2626;
  border: 1.5px solid #fecaca; border-radius: 7px; font-size: 12px; font-weight: 600;
  cursor: pointer; transition: background .15s;
}
.btn-cancel:hover { background: #fee2e2; }

.spinner { width: 16px; height: 16px; border: 2px solid #e2e8f0; border-top-color: #64748b; border-radius: 50%; animation: spin .6s linear infinite; display: inline-block; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
