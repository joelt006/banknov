<template>
  <div class="accounts-page">
    <!-- Page header -->
    <div class="page-header">
      <div>
        <h2>Account Management</h2>
        <p>View and manage all customer bank accounts</p>
      </div>
      <div class="header-stats">
        <div class="hstat">
          <span class="hstat-val">{{ accounts.length }}</span>
          <span class="hstat-lbl">Total</span>
        </div>
        <div class="hstat hstat-green">
          <span class="hstat-val">{{ activeCount }}</span>
          <span class="hstat-lbl">Active</span>
        </div>
        <div class="hstat hstat-red">
          <span class="hstat-val">{{ frozenCount }}</span>
          <span class="hstat-lbl">Frozen</span>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-wrap">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input v-model="search" type="text" placeholder="Search by name or account number…" />
      </div>
      <div class="filter-group">
        <select v-model="filterType">
          <option value="">All Types</option>
          <option value="standard">Standard</option>
          <option value="minor">Minor</option>
          <option value="senior">Senior</option>
        </select>
        <select v-model="filterStatus">
          <option value="">All Status</option>
          <option value="active">Active</option>
          <option value="frozen">Frozen</option>
        </select>
      </div>
    </div>

    <!-- Table -->
    <div class="table-card">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading accounts…</p>
      </div>

      <div v-else-if="filtered.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
        <p>No accounts match your filters</p>
      </div>

      <table v-else class="accounts-table">
        <thead>
          <tr>
            <th>Account #</th>
            <th>Account Holder</th>
            <th>Type</th>
            <th>Balance</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="acc in filtered" :key="acc.id">
            <td class="mono">{{ acc.account_number }}</td>
            <td>
              <div class="holder-cell">
                <div class="holder-avatar">{{ (acc.account_holder_name || '?')[0].toUpperCase() }}</div>
                <div>
                  <div class="holder-name">{{ acc.account_holder_name }}</div>
                  <div class="holder-email">{{ acc.email || '—' }}</div>
                </div>
              </div>
            </td>
            <td>
              <span class="type-badge" :class="'type-' + acc.account_type.toLowerCase()">
                {{ acc.account_type }}
              </span>
            </td>
            <td>
              <div v-if="editingId === acc.id" class="balance-edit">
                <input
                  v-model="editBalance"
                  type="number"
                  step="0.01"
                  min="0"
                  class="balance-input"
                  @keyup.enter="saveBalance(acc)"
                  @keyup.esc="cancelEdit"
                />
                <button class="btn-save" @click="saveBalance(acc)" :disabled="saving">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                </button>
                <button class="btn-cancel" @click="cancelEdit">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                </button>
              </div>
              <div v-else class="balance-cell">
                <span>₹ {{ formatBalance(acc.balance) }}</span>
                <button v-if="isStandard(acc)" class="btn-edit-bal" @click="startEdit(acc)" title="Edit balance">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                </button>
              </div>
            </td>
            <td>
              <span class="status-badge" :class="acc.is_frozen ? 'status-frozen' : 'status-active'">
                <span class="status-dot"></span>
                {{ acc.is_frozen ? 'Frozen' : 'Active' }}
              </span>
            </td>
            <td>
              <div class="action-btns">
                <button
                  class="action-btn"
                  :class="acc.is_frozen ? 'btn-unfreeze' : 'btn-freeze'"
                  @click="toggleFreeze(acc)"
                  :disabled="togglingId === acc.id || !isStandard(acc)"
                  :title="!isStandard(acc) ? 'Only standard accounts can be frozen' : ''"
                >
                  <svg v-if="!acc.is_frozen" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M2 12h20M4.93 4.93l14.14 14.14M19.07 4.93L4.93 19.07"/></svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="10 8 16 12 10 16"/></svg>
                  {{ acc.is_frozen ? 'Unfreeze' : 'Freeze' }}
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Toast notification -->
    <transition name="toast">
      <div v-if="toast.show" class="toast" :class="'toast-' + toast.type">
        <svg v-if="toast.type === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        {{ toast.message }}
      </div>
    </transition>
  </div>
</template>

<script>
import adminApiClient from '@/services/adminApiClient';

