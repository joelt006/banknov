<template>
  <div class="admin-page">

    <!-- Access denied -->
    <div v-if="accessDenied" class="denied-card">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/></svg>
      <h3>Access Denied</h3>
      <p>This page is restricted to administrators only.</p>
    </div>

    <template v-else>
      <!-- Header -->
      <div class="admin-header">
        <div>
          <h2 class="page-heading">Admin Panel</h2>
          <p class="page-sub">Manage accounts, users, and transactions</p>
        </div>
        <button class="refresh-btn" @click="loadAll" :disabled="loading">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ spin: loading }"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>
          Refresh
        </button>
      </div>

      <!-- Stats -->
      <div class="stats-grid" v-if="stats">
        <div class="stat-card blue">
          <div class="stat-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></div>
          <div class="stat-body">
            <div class="stat-value">{{ stats.total_users }}</div>
            <div class="stat-label">Total Users</div>
          </div>
        </div>
        <div class="stat-card green">
          <div class="stat-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg></div>
          <div class="stat-body">
            <div class="stat-value">{{ totalAccounts }}</div>
            <div class="stat-label">Total Accounts</div>
          </div>
        </div>
        <div class="stat-card purple">
          <div class="stat-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg></div>
          <div class="stat-body">
            <div class="stat-value">{{ stats.total_transactions }}</div>
            <div class="stat-label">Transactions</div>
          </div>
        </div>
        <div class="stat-card gold">
          <div class="stat-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div>
          <div class="stat-body">
            <div class="stat-value">₹{{ formatAmount(stats.total_balance) }}</div>
            <div class="stat-label">Total Deposits</div>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="tab-bar">
        <button class="tab" :class="{ active: activeTab === 'accounts' }" @click="activeTab = 'accounts'">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
          Accounts
          <span class="tab-count">{{ accounts.length }}</span>
        </button>
        <button class="tab" :class="{ active: activeTab === 'transactions' }" @click="activeTab = 'transactions'">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/></svg>
          Transactions
          <span class="tab-count">{{ transactions.length }}</span>
        </button>
      </div>

      <!-- Accounts Table -->
      <div v-if="activeTab === 'accounts'" class="table-card">
        <div class="table-toolbar">
          <input v-model="accountSearch" class="search-input" placeholder="Search by name, account no., email…" />
          <div class="type-filters">
            <button v-for="t in accountTypes" :key="t" class="filter-chip" :class="{ active: typeFilter === t }" @click="typeFilter = typeFilter === t ? '' : t">{{ t }}</button>
          </div>
        </div>
        <div class="table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th>Account Holder</th>
                <th>Account Number</th>
                <th>Balance</th>
                <th>Type</th>
                <th>Contact</th>
                <th>Location</th>
                <th>Joined</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredAccounts.length === 0">
                <td colspan="7" class="empty-row">No accounts found</td>
              </tr>
              <tr v-for="a in filteredAccounts" :key="a.id">
                <td>
                  <div class="name-cell">
                    <div class="avatar">{{ (a.account_holder_name || '?')[0].toUpperCase() }}</div>
                    <div>
                      <div class="name">{{ a.account_holder_name }}</div>
                      <div class="sub">{{ a.username || '—' }}</div>
                    </div>
                  </div>
                </td>
                <td><span class="mono">{{ a.account_number }}</span></td>
                <td><span class="amount">₹{{ formatAmount(a.balance) }}</span></td>
                <td><span class="type-badge" :class="a.account_type.toLowerCase()">{{ a.account_type }}</span></td>
                <td>
                  <div class="sub">{{ a.email || '—' }}</div>
                  <div class="sub">{{ a.phone_number || '—' }}</div>
                </td>
                <td>{{ a.city || '—' }}, {{ a.country || '—' }}</td>
                <td class="sub">{{ a.created_at ? formatDate(a.created_at) : '—' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Transactions Table -->
      <div v-if="activeTab === 'transactions'" class="table-card">
        <div class="table-toolbar">
          <input v-model="txnSearch" class="search-input" placeholder="Search by sender, receiver, status…" />
        </div>
        <div class="table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Sender</th>
                <th>Receiver</th>
                <th>Amount</th>
                <th>Type</th>
                <th>Status</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredTxns.length === 0">
                <td colspan="7" class="empty-row">No transactions found</td>
              </tr>
              <tr v-for="t in filteredTxns" :key="t.id">
                <td class="mono sub">#{{ t.id }}</td>
                <td><span class="sub">{{ t.sender || '—' }}</span></td>
                <td><span class="sub">{{ t.receiver || '—' }}</span></td>
                <td><span class="amount">₹{{ formatAmount(t.amount) }}</span></td>
                <td><span class="type-badge standard">{{ t.transaction_type }}</span></td>
                <td>
                  <span class="status-badge" :class="t.status === 'Completed' ? 'success' : t.status === 'PENDING' ? 'warning' : 'danger'">
                    {{ t.status }}
                  </span>
                </td>
                <td class="sub">{{ formatDate(t.date) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

export default {
  name: 'BankAdmin',
  data() {
    return {
      loading: false,
      accessDenied: false,
      stats: null,
      accounts: [],
      transactions: [],
      activeTab: 'accounts',
      accountSearch: '',
      txnSearch: '',
      typeFilter: '',
      accountTypes: ['Standard', 'Minor', 'Senior'],
    };
  },
  computed: {
    totalAccounts() {
      if (!this.stats) return 0;
      return (
        (this.stats.total_accounts || 0) +
        (this.stats.total_minor_accounts || 0) +
        (this.stats.total_senior_accounts || 0)
      );
    },
    filteredAccounts() {
      let list = this.accounts;
      if (this.typeFilter) list = list.filter(a => a.account_type === this.typeFilter);
      if (this.accountSearch.trim()) {
        const q = this.accountSearch.toLowerCase();
        list = list.filter(a =>
          (a.account_holder_name || '').toLowerCase().includes(q) ||
          (a.account_number || '').toLowerCase().includes(q) ||
          (a.email || '').toLowerCase().includes(q) ||
          (a.username || '').toLowerCase().includes(q)
        );
      }
      return list;
    },
    filteredTxns() {
      if (!this.txnSearch.trim()) return this.transactions;
      const q = this.txnSearch.toLowerCase();
      return this.transactions.filter(t =>
        (t.sender || '').toLowerCase().includes(q) ||
        (t.receiver || '').toLowerCase().includes(q) ||
        (t.status || '').toLowerCase().includes(q)
      );
    },
  },
  async created() {
    await this.loadAll();
  },
  methods: {
    async loadAll() {
      this.loading = true;
      try {
        const [statsRes, accountsRes, txnsRes] = await Promise.all([
          apiClient.get('/accounts/admin/stats/'),
          apiClient.get('/accounts/admin/accounts/'),
          apiClient.get('/accounts/admin/transactions/'),
        ]);
        this.stats = statsRes.data;
        this.accounts = accountsRes.data;
        this.transactions = txnsRes.data;
      } catch (err) {
        if (err.response?.status === 403) this.accessDenied = true;
      } finally {
        this.loading = false;
      }
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
.admin-page { display: flex; flex-direction: column; gap: 24px; }

/* Denied */
.denied-card {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 14px; padding: 80px 24px; background: #fff; border-radius: 20px;
  border: 1.5px solid #fecaca; color: #b91c1c; text-align: center;
}
.denied-card svg { width: 56px; height: 56px; }
.denied-card h3 { font-size: 20px; font-weight: 800; }
.denied-card p { font-size: 14px; color: #64748b; }

/* Header */
.admin-header { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; }
.page-heading { font-size: 22px; font-weight: 800; color: #1e293b; }
.page-sub { font-size: 14px; color: #64748b; margin-top: 4px; }

.refresh-btn {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 20px; border-radius: 10px; border: 1.5px solid #e2e8f0;
  background: #fff; color: #475569; font-size: 13px; font-weight: 600; cursor: pointer;
  transition: all .18s;
}
.refresh-btn:hover { background: #eff6ff; border-color: #bfdbfe; color: #2563eb; }
.refresh-btn svg { width: 16px; height: 16px; transition: transform .3s; }
.refresh-btn svg.spin { animation: spin .7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Stats */
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.stat-card {
  display: flex; align-items: center; gap: 16px;
  background: #fff; border-radius: 16px; padding: 20px 22px;
  border: 1.5px solid #e2e8f0; box-shadow: 0 2px 8px rgba(15,32,68,.06);
}
.stat-icon { width: 48px; height: 48px; border-radius: 14px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.stat-icon svg { width: 22px; height: 22px; }
.stat-card.blue  .stat-icon { background: #eff6ff; color: #2563eb; }
.stat-card.green .stat-icon { background: #f0fdf4; color: #16a34a; }
.stat-card.purple.stat-icon { background: #faf5ff; color: #7c3aed; }
.stat-card.purple .stat-icon { background: #faf5ff; color: #7c3aed; }
.stat-card.gold  .stat-icon { background: #fffbeb; color: #d97706; }
.stat-value { font-size: 22px; font-weight: 800; color: #1e293b; }
.stat-label { font-size: 12px; color: #64748b; margin-top: 2px; font-weight: 500; }

/* Tabs */
.tab-bar { display: flex; gap: 4px; background: #f1f5f9; border-radius: 12px; padding: 4px; width: fit-content; }
.tab {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 20px; border-radius: 9px; border: none;
  background: transparent; color: #64748b; font-size: 13px; font-weight: 600;
  cursor: pointer; transition: all .18s;
}
.tab svg { width: 15px; height: 15px; }
.tab:hover { color: #1e293b; }
.tab.active { background: #fff; color: #2563eb; box-shadow: 0 2px 8px rgba(15,32,68,.08); }
.tab-count {
  background: #e2e8f0; color: #64748b; border-radius: 10px;
  padding: 1px 8px; font-size: 11px; font-weight: 700;
}
.tab.active .tab-count { background: #eff6ff; color: #2563eb; }

/* Table card */
.table-card { background: #fff; border-radius: 16px; border: 1.5px solid #e2e8f0; box-shadow: 0 2px 8px rgba(15,32,68,.06); overflow: hidden; }

.table-toolbar {
  display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
  padding: 16px 20px; border-bottom: 1px solid #f1f5f9;
}
.search-input {
  flex: 1; min-width: 200px; padding: 9px 14px;
  border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 13px; color: #1e293b;
  background: #f8fafc; outline: none;
}
.search-input:focus { border-color: #2563eb; background: #fff; }

.type-filters { display: flex; gap: 6px; }
.filter-chip {
  padding: 6px 14px; border-radius: 20px; border: 1.5px solid #e2e8f0;
  background: #f8fafc; color: #64748b; font-size: 12px; font-weight: 600; cursor: pointer;
  transition: all .18s;
}
.filter-chip:hover { border-color: #2563eb; color: #2563eb; }
.filter-chip.active { background: #eff6ff; border-color: #2563eb; color: #2563eb; }

.table-wrap { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th {
  padding: 12px 16px; text-align: left; font-size: 11px; font-weight: 700;
  color: #64748b; text-transform: uppercase; letter-spacing: .6px;
  background: #f8fafc; border-bottom: 1px solid #e2e8f0;
  white-space: nowrap;
}
.data-table td {
  padding: 13px 16px; font-size: 13px; color: #1e293b;
  border-bottom: 1px solid #f1f5f9; vertical-align: middle;
}
.data-table tr:last-child td { border-bottom: none; }
.data-table tr:hover td { background: #f8fafc; }
.empty-row { text-align: center; color: #94a3b8; font-size: 14px; padding: 40px !important; }

/* Cells */
.name-cell { display: flex; align-items: center; gap: 10px; }
.avatar {
  width: 34px; height: 34px; border-radius: 50%; background: #eff6ff; color: #2563eb;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700; flex-shrink: 0;
}
.name { font-size: 13px; font-weight: 600; color: #1e293b; }
.sub { font-size: 12px; color: #64748b; }
.mono { font-family: 'Courier New', monospace; letter-spacing: .5px; }
.amount { font-size: 13px; font-weight: 700; color: #1e293b; }

.type-badge {
  padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 700;
  text-transform: uppercase; letter-spacing: .5px;
}
.type-badge.standard { background: #eff6ff; color: #2563eb; }
.type-badge.minor    { background: #faf5ff; color: #7c3aed; }
.type-badge.senior   { background: #fffbeb; color: #d97706; }
.type-badge.transfer { background: #f0fdf4; color: #16a34a; }

.status-badge {
  padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 700;
}
.status-badge.success { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
.status-badge.warning { background: #fffbeb; color: #d97706; border: 1px solid #fde68a; }
.status-badge.danger  { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }

@media (max-width: 900px) { .stats-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 600px) { .stats-grid { grid-template-columns: 1fr 1fr; } .tab-bar { width: 100%; } }
</style>
