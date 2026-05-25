<template>
  <div class="admin-loans">
    <!-- Filter bar -->
    <div class="filter-bar">
      <div class="filter-group">
        <label>Status</label>
        <select v-model="filterStatus" @change="fetchLoans">
          <option value="">All</option>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
          <option value="active">Active</option>
          <option value="closed">Closed</option>
        </select>
      </div>
      <div class="filter-group">
        <label>Type</label>
        <select v-model="filterType" @change="applyFilter">
          <option value="">All Types</option>
          <option value="personal">Personal</option>
          <option value="home">Home</option>
          <option value="car">Car</option>
          <option value="education">Education</option>
        </select>
      </div>
      <div class="stats-chips">
        <div class="stat-chip pending">{{ counts.pending }} Pending</div>
        <div class="stat-chip approved">{{ counts.approved }} Approved</div>
        <div class="stat-chip rejected">{{ counts.rejected }} Rejected</div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading loan applications…</p>
    </div>

    <!-- Empty -->
    <div v-else-if="filtered.length === 0" class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M8 12h8M12 8v8"/></svg>
      <p>No loan applications found</p>
    </div>

    <!-- Loan cards -->
    <div v-else class="loans-grid">
      <div v-for="loan in filtered" :key="loan.id" class="loan-card" :class="loan.status">
        <div class="loan-header">
          <div class="loan-meta">
            <span class="loan-type-badge" :class="loan.loan_type">{{ loanTypeLabel(loan.loan_type) }}</span>
            <span class="status-badge" :class="loan.status">{{ statusLabel(loan.status) }}</span>
          </div>
          <div class="loan-amount">₹{{ formatAmount(loan.amount) }}</div>
        </div>

        <div class="loan-body">
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">Account Holder</span>
              <span class="info-value">{{ loan.account_holder_name || '—' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Account No.</span>
              <span class="info-value mono">{{ loan.account_number || '—' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Tenure</span>
              <span class="info-value">{{ loan.tenure_months }} months</span>
            </div>
            <div class="info-item">
              <span class="info-label">Interest Rate</span>
              <span class="info-value">{{ loan.interest_rate }}% p.a.</span>
            </div>
            <div class="info-item">
              <span class="info-label">Monthly EMI</span>
              <span class="info-value">₹{{ formatAmount(loan.monthly_emi || 0) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Applied On</span>
              <span class="info-value">{{ formatDate(loan.applied_at) }}</span>
            </div>
          </div>

          <div v-if="loan.purpose" class="purpose-block">
            <span class="info-label">Purpose</span>
            <p class="purpose-text">{{ loan.purpose }}</p>
          </div>

          <div v-if="loan.admin_note" class="note-block">
            <span class="info-label">Admin Note</span>
            <p class="note-text">{{ loan.admin_note }}</p>
          </div>

          <div v-if="loan.reviewed_at" class="review-meta">
            Reviewed on {{ formatDate(loan.reviewed_at) }}
          </div>
        </div>

        <!-- Action panel for pending loans -->
        <div v-if="loan.status === 'pending'" class="action-panel">
          <div class="action-fields">
            <div class="field-group">
              <label>Approved Amount (₹)</label>
              <input
                type="number"
                v-model.number="actions[loan.id].approvedAmount"
                :placeholder="loan.amount"
                min="1000"
              />
            </div>
            <div class="field-group">
              <label>Admin Note (optional)</label>
              <input
                type="text"
                v-model="actions[loan.id].note"
                placeholder="Reason or remarks…"
              />
            </div>
          </div>
          <div class="action-btns">
            <button
              class="btn-approve"
              :disabled="reviewing === loan.id"
              @click="reviewLoan(loan.id, 'approved')"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
              {{ reviewing === loan.id ? 'Processing…' : 'Approve' }}
            </button>
            <button
              class="btn-reject"
              :disabled="reviewing === loan.id"
              @click="reviewLoan(loan.id, 'rejected')"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              Reject
            </button>
          </div>
          <p v-if="errors[loan.id]" class="action-error">{{ errors[loan.id] }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminLoans',
  data() {
    return {
      loans: [],
      loading: false,
      filterStatus: 'pending',
      filterType: '',
      reviewing: null,
      actions: {},
      errors: {},
    }
  },
  computed: {
    filtered() {
      if (!this.filterType) return this.loans
      return this.loans.filter(l => l.loan_type === this.filterType)
    },
    counts() {
      return {
        pending:  this.loans.filter(l => l.status === 'pending').length,
        approved: this.loans.filter(l => l.status === 'approved' || l.status === 'active').length,
        rejected: this.loans.filter(l => l.status === 'rejected').length,
      }
    },
  },
  created() {
    this.fetchLoans()
  },
  methods: {
    token() {
      return localStorage.getItem('adminToken')
    },
    async fetchLoans() {
      this.loading = true
      try {
        const params = this.filterStatus ? { status: this.filterStatus } : {}
        const res = await axios.get('http://127.0.0.1:8000/accounts/admin/loans/', {
          params,
          headers: { Authorization: `Bearer ${this.token()}` },
        })
        this.loans = res.data
        this.loans.forEach(l => {
          if (!this.actions[l.id]) {
            this.actions[l.id] = { approvedAmount: '', note: '' }
          }
        })
      } catch (e) {
        console.error(e)
      } finally {
        this.loading = false
      }
    },
    applyFilter() {
      // filterType is client-side; filterStatus triggers a new fetch
    },
    async reviewLoan(id, decision) {
      const act = this.actions[id]
      this.errors[id] = ''
      if (decision === 'approved' && !act.approvedAmount) {
        this.errors[id] = 'Enter the approved amount.'
        return
      }
      this.reviewing = id
      try {
        const action = decision === 'approved' ? 'approve' : 'reject'
        const payload = { action, admin_note: act.note }
        if (action === 'approve') payload.approved_amount = act.approvedAmount
        await axios.patch(`http://127.0.0.1:8000/accounts/admin/loans/${id}/`, payload, {
          headers: { Authorization: `Bearer ${this.token()}` },
        })
        await this.fetchLoans()
      } catch (e) {
        this.errors[id] = e.response?.data?.error || 'Failed to update loan.'
      } finally {
        this.reviewing = null
      }
    },
    loanTypeLabel(type) {
      return { personal: 'Personal', home: 'Home', car: 'Car', education: 'Education' }[type] || type
    },
    statusLabel(s) {
      return { pending: 'Pending', approved: 'Approved', rejected: 'Rejected', active: 'Active', closed: 'Closed' }[s] || s
    },
    formatAmount(v) {
      return Number(v).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    },
    formatDate(d) {
      if (!d) return '—'
      return new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
    },
  },
}
</script>

<style scoped>
.admin-loans { display: flex; flex-direction: column; gap: 20px; }

/* Filter bar */
.filter-bar {
  display: flex;
  align-items: flex-end;
  gap: 16px;
  flex-wrap: wrap;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px 20px;
}
.filter-group { display: flex; flex-direction: column; gap: 6px; }
.filter-group label { font-size: 12px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: .5px; }
.filter-group select {
  padding: 8px 12px; border: 1px solid var(--border); border-radius: var(--radius-sm);
  font-size: 14px; background: var(--bg); color: var(--text); min-width: 140px;
}
.stats-chips { display: flex; gap: 8px; margin-left: auto; }
.stat-chip {
  padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 700;
}
.stat-chip.pending  { background: #fef3c7; color: #b45309; }
.stat-chip.approved { background: #d1fae5; color: #065f46; }
.stat-chip.rejected { background: #fee2e2; color: #991b1b; }

/* Loading / empty */
.loading-state, .empty-state {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 12px; padding: 60px 20px; color: var(--muted); text-align: center;
}
.loading-state svg, .empty-state svg { width: 48px; height: 48px; opacity: .4; }
.spinner {
  width: 36px; height: 36px; border: 3px solid var(--border);
  border-top-color: #6366f1; border-radius: 50%; animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Loans grid */
.loans-grid { display: flex; flex-direction: column; gap: 16px; }

.loan-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  border-left: 4px solid var(--border);
}
.loan-card.pending  { border-left-color: #f59e0b; }
.loan-card.approved, .loan-card.active { border-left-color: #10b981; }
.loan-card.rejected { border-left-color: #ef4444; }
.loan-card.closed   { border-left-color: #94a3b8; }

.loan-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 20px;
  background: #f8fafc;
  border-bottom: 1px solid var(--border);
}
.loan-meta { display: flex; align-items: center; gap: 10px; }

.loan-type-badge {
  padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700;
  text-transform: uppercase; letter-spacing: .5px;
}
.loan-type-badge.personal  { background: #ede9fe; color: #5b21b6; }
.loan-type-badge.home      { background: #dbeafe; color: #1d4ed8; }
.loan-type-badge.car       { background: #fce7f3; color: #9d174d; }
.loan-type-badge.education { background: #d1fae5; color: #065f46; }

.status-badge {
  padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;
}
.status-badge.pending  { background: #fef3c7; color: #b45309; }
.status-badge.approved, .status-badge.active { background: #d1fae5; color: #065f46; }
.status-badge.rejected { background: #fee2e2; color: #991b1b; }
.status-badge.closed   { background: #f1f5f9; color: #64748b; }

.loan-amount { font-size: 22px; font-weight: 800; color: var(--text); }

.loan-body { padding: 20px; display: flex; flex-direction: column; gap: 14px; }

.info-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px;
}
.info-item { display: flex; flex-direction: column; gap: 3px; }
.info-label { font-size: 11px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: .4px; }
.info-value { font-size: 14px; font-weight: 600; color: var(--text); }
.info-value.mono { font-family: monospace; letter-spacing: .5px; }

.purpose-block, .note-block { display: flex; flex-direction: column; gap: 4px; }
.purpose-text {
  font-size: 14px; color: var(--text); background: #f8fafc;
  border: 1px solid var(--border); border-radius: 8px; padding: 10px 14px;
  line-height: 1.5;
}
.note-text {
  font-size: 14px; color: #1d4ed8; background: #eff6ff;
  border: 1px solid #bfdbfe; border-radius: 8px; padding: 10px 14px;
  line-height: 1.5;
}

.review-meta { font-size: 12px; color: var(--muted); }

/* Action panel */
.action-panel {
  padding: 16px 20px;
  background: #f8fafc;
  border-top: 1px solid var(--border);
  display: flex; flex-direction: column; gap: 12px;
}
.action-fields { display: flex; gap: 12px; flex-wrap: wrap; }
.field-group { display: flex; flex-direction: column; gap: 6px; flex: 1; min-width: 180px; }
.field-group label { font-size: 12px; font-weight: 600; color: var(--muted); }
.field-group input {
  padding: 9px 12px; border: 1px solid var(--border); border-radius: var(--radius-sm);
  font-size: 14px; background: #fff; color: var(--text);
}
.field-group input:focus { outline: none; border-color: #6366f1; }

.action-btns { display: flex; gap: 10px; }

.btn-approve, .btn-reject {
  display: flex; align-items: center; gap: 7px;
  padding: 10px 20px; border-radius: var(--radius-sm);
  font-size: 14px; font-weight: 600; cursor: pointer; border: none;
  transition: all .18s;
}
.btn-approve svg, .btn-reject svg { width: 16px; height: 16px; }

.btn-approve {
  background: #10b981; color: #fff;
}
.btn-approve:hover:not(:disabled) { background: #059669; }
.btn-approve:disabled { opacity: .6; cursor: not-allowed; }

.btn-reject {
  background: #fee2e2; color: #dc2626;
}
.btn-reject:hover:not(:disabled) { background: #fecaca; }
.btn-reject:disabled { opacity: .6; cursor: not-allowed; }

.action-error { font-size: 13px; color: var(--danger); font-weight: 500; }
</style>
