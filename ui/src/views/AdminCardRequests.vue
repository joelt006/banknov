<template>
  <div class="card-requests-page">

    <!-- Header -->
    <div class="page-header">
      <div>
        <h2>Card Requests</h2>
        <p>Review and approve or reject customer card applications</p>
      </div>
      <div class="header-stats">
        <div class="hstat">
          <span class="hstat-val">{{ requests.length }}</span>
          <span class="hstat-lbl">Total</span>
        </div>
        <div class="hstat hstat-amber">
          <span class="hstat-val">{{ countByStatus('pending') }}</span>
          <span class="hstat-lbl">Pending</span>
        </div>
        <div class="hstat hstat-green">
          <span class="hstat-val">{{ countByStatus('approved') }}</span>
          <span class="hstat-lbl">Approved</span>
        </div>
        <div class="hstat hstat-red">
          <span class="hstat-val">{{ countByStatus('rejected') }}</span>
          <span class="hstat-lbl">Rejected</span>
        </div>
      </div>
    </div>

    <!-- Filter tabs -->
    <div class="filter-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.value"
        class="tab-btn"
        :class="{ active: activeTab === tab.value }"
        @click="setTab(tab.value)"
      >
        {{ tab.label }}
        <span class="tab-count" :class="'count-' + tab.value">{{ tab.value === 'all' ? requests.length : countByStatus(tab.value) }}</span>
      </button>
    </div>

    <!-- Table -->
    <div class="table-card">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading card requests…</p>
      </div>

      <div v-else-if="filtered.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
        <p>No {{ activeTab !== 'all' ? activeTab : '' }} card requests</p>
      </div>

      <table v-else class="req-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Card Type</th>
            <th>Customer</th>
            <th>Account</th>
            <th>Requested</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="req in filtered" :key="req.id">
            <td class="id-cell">{{ req.id }}</td>
            <td>
              <span class="type-badge" :class="'type-' + req.card_type">
                <svg v-if="req.card_type === 'platinum'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                <svg v-else-if="req.card_type === 'gold'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="6"/><path d="M15.477 12.89L17 22l-5-3-5 3 1.523-9.11"/></svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
                {{ req.card_type.charAt(0).toUpperCase() + req.card_type.slice(1) }}
              </span>
            </td>
            <td>
              <div class="customer-cell">
                <div class="cust-avatar">{{ (req.account_holder_name || '?')[0].toUpperCase() }}</div>
                <div>
                  <div class="cust-name">{{ req.account_holder_name }}</div>
                  <div class="cust-email">{{ req.email || '—' }}</div>
                </div>
              </div>
            </td>
            <td class="mono-cell">{{ req.account_number }}</td>
            <td class="date-cell">{{ formatDate(req.requested_at) }}</td>
            <td>
              <span class="status-badge" :class="'status-' + req.status">
                <span class="status-dot"></span>
                {{ req.status.charAt(0).toUpperCase() + req.status.slice(1) }}
              </span>
              <div v-if="req.reviewed_by" class="reviewed-by">by {{ req.reviewed_by }}</div>
            </td>
            <td>
              <!-- Already decided -->
              <div v-if="req.status !== 'pending'" class="decided-cell">
                <span v-if="req.admin_note" class="note-preview" :title="req.admin_note">
                  "{{ req.admin_note.length > 40 ? req.admin_note.slice(0, 40) + '…' : req.admin_note }}"
                </span>
                <span v-else class="no-note">No note</span>
              </div>

              <!-- Pending: inline review -->
              <div v-else-if="reviewingId !== req.id" class="action-btns">
                <button class="action-btn btn-approve" @click="startReview(req.id, 'approve')">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                  Approve
                </button>
                <button class="action-btn btn-reject" @click="startReview(req.id, 'reject')">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                  Reject
                </button>
              </div>

              <!-- Inline review form -->
              <div v-else class="review-form">
                <div class="review-header">
                  <span class="review-action-label" :class="reviewAction === 'approve' ? 'label-approve' : 'label-reject'">
                    {{ reviewAction === 'approve' ? 'Approving' : 'Rejecting' }}
                  </span>
                  <button class="cancel-review" @click="cancelReview">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                  </button>
                </div>
                <textarea
                  v-model="reviewNote"
                  class="review-note"
                  :placeholder="reviewAction === 'reject' ? 'Reason for rejection (optional)…' : 'Approval note (optional)…'"
                  rows="2"
                ></textarea>
                <button
                  class="confirm-btn"
                  :class="reviewAction === 'approve' ? 'confirm-approve' : 'confirm-reject'"
                  :disabled="submitting"
                  @click="submitReview(req)"
                >
                  <span v-if="submitting" class="btn-spinner"></span>
                  {{ submitting ? 'Saving…' : (reviewAction === 'approve' ? 'Confirm Approval' : 'Confirm Rejection') }}
                </button>
              </div>
            </td>
          </tr>
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
  name: 'AdminCardRequests',
  data() {
    return {
      requests: [],
      loading: true,
      activeTab: 'pending',
      tabs: [
        { label: 'All',      value: 'all' },
        { label: 'Pending',  value: 'pending' },
        { label: 'Approved', value: 'approved' },
        { label: 'Rejected', value: 'rejected' },
      ],
      reviewingId: null,
      reviewAction: '',
      reviewNote: '',
      submitting: false,
      toast: { show: false, type: 'success', message: '' },
    };
  },
  computed: {
    filtered() {
      if (this.activeTab === 'all') return this.requests;
      return this.requests.filter(r => r.status === this.activeTab);
    },
  },
  mounted() { this.fetchRequests(); },
  methods: {
    async fetchRequests() {
      this.loading = true;
      try {
        const res = await adminApiClient.get('/accounts/admin/card-requests/');
        this.requests = res.data;
      } catch {
        this.showToast('error', 'Failed to load card requests');
      } finally {
        this.loading = false;
      }
    },

    countByStatus(s) { return this.requests.filter(r => r.status === s).length; },

    setTab(val) {
      this.activeTab = val;
      this.cancelReview();
    },

    startReview(id, action) {
      this.reviewingId = id;
      this.reviewAction = action;
      this.reviewNote = '';
    },

    cancelReview() {
      this.reviewingId = null;
      this.reviewAction = '';
      this.reviewNote = '';
    },

    async submitReview(req) {
      this.submitting = true;
      try {
        const res = await adminApiClient.patch(`/accounts/admin/card-requests/${req.id}/`, {
          action: this.reviewAction,
          admin_note: this.reviewNote,
        });
        Object.assign(req, res.data);
        this.showToast('success', `Request ${res.data.status} successfully`);
        this.cancelReview();
      } catch (err) {
        this.showToast('error', err.response?.data?.error || 'Failed to update request');
      } finally {
        this.submitting = false;
      }
    },

    formatDate(iso) {
      return new Date(iso).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
    },

    showToast(type, message) {
      this.toast = { show: true, type, message };
      setTimeout(() => { this.toast.show = false; }, 3500);
    },
  },
};
</script>