export default {
  name: 'AdminAccounts',
  data() {
    return {
      accounts: [],
      loading: true,
      search: '',
      filterType: '',
      filterStatus: '',
      editingId: null,
      editBalance: '',
      saving: false,
      togglingId: null,
      toast: { show: false, type: 'success', message: '' },
    };
  },
  computed: {
    filtered() {
      return this.accounts.filter(acc => {
        const q = this.search.toLowerCase();
        const matchSearch = !q ||
          (acc.account_holder_name || '').toLowerCase().includes(q) ||
          (acc.account_number || '').toLowerCase().includes(q) ||
          (acc.email || '').toLowerCase().includes(q);
        const matchType = !this.filterType || acc.account_type.toLowerCase() === this.filterType;
        const matchStatus = !this.filterStatus ||
          (this.filterStatus === 'frozen' ? acc.is_frozen : !acc.is_frozen);
        return matchSearch && matchType && matchStatus;
      });
    },
    activeCount() { return this.accounts.filter(a => !a.is_frozen).length; },
    frozenCount()  { return this.accounts.filter(a =>  a.is_frozen).length; },
  },
  mounted() { this.fetchAccounts(); },
  methods: {
    async fetchAccounts() {
      this.loading = true;
      try {
        const res = await adminApiClient.get('/accounts/admin/accounts/');
        this.accounts = res.data;
      } catch {
        this.showToast('error', 'Failed to load accounts');
      } finally {
        this.loading = false;
      }
    },

    async toggleFreeze(acc) {
      this.togglingId = acc.id;
      try {
        const res = await adminApiClient.patch(`/accounts/admin/accounts/${acc.id}/`, {
          is_frozen: !acc.is_frozen,
        });
        acc.is_frozen = res.data.is_frozen;
        this.showToast('success', `Account ${acc.is_frozen ? 'frozen' : 'unfrozen'} successfully`);
      } catch {
        this.showToast('error', 'Failed to update account status');
      } finally {
        this.togglingId = null;
      }
    },

    startEdit(acc) {
      this.editingId = acc.id;
      this.editBalance = acc.balance;
    },

    cancelEdit() {
      this.editingId = null;
      this.editBalance = '';
    },

    async saveBalance(acc) {
      if (this.editBalance === '' || isNaN(Number(this.editBalance))) return;
      this.saving = true;
      try {
        const res = await adminApiClient.patch(`/accounts/admin/accounts/${acc.id}/`, {
          balance: Number(this.editBalance),
        });
        acc.balance = res.data.balance;
        this.cancelEdit();
        this.showToast('success', 'Balance updated successfully');
      } catch {
        this.showToast('error', 'Failed to update balance');
      } finally {
        this.saving = false;
      }
    },

    isStandard(acc) { return typeof acc.id === 'number'; },

    formatBalance(val) {
      return Number(val).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },

    showToast(type, message) {
      this.toast = { show: true, type, message };
      setTimeout(() => { this.toast.show = false; }, 3500);
    },
  },
};
</script>

<style scoped>
.accounts-page { display: flex; flex-direction: column; gap: 24px; }

