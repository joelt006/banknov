<template>
  <div class="accounts-page">
    <!-- Page header -->
    <div class="page-header">
      <div>
        <h2>Account Management</h2>
        <p>View, freeze, and deposit funds into customer accounts</p>
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
          <template v-for="acc in filtered" :key="acc.id">
            <!-- Main row -->
            <tr :class="{ 'row-expanded': depositingId === acc.id }">
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
                <div class="balance-cell">
                  <span class="balance-amount">₹ {{ formatBalance(acc.balance) }}</span>
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
                  <!-- Freeze / Unfreeze -->
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
                  <!-- Deposit -->
                  <button
                    class="action-btn btn-deposit"
                    :class="{ active: depositingId === acc.id }"
                    @click="toggleDeposit(acc)"
                    :disabled="!isStandard(acc)"
                    :title="!isStandard(acc) ? 'Only standard accounts support deposits' : 'Deposit funds'"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></svg>
                    Deposit
                  </button>
                </div>
              </td>
            </tr>

            <!-- Inline deposit row -->
            <tr v-if="depositingId === acc.id" class="deposit-row">
              <td colspan="6">
                <div class="deposit-form">
                  <div class="deposit-form-inner">
                    <div class="deposit-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></svg>
                    </div>
                    <div class="deposit-info">
                      <div class="deposit-title">Deposit to {{ acc.account_holder_name }}</div>
                      <div class="deposit-acct">{{ acc.account_number }}</div>
                    </div>
                    <div class="deposit-input-wrap">
                      <span class="deposit-currency">₹</span>
                      <input
                        v-model="depositAmount"
                        type="number"
                        min="1"
                        step="0.01"
                        placeholder="Enter amount"
                        class="deposit-input"
                        @keyup.enter="submitDeposit(acc)"
                        @keyup.esc="cancelDeposit"
                        ref="depositInput"
                      />
                    </div>
                    <div class="deposit-actions">
                      <button class="btn-confirm-deposit" @click="submitDeposit(acc)" :disabled="depositing">
                        <span v-if="depositing" class="btn-spinner"></span>
                        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                        {{ depositing ? 'Processing…' : 'Confirm Deposit' }}
                      </button>
                      <button class="btn-cancel-deposit" @click="cancelDeposit">Cancel</button>
                    </div>
                  </div>
                  <div v-if="depositError" class="deposit-error">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                    {{ depositError }}
                  </div>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>

    <!-- Toast -->
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
      togglingId: null,
      depositingId: null,
      depositAmount: '',
      depositError: '',
      depositing: false,
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
        const matchType   = !this.filterType   || acc.account_type.toLowerCase() === this.filterType;
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

    toggleDeposit(acc) {
      if (this.depositingId === acc.id) {
        this.cancelDeposit();
      } else {
        this.depositingId = acc.id;
        this.depositAmount = '';
        this.depositError = '';
        this.$nextTick(() => {
          const el = this.$refs.depositInput;
          if (el) (Array.isArray(el) ? el[0] : el).focus();
        });
      }
    },

    cancelDeposit() {
      this.depositingId = null;
      this.depositAmount = '';
      this.depositError = '';
    },

    async submitDeposit(acc) {
      this.depositError = '';
      const amount = parseFloat(this.depositAmount);
      if (!amount || amount <= 0) {
        this.depositError = 'Please enter a valid amount greater than 0.';
        return;
      }
      this.depositing = true;
      try {
        const res = await adminApiClient.post('/transactions/deposit-money/', {
          account_number: acc.account_number,
          amount: amount,
        });
        acc.balance = parseFloat(res.data.new_balance);
        this.cancelDeposit();
        this.showToast('success', `₹ ${this.formatBalance(amount)} deposited to ${acc.account_holder_name}`);
      } catch (err) {
        this.depositError = err.response?.data?.error || 'Deposit failed. Please try again.';
      } finally {
        this.depositing = false;
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

.page-header { display: flex; align-items: flex-start; justify-content: space-between; flex-wrap: wrap; gap: 16px; }
.page-header h2 { font-size: 22px; font-weight: 800; color: #0f172a; margin-bottom: 4px; }
.page-header p  { font-size: 14px; color: #64748b; }

.header-stats { display: flex; gap: 12px; }
.hstat { display: flex; flex-direction: column; align-items: center; background: #f1f5f9; border-radius: 10px; padding: 12px 20px; min-width: 80px; }
.hstat-green { background: #f0fdf4; }
.hstat-red   { background: #fff1f2; }
.hstat-val { font-size: 22px; font-weight: 800; color: #0f172a; }
.hstat-green .hstat-val { color: #16a34a; }
.hstat-red   .hstat-val { color: #dc2626; }
.hstat-lbl { font-size: 11px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: .5px; }

.filters-bar { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px 18px; }
.search-wrap { display: flex; align-items: center; gap: 8px; flex: 1; min-width: 240px; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 8px 12px; background: #f8fafc; transition: border-color .15s; }
.search-wrap:focus-within { border-color: #6366f1; }
.search-wrap svg { width: 16px; height: 16px; color: #94a3b8; flex-shrink: 0; }
.search-wrap input { border: none; outline: none; background: transparent; font-size: 14px; color: #1e293b; width: 100%; }
.filter-group { display: flex; gap: 10px; }
.filter-group select { border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 8px 12px; font-size: 13px; color: #1e293b; background: #f8fafc; cursor: pointer; outline: none; }
.filter-group select:focus { border-color: #6366f1; }

.table-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 14px; overflow: hidden; box-shadow: 0 2px 12px rgba(15,32,68,.06); }
.loading-state, .empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; padding: 64px; color: #94a3b8; }
.loading-state .spinner { width: 32px; height: 32px; border: 3px solid #e2e8f0; border-top-color: #6366f1; border-radius: 50%; animation: spin .7s linear infinite; }
.empty-state svg { width: 48px; height: 48px; }
.empty-state p { font-size: 15px; font-weight: 500; }

.accounts-table { width: 100%; border-collapse: collapse; }
.accounts-table thead tr { background: #f8fafc; border-bottom: 2px solid #e2e8f0; }
.accounts-table th { padding: 13px 18px; text-align: left; font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: .6px; }
.accounts-table tbody tr { border-bottom: 1px solid #f1f5f9; transition: background .12s; }
.accounts-table tbody tr:last-child { border-bottom: none; }
.accounts-table tbody tr:hover { background: #fafbff; }
.accounts-table tbody tr.row-expanded { background: #f0fdf4; }
.accounts-table td { padding: 14px 18px; vertical-align: middle; }

.mono { font-family: 'Courier New', monospace; font-size: 13px; color: #475569; font-weight: 600; }

.holder-cell { display: flex; align-items: center; gap: 12px; }
.holder-avatar { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #4f46e5); display: flex; align-items: center; justify-content: center; color: #fff; font-size: 13px; font-weight: 700; flex-shrink: 0; }
.holder-name  { font-size: 14px; font-weight: 600; color: #1e293b; }
.holder-email { font-size: 12px; color: #94a3b8; margin-top: 1px; }

.type-badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; text-transform: capitalize; }
.type-standard { background: #eff6ff; color: #1d4ed8; }
.type-minor    { background: #fef9c3; color: #854d0e; }
.type-senior   { background: #f0fdf4; color: #15803d; }

.balance-cell  { display: flex; align-items: center; gap: 8px; }
.balance-amount { font-size: 14px; font-weight: 700; color: #1e293b; }

.status-badge { display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; }
.status-active { background: #f0fdf4; color: #16a34a; }
.status-frozen { background: #fff1f2; color: #dc2626; }
.status-dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }

.action-btns { display: flex; gap: 8px; flex-wrap: wrap; }
.action-btn { display: inline-flex; align-items: center; gap: 6px; padding: 7px 14px; border: none; border-radius: 8px; font-size: 12px; font-weight: 700; cursor: pointer; transition: all .15s; }
.action-btn svg { width: 14px; height: 14px; }
.action-btn:disabled { opacity: .5; cursor: not-allowed; }
.btn-freeze   { background: #fff1f2; color: #dc2626; }
.btn-freeze:hover:not(:disabled)   { background: #fecaca; }
.btn-unfreeze { background: #f0fdf4; color: #16a34a; }
.btn-unfreeze:hover:not(:disabled) { background: #bbf7d0; }
.btn-deposit  { background: #eff6ff; color: #2563eb; }
.btn-deposit:hover:not(:disabled)  { background: #dbeafe; }
.btn-deposit.active { background: #2563eb; color: #fff; }

/* Deposit inline row */
.deposit-row td { padding: 0; background: #f0fdf4; border-bottom: 2px solid #bbf7d0 !important; }
.deposit-form { padding: 20px 24px; }
.deposit-form-inner { display: flex; align-items: center; gap: 20px; flex-wrap: wrap; }
.deposit-icon { width: 42px; height: 42px; border-radius: 10px; background: #16a34a; display: flex; align-items: center; justify-content: center; color: #fff; flex-shrink: 0; }
.deposit-icon svg { width: 20px; height: 20px; }
.deposit-info { flex-shrink: 0; }
.deposit-title { font-size: 14px; font-weight: 700; color: #1e293b; }
.deposit-acct  { font-size: 12px; color: #64748b; font-family: 'Courier New', monospace; margin-top: 2px; }

.deposit-input-wrap { display: flex; align-items: center; border: 2px solid #16a34a; border-radius: 10px; background: #fff; overflow: hidden; flex: 1; min-width: 180px; max-width: 260px; }
.deposit-currency { padding: 0 14px; font-size: 20px; font-weight: 700; color: #16a34a; border-right: 2px solid #bbf7d0; }
.deposit-input { flex: 1; border: none; outline: none; padding: 10px 14px; font-size: 18px; font-weight: 700; color: #1e293b; background: transparent; min-width: 0; }
.deposit-input::placeholder { color: #cbd5e1; font-weight: 400; }

.deposit-actions { display: flex; gap: 8px; align-items: center; flex-shrink: 0; }
.btn-confirm-deposit { display: flex; align-items: center; gap: 6px; padding: 10px 18px; background: #16a34a; color: #fff; border: none; border-radius: 9px; font-size: 13px; font-weight: 700; cursor: pointer; transition: background .15s; }
.btn-confirm-deposit:hover:not(:disabled) { background: #15803d; }
.btn-confirm-deposit:disabled { opacity: .6; cursor: not-allowed; }
.btn-confirm-deposit svg { width: 14px; height: 14px; }
.btn-cancel-deposit { padding: 10px 16px; background: #f1f5f9; color: #475569; border: none; border-radius: 9px; font-size: 13px; font-weight: 600; cursor: pointer; }
.btn-cancel-deposit:hover { background: #e2e8f0; }

.deposit-error { display: flex; align-items: center; gap: 8px; margin-top: 12px; padding: 10px 14px; background: #fff1f2; border: 1px solid #fecaca; border-radius: 8px; color: #dc2626; font-size: 13px; }
.deposit-error svg { width: 15px; height: 15px; flex-shrink: 0; }

.btn-spinner { width: 14px; height: 14px; border: 2px solid rgba(255,255,255,.3); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; }

.toast { position: fixed; bottom: 28px; right: 28px; display: flex; align-items: center; gap: 10px; padding: 14px 20px; border-radius: 12px; font-size: 14px; font-weight: 600; z-index: 9999; box-shadow: 0 8px 32px rgba(0,0,0,.15); }
.toast svg { width: 18px; height: 18px; flex-shrink: 0; }
.toast-success { background: #16a34a; color: #fff; }
.toast-error   { background: #dc2626; color: #fff; }
.toast-enter-active, .toast-leave-active { transition: all .3s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(16px); }

@keyframes spin { to { transform: rotate(360deg); } }
</style>