<style scoped>
.card-requests-page { display: flex; flex-direction: column; gap: 24px; }

/* Header */
.page-header { display: flex; align-items: flex-start; justify-content: space-between; flex-wrap: wrap; gap: 16px; }
.page-header h2 { font-size: 22px; font-weight: 800; color: #0f172a; margin-bottom: 4px; }
.page-header p  { font-size: 14px; color: #64748b; }

.header-stats { display: flex; gap: 12px; }
.hstat { display: flex; flex-direction: column; align-items: center; background: #f1f5f9; border-radius: 10px; padding: 12px 18px; min-width: 72px; }
.hstat-amber { background: #fffbeb; }
.hstat-green { background: #f0fdf4; }
.hstat-red   { background: #fff1f2; }
.hstat-val { font-size: 22px; font-weight: 800; color: #0f172a; }
.hstat-amber .hstat-val { color: #d97706; }
.hstat-green .hstat-val { color: #16a34a; }
.hstat-red   .hstat-val { color: #dc2626; }
.hstat-lbl { font-size: 11px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: .5px; }

/* Tabs */
.filter-tabs { display: flex; gap: 4px; background: #f1f5f9; border-radius: 12px; padding: 4px; width: fit-content; }
.tab-btn {
  display: flex; align-items: center; gap: 8px;
  padding: 8px 18px; border: none; border-radius: 9px;
  font-size: 13px; font-weight: 600; color: #64748b;
  background: transparent; cursor: pointer; transition: all .15s;
}
.tab-btn:hover { background: rgba(255,255,255,.7); color: #1e293b; }
.tab-btn.active { background: #fff; color: #1e293b; box-shadow: 0 1px 4px rgba(0,0,0,.1); }

.tab-count { display: inline-flex; align-items: center; justify-content: center; min-width: 20px; height: 20px; border-radius: 10px; font-size: 11px; font-weight: 700; background: #e2e8f0; color: #64748b; padding: 0 5px; }
.tab-btn.active .tab-count { background: #e0e7ff; color: #4f46e5; }
.count-pending  { background: #fef9c3 !important; color: #854d0e !important; }
.count-approved { background: #dcfce7 !important; color: #15803d !important; }
.count-rejected { background: #fee2e2 !important; color: #b91c1c !important; }

/* Table */
.table-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 14px; overflow: hidden; box-shadow: 0 2px 12px rgba(15,32,68,.06); }

.loading-state, .empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; padding: 64px; color: #94a3b8; }
.loading-state .spinner { width: 32px; height: 32px; border: 3px solid #e2e8f0; border-top-color: #6366f1; border-radius: 50%; animation: spin .7s linear infinite; }
.empty-state svg { width: 48px; height: 48px; }
.empty-state p { font-size: 15px; font-weight: 500; }

.req-table { width: 100%; border-collapse: collapse; }
.req-table thead tr { background: #f8fafc; border-bottom: 2px solid #e2e8f0; }
.req-table th { padding: 12px 16px; text-align: left; font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: .6px; }
.req-table tbody tr { border-bottom: 1px solid #f1f5f9; transition: background .12s; }
.req-table tbody tr:last-child { border-bottom: none; }
.req-table tbody tr:hover { background: #fafbff; }
.req-table td { padding: 14px 16px; vertical-align: middle; }

.id-cell { font-size: 12px; color: #94a3b8; font-weight: 600; }
.mono-cell { font-family: 'Courier New', monospace; font-size: 12px; color: #475569; font-weight: 600; }
.date-cell { font-size: 12px; color: #64748b; }

/* Type badge */
.type-badge { display: inline-flex; align-items: center; gap: 6px; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; }
.type-badge svg { width: 13px; height: 13px; }
.type-classic  { background: #eff6ff; color: #1d4ed8; }
.type-gold     { background: #fffbeb; color: #92400e; }
.type-platinum { background: #f1f5f9; color: #374151; }

/* Customer cell */
.customer-cell { display: flex; align-items: center; gap: 10px; }
.cust-avatar { width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #4f46e5); display: flex; align-items: center; justify-content: center; color: #fff; font-size: 12px; font-weight: 700; flex-shrink: 0; }
.cust-name  { font-size: 13px; font-weight: 600; color: #1e293b; }
.cust-email { font-size: 11px; color: #94a3b8; }

/* Status badge */
.status-badge { display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; }
.status-dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }
.status-pending  { background: #fffbeb; color: #d97706; }
.status-approved { background: #f0fdf4; color: #16a34a; }
.status-rejected { background: #fff1f2; color: #dc2626; }

.reviewed-by { font-size: 10px; color: #94a3b8; margin-top: 3px; }

/* Decided cell */
.decided-cell { font-size: 12px; }
.note-preview { color: #64748b; font-style: italic; }
.no-note { color: #cbd5e1; }

/* Action buttons */
.action-btns { display: flex; gap: 8px; flex-wrap: wrap; }
.action-btn { display: inline-flex; align-items: center; gap: 5px; padding: 6px 12px; border: none; border-radius: 7px; font-size: 12px; font-weight: 700; cursor: pointer; transition: all .15s; }
.action-btn svg { width: 13px; height: 13px; }
.btn-approve { background: #f0fdf4; color: #16a34a; }
.btn-approve:hover { background: #bbf7d0; }
.btn-reject  { background: #fff1f2; color: #dc2626; }
.btn-reject:hover  { background: #fecaca; }

/* Review form */
.review-form { display: flex; flex-direction: column; gap: 8px; min-width: 240px; }
.review-header { display: flex; align-items: center; justify-content: space-between; }
.review-action-label { font-size: 12px; font-weight: 700; }
.label-approve { color: #16a34a; }
.label-reject  { color: #dc2626; }
.cancel-review { background: none; border: none; cursor: pointer; color: #94a3b8; padding: 2px; }
.cancel-review:hover { color: #475569; }
.cancel-review svg { width: 14px; height: 14px; display: block; }

.review-note {
  width: 100%; border: 1.5px solid #e2e8f0; border-radius: 7px;
  padding: 8px 10px; font-size: 12px; resize: none; outline: none;
  font-family: inherit; color: #1e293b; transition: border-color .15s;
}
.review-note:focus { border-color: #6366f1; }

.confirm-btn {
  display: flex; align-items: center; justify-content: center; gap: 6px;
  padding: 8px 14px; border: none; border-radius: 7px;
  font-size: 12px; font-weight: 700; cursor: pointer; color: #fff;
  transition: opacity .15s;
}
.confirm-btn:disabled { opacity: .6; cursor: not-allowed; }
.confirm-approve { background: #16a34a; }
.confirm-approve:hover:not(:disabled) { background: #15803d; }
.confirm-reject  { background: #dc2626; }
.confirm-reject:hover:not(:disabled)  { background: #b91c1c; }

.btn-spinner { width: 13px; height: 13px; border: 2px solid rgba(255,255,255,.3); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; }

/* Toast */
.toast { position: fixed; bottom: 28px; right: 28px; display: flex; align-items: center; gap: 10px; padding: 14px 20px; border-radius: 12px; font-size: 14px; font-weight: 600; z-index: 9999; box-shadow: 0 8px 32px rgba(0,0,0,.15); }
.toast svg { width: 18px; height: 18px; flex-shrink: 0; }
.toast-success { background: #16a34a; color: #fff; }
.toast-error   { background: #dc2626; color: #fff; }
.toast-enter-active, .toast-leave-active { transition: all .3s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(16px); }

@keyframes spin { to { transform: rotate(360deg); } }
</style>
