<template>
  <div class="page">

    <!-- Summary row -->
    <div class="summary-row">
      <div class="sum-card blue">
        <p class="sum-label">Total Transactions</p>
        <p class="sum-val">{{ filtered.length }}</p>
      </div>
      <div class="sum-card red">
        <p class="sum-label">Total Debited</p>
        <p class="sum-val">₹ {{ totalDebited }}</p>
      </div>
      <div class="sum-card green">
        <p class="sum-label">Total Credited</p>
        <p class="sum-val">₹ {{ totalCredited }}</p>
      </div>
    </div>

    <!-- Filters -->
    <div class="filter-bar">
      <div class="search-wrap">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input v-model="search" type="text" placeholder="Search by account, amount…" />
      </div>
      <div class="filter-group">
        <select v-model="typeFilter">
          <option value="">All Types</option>
          <option value="sent">Sent</option>
          <option value="received">Received</option>
        </select>
        <select v-model="statusFilter">
          <option value="">All Status</option>
          <option value="Completed">Completed</option>
          <option value="PENDING">Pending</option>
        </select>
      </div>
    </div>

    <!-- Table -->
    <div class="table-card">
      <div v-if="loading" class="state">
        <div class="spinner"></div><p>Loading transactions…</p>
      </div>
      <div v-else-if="filtered.length === 0" class="state">
        <svg viewBox="0 0 24 24" fill="none" stroke="#cbd5e1" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        <p>{{ transactions.length === 0 ? 'No transactions found' : 'No results match your filter' }}</p>
      </div>
      <table v-else class="txn-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Date</th>
            <th>Type</th>
            <th>From / To</th>
            <th>Amount</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(txn, i) in paginated" :key="txn.id">
            <td class="num">{{ (currentPage - 1) * perPage + i + 1 }}</td>
            <td>
              <p class="date-main">{{ formatDate(txn.date) }}</p>
              <p class="date-sub">{{ formatTime(txn.date) }}</p>
            </td>
            <td>
              <span class="type-badge" :class="txn._sent ? 'sent' : 'received'">
                <svg v-if="txn._sent" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></svg>
                {{ txn._sent ? 'Sent' : 'Received' }}
              </span>
            </td>
            <td>
              <p class="counterparty">{{ txn._sent ? txn.receiver : txn.sender }}</p>
            </td>
            <td>
              <span class="amount" :class="txn._sent ? 'debit' : 'credit'">
                {{ txn._sent ? '−' : '+' }} ₹{{ formatAmount(txn.amount) }}
              </span>
            </td>
            <td>
              <span class="status-badge" :class="txn.status === 'Completed' ? 'done' : 'pending'">
                {{ txn.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination">
        <button :disabled="currentPage === 1" @click="currentPage--" class="page-btn">← Prev</button>
        <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
        <button :disabled="currentPage === totalPages" @click="currentPage++" class="page-btn">Next →</button>
      </div>
    </div>

  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

export default {
  data() {
    return {
      transactions: [], loading: true,
      search: '', typeFilter: '', statusFilter: '',
      currentPage: 1, perPage: 10,
      accountNumber: '',
    };
  },
  computed: {
    enriched() {
      return this.transactions.map(t => ({
        ...t,
        _sent: t.sender && this.accountNumber && t.sender.includes(this.accountNumber),
      }));
    },
    filtered() {
      const q = this.search.toLowerCase();
      return this.enriched.filter(t => {
        const matchSearch = !q || t.sender?.toLowerCase().includes(q) || t.receiver?.toLowerCase().includes(q) || String(t.amount).includes(q);
        const matchType = !this.typeFilter || (this.typeFilter === 'sent' ? t._sent : !t._sent);
        const matchStatus = !this.statusFilter || t.status === this.statusFilter;
        return matchSearch && matchType && matchStatus;
      });
    },
    paginated() {
      const start = (this.currentPage - 1) * this.perPage;
      return this.filtered.slice(start, start + this.perPage);
    },
    totalPages() { return Math.ceil(this.filtered.length / this.perPage); },
    totalDebited() {
      return this.enriched.filter(t => t._sent).reduce((s, t) => s + parseFloat(t.amount || 0), 0).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },
    totalCredited() {
      return this.enriched.filter(t => !t._sent).reduce((s, t) => s + parseFloat(t.amount || 0), 0).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },
  },
  watch: {
    search() { this.currentPage = 1; },
    typeFilter() { this.currentPage = 1; },
    statusFilter() { this.currentPage = 1; },
  },
  async created() {
    try {
      const [txnRes, profileRes] = await Promise.all([
        apiClient.get('/transactions/statement/'),
        apiClient.get('/accounts/profile/').catch(() => null),
      ]);
      this.transactions = txnRes.data;
      if (profileRes) this.accountNumber = profileRes.data.account_number || '';
    } catch { this.transactions = []; }
    finally { this.loading = false; }
  },
  methods: {
    formatDate(d) { return new Date(d).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }); },
    formatTime(d) { return new Date(d).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }); },
    formatAmount(v) { return parseFloat(v || 0).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); },
  },
};
</script>