/* Header */
.page-header {
  display: flex; align-items: flex-start; justify-content: space-between; flex-wrap: wrap; gap: 16px;
}
.page-header h2 { font-size: 22px; font-weight: 800; color: #0f172a; margin-bottom: 4px; }
.page-header p { font-size: 14px; color: #64748b; }

.header-stats { display: flex; gap: 12px; }
.hstat {
  display: flex; flex-direction: column; align-items: center;
  background: #f1f5f9; border-radius: 10px; padding: 12px 20px;
  min-width: 80px;
}
.hstat-green { background: #f0fdf4; }
.hstat-red   { background: #fff1f2; }
.hstat-val { font-size: 22px; font-weight: 800; color: #0f172a; }
.hstat-green .hstat-val { color: #16a34a; }
.hstat-red   .hstat-val { color: #dc2626; }
.hstat-lbl { font-size: 11px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: .5px; }

/* Filters */
.filters-bar {
  display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
  background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px 18px;
}

.search-wrap {
  display: flex; align-items: center; gap: 8px; flex: 1; min-width: 240px;
  border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 8px 12px;
  background: #f8fafc; transition: border-color .15s;
}
.search-wrap:focus-within { border-color: #6366f1; }
.search-wrap svg { width: 16px; height: 16px; color: #94a3b8; flex-shrink: 0; }
.search-wrap input { border: none; outline: none; background: transparent; font-size: 14px; color: #1e293b; width: 100%; }

.filter-group { display: flex; gap: 10px; }
.filter-group select {
  border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 8px 12px;
  font-size: 13px; color: #1e293b; background: #f8fafc;
  cursor: pointer; outline: none; transition: border-color .15s;
}
.filter-group select:focus { border-color: #6366f1; }

/* Table card */
.table-card {
  background: #fff; border: 1px solid #e2e8f0; border-radius: 14px;
  overflow: hidden; box-shadow: 0 2px 12px rgba(15,32,68,.06);
}

.loading-state, .empty-state {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 12px; padding: 64px; color: #94a3b8;
}
.loading-state .spinner {
  width: 32px; height: 32px; border: 3px solid #e2e8f0;
  border-top-color: #6366f1; border-radius: 50%;
  animation: spin .7s linear infinite;
}
.empty-state svg { width: 48px; height: 48px; }
.empty-state p { font-size: 15px; font-weight: 500; }

/* Table */
.accounts-table { width: 100%; border-collapse: collapse; }
.accounts-table thead tr { background: #f8fafc; border-bottom: 2px solid #e2e8f0; }
.accounts-table th {
  padding: 13px 18px; text-align: left;
  font-size: 11px; font-weight: 700; color: #64748b;
  text-transform: uppercase; letter-spacing: .6px;
}
.accounts-table tbody tr {
  border-bottom: 1px solid #f1f5f9;
  transition: background .12s;
}
.accounts-table tbody tr:last-child { border-bottom: none; }
.accounts-table tbody tr:hover { background: #fafbff; }
.accounts-table td { padding: 14px 18px; vertical-align: middle; }

.mono { font-family: 'Courier New', monospace; font-size: 13px; color: #475569; font-weight: 600; }

/* Holder cell */
.holder-cell { display: flex; align-items: center; gap: 12px; }
.holder-avatar {
  width: 36px; height: 36px; border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 13px; font-weight: 700; flex-shrink: 0;
}
.holder-name { font-size: 14px; font-weight: 600; color: #1e293b; }
.holder-email { font-size: 12px; color: #94a3b8; margin-top: 1px; }

/* Type badge */
.type-badge {
  display: inline-block; padding: 3px 10px; border-radius: 20px;
  font-size: 11px; font-weight: 700; text-transform: capitalize; letter-spacing: .3px;
}
.type-standard { background: #eff6ff; color: #1d4ed8; }
.type-minor    { background: #fef9c3; color: #854d0e; }
.type-senior   { background: #f0fdf4; color: #15803d; }

/* Status badge */
.status-badge {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 4px 10px; border-radius: 20px;
  font-size: 12px; font-weight: 600;
}
.status-active { background: #f0fdf4; color: #16a34a; }
.status-frozen { background: #fff1f2; color: #dc2626; }
.status-dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }

/* Balance cell */
.balance-cell { display: flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 600; color: #1e293b; }
.btn-edit-bal {
  background: none; border: none; cursor: pointer; padding: 4px;
  color: #94a3b8; opacity: 0; transition: opacity .15s, color .15s;
}
tr:hover .btn-edit-bal { opacity: 1; }
.btn-edit-bal:hover { color: #6366f1; }
.btn-edit-bal svg { width: 14px; height: 14px; display: block; }

/* Balance edit */
.balance-edit { display: flex; align-items: center; gap: 6px; }
.balance-input {
  width: 110px; padding: 6px 10px; border: 2px solid #6366f1;
  border-radius: 7px; font-size: 14px; color: #1e293b; outline: none;
}
.btn-save, .btn-cancel {
  width: 28px; height: 28px; border: none; border-radius: 6px;
  display: flex; align-items: center; justify-content: center; cursor: pointer;
}
.btn-save { background: #6366f1; color: #fff; }
.btn-save:disabled { opacity: .5; cursor: not-allowed; }
.btn-save svg, .btn-cancel svg { width: 14px; height: 14px; }
.btn-cancel { background: #f1f5f9; color: #64748b; }
.btn-cancel:hover { background: #e2e8f0; }

/* Action buttons */
.action-btns { display: flex; gap: 8px; }
.action-btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 7px 14px; border: none; border-radius: 8px;
  font-size: 12px; font-weight: 700; cursor: pointer; transition: all .15s;
}
.action-btn svg { width: 14px; height: 14px; }
.action-btn:disabled { opacity: .5; cursor: not-allowed; }

.btn-freeze { background: #fff1f2; color: #dc2626; }
.btn-freeze:hover:not(:disabled) { background: #fecaca; }
.btn-unfreeze { background: #f0fdf4; color: #16a34a; }
.btn-unfreeze:hover:not(:disabled) { background: #bbf7d0; }

/* Toast */
.toast {
  position: fixed; bottom: 28px; right: 28px;
  display: flex; align-items: center; gap: 10px;
  padding: 14px 20px; border-radius: 12px;
  font-size: 14px; font-weight: 600; z-index: 9999;
  box-shadow: 0 8px 32px rgba(0,0,0,.15);
}
.toast svg { width: 18px; height: 18px; flex-shrink: 0; }
.toast-success { background: #16a34a; color: #fff; }
.toast-error   { background: #dc2626; color: #fff; }

.toast-enter-active, .toast-leave-active { transition: all .3s ease; }
.toast-enter-from { opacity: 0; transform: translateY(16px); }
.toast-leave-to   { opacity: 0; transform: translateY(16px); }

@keyframes spin { to { transform: rotate(360deg); } }
</style>