<style scoped>
.page { display: flex; flex-direction: column; gap: 20px; }

.summary-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.sum-card { background: #fff; border-radius: 14px; padding: 20px 24px; border: 1.5px solid #e2e8f0; box-shadow: 0 2px 8px rgba(15,32,68,.06); }
.sum-label { font-size: 12px; text-transform: uppercase; letter-spacing: .6px; color: #94a3b8; font-weight: 600; margin-bottom: 6px; }
.sum-val { font-size: 22px; font-weight: 800; }
.sum-card.blue .sum-val { color: #2563eb; }
.sum-card.red  .sum-val { color: #ef4444; }
.sum-card.green .sum-val { color: #16a34a; }

.filter-bar {
  display: flex; gap: 12px; align-items: center; flex-wrap: wrap;
  background: #fff; border-radius: 14px; padding: 16px 20px;
  border: 1.5px solid #e2e8f0; box-shadow: 0 2px 8px rgba(15,32,68,.04);
}
.search-wrap {
  flex: 1; display: flex; align-items: center; gap: 10px;
  border: 1.5px solid #e2e8f0; border-radius: 8px;
  padding: 8px 14px; background: #f8fafc; min-width: 200px;
}
.search-wrap svg { width: 16px; height: 16px; color: #94a3b8; flex-shrink: 0; }
.search-wrap input { border: none; background: transparent; outline: none; font-size: 14px; color: #1e293b; width: 100%; }

.filter-group { display: flex; gap: 10px; }
.filter-group select {
  padding: 9px 32px 9px 12px; border: 1.5px solid #e2e8f0; border-radius: 8px;
  font-size: 13px; color: #475569; background: #f8fafc;
  cursor: pointer; outline: none; appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' stroke='%2394a3b8' stroke-width='2' viewBox='0 0 24 24'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: right 8px center; background-size: 16px;
}

.table-card {
  background: #fff; border-radius: 16px;
  box-shadow: 0 2px 8px rgba(15,32,68,.06); border: 1.5px solid #e2e8f0; overflow: hidden;
}

.state {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 60px 24px; gap: 12px; color: #94a3b8; font-size: 14px;
}
.state svg { width: 48px; height: 48px; }

.spinner { width: 36px; height: 36px; border: 3px solid #e2e8f0; border-top-color: #2563eb; border-radius: 50%; animation: spin .7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.txn-table { width: 100%; border-collapse: collapse; }
.txn-table thead tr { background: #f8fafc; border-bottom: 1.5px solid #e2e8f0; }
.txn-table th { padding: 12px 16px; text-align: left; font-size: 11px; text-transform: uppercase; letter-spacing: .7px; color: #94a3b8; font-weight: 700; white-space: nowrap; }
.txn-table tbody tr { border-bottom: 1px solid #f1f5f9; transition: background .12s; }
.txn-table tbody tr:last-child { border-bottom: none; }
.txn-table tbody tr:hover { background: #f8fafc; }
.txn-table td { padding: 14px 16px; font-size: 13px; color: #1e293b; vertical-align: middle; }

.num { color: #94a3b8; font-weight: 600; }
.date-main { font-size: 13px; font-weight: 600; color: #1e293b; }
.date-sub { font-size: 11px; color: #94a3b8; margin-top: 2px; }

.type-badge {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600;
}
.type-badge svg { width: 12px; height: 12px; }
.type-badge.sent     { background: #fef2f2; color: #ef4444; }
.type-badge.received { background: #f0fdf4; color: #16a34a; }

.counterparty { font-size: 12px; color: #475569; font-family: 'Courier New', monospace; letter-spacing: .5px; max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.amount { font-size: 14px; font-weight: 700; white-space: nowrap; }
.amount.debit  { color: #ef4444; }
.amount.credit { color: #16a34a; }

.status-badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.status-badge.done    { background: #f0fdf4; color: #16a34a; }
.status-badge.pending { background: #fffbeb; color: #d97706; }

.pagination {
  display: flex; align-items: center; justify-content: center; gap: 16px;
  padding: 16px 20px; border-top: 1px solid #f1f5f9;
}
.page-btn {
  padding: 7px 16px; background: #f1f5f9; color: #475569;
  border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 13px; font-weight: 600;
  cursor: pointer; transition: all .15s;
}
.page-btn:hover:not(:disabled) { background: #e2e8f0; }
.page-btn:disabled { opacity: .4; cursor: not-allowed; }
.page-info { font-size: 13px; color: #64748b; }

@media (max-width: 640px) {
  .summary-row { grid-template-columns: 1fr; }
  .filter-bar { flex-direction: column; }
  .txn-table { display: block; overflow-x: auto; }
}
</style>
