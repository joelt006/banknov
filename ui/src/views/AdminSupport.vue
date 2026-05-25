<template>
  <div class="admin-support">

    <!-- Ticket detail -->
    <div v-if="activeTicket" class="ticket-detail">
      <div class="detail-top">
        <button class="back-btn" @click="activeTicket = null">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
          All tickets
        </button>
        <div class="detail-controls">
          <div class="control-group">
            <label>Status</label>
            <select v-model="editStatus" @change="updateTicket">
              <option value="open">Open</option>
              <option value="in_progress">In Progress</option>
              <option value="resolved">Resolved</option>
              <option value="closed">Closed</option>
            </select>
          </div>
          <div class="control-group">
            <label>Priority</label>
            <select v-model="editPriority" @change="updateTicket">
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>
          </div>
        </div>
      </div>

      <div class="detail-info">
        <div class="info-left">
          <div class="ticket-num">{{ activeTicket.ticket_number }}</div>
          <h2 class="detail-subject">{{ activeTicket.subject }}</h2>
          <div class="detail-badges">
            <span class="status-badge" :class="activeTicket.status">{{ statusLabel(activeTicket.status) }}</span>
            <span class="priority-badge" :class="activeTicket.priority">{{ capitalize(activeTicket.priority) }}</span>
            <span class="cat-chip">{{ categoryLabel(activeTicket.category) }}</span>
          </div>
        </div>
        <div class="user-card">
          <div class="user-avatar-lg">{{ (activeTicket.username || 'U')[0].toUpperCase() }}</div>
          <div>
            <div class="user-name">{{ activeTicket.username }}</div>
            <div class="user-email">{{ activeTicket.user_email }}</div>
            <div class="user-opened">Opened {{ formatDate(activeTicket.created_at) }}</div>
          </div>
        </div>
      </div>

      <!-- Thread -->
      <div class="thread" ref="thread">
        <div
          v-for="msg in activeTicket.messages"
          :key="msg.id"
          class="message"
          :class="msg.is_staff ? 'staff' : 'user'"
        >
          <div class="msg-avatar" :class="msg.is_staff ? 'staff-avatar' : 'user-avatar'">
            {{ msg.is_staff ? 'MB' : (msg.sender || 'U')[0].toUpperCase() }}
          </div>
          <div class="msg-bubble">
            <div class="msg-sender">{{ msg.is_staff ? 'MyBank Support' : msg.sender }}</div>
            <p class="msg-body">{{ msg.body }}</p>
            <div class="msg-time">{{ timeAgo(msg.created_at) }}</div>
          </div>
        </div>
      </div>

      <!-- Admin reply -->
      <div class="reply-box">
        <textarea
          v-model="replyBody"
          rows="3"
          placeholder="Type your staff reply…"
          @keydown.ctrl.enter="sendReply"
        ></textarea>
        <div class="reply-actions">
          <span class="reply-hint">Ctrl+Enter to send</span>
          <button class="send-btn" :disabled="!replyBody.trim() || replying" @click="sendReply">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
            {{ replying ? 'Sending…' : 'Send Reply' }}
          </button>
        </div>
        <p v-if="replyError" class="form-error">{{ replyError }}</p>
      </div>
    </div>

    <!-- List view -->
    <div v-else>
      <!-- Filter bar -->
      <div class="filter-bar">
        <div class="filter-group">
          <label>Status</label>
          <select v-model="filterStatus" @change="fetchTickets">
            <option value="">All</option>
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="resolved">Resolved</option>
            <option value="closed">Closed</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Priority</label>
          <select v-model="filterPriority" @change="fetchTickets">
            <option value="">All</option>
            <option value="urgent">Urgent</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Category</label>
          <select v-model="filterCategory" @change="fetchTickets">
            <option value="">All</option>
            <option value="account">Account</option>
            <option value="transaction">Transaction</option>
            <option value="card">Card</option>
            <option value="loan">Loan</option>
            <option value="fd">Fixed Deposit</option>
            <option value="technical">Technical</option>
            <option value="other">Other</option>
          </select>
        </div>
        <div class="stats-chips">
          <div class="stat-chip open">{{ counts.open }} Open</div>
          <div class="stat-chip in_progress">{{ counts.in_progress }} In Progress</div>
          <div class="stat-chip urgent">{{ counts.urgent }} Urgent</div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="state-box">
        <div class="spinner"></div>
        <p>Loading tickets…</p>
      </div>

      <!-- Empty -->
      <div v-else-if="tickets.length === 0" class="state-box">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        <p>No tickets found</p>
      </div>

      <!-- Table -->
      <div v-else class="ticket-table">
        <div class="table-header">
          <span>Ticket</span>
          <span>Customer</span>
          <span>Category</span>
          <span>Status</span>
          <span>Priority</span>
          <span>Messages</span>
          <span>Date</span>
        </div>
        <div
          v-for="t in tickets"
          :key="t.id"
          class="table-row"
          @click="openTicket(t.id)"
        >
          <span class="col-ticket">
            <span class="tn">{{ t.ticket_number }}</span>
            <span class="subject-text">{{ t.subject }}</span>
          </span>
          <span class="col-user">
            <span class="uname">{{ t.username }}</span>
            <span class="uemail">{{ t.user_email }}</span>
          </span>
          <span><span class="cat-chip sm">{{ categoryLabel(t.category) }}</span></span>
          <span><span class="status-badge" :class="t.status">{{ statusLabel(t.status) }}</span></span>
          <span><span class="priority-badge" :class="t.priority">{{ capitalize(t.priority) }}</span></span>
          <span class="msg-count-col">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            {{ t.message_count }}
          </span>
          <span class="col-date">{{ formatDate(t.created_at) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminSupport',
  data() {
    return {
      tickets: [],
      loading: false,
      filterStatus: 'open',
      filterPriority: '',
      filterCategory: '',
      activeTicket: null,
      editStatus: '',
      editPriority: '',
      replyBody: '',
      replying: false,
      replyError: '',
    }
  },
  computed: {
    counts() {
      return {
        open: this.tickets.filter(t => t.status === 'open').length,
        in_progress: this.tickets.filter(t => t.status === 'in_progress').length,
        urgent: this.tickets.filter(t => t.priority === 'urgent').length,
      }
    },
  },
  created() {
    this.fetchTickets()
  },
  methods: {
    token() { return localStorage.getItem('adminToken') },
    headers() { return { Authorization: `Bearer ${this.token()}` } },
    async fetchTickets() {
      this.loading = true
      try {
        const params = {}
        if (this.filterStatus)   params.status = this.filterStatus
        if (this.filterPriority) params.priority = this.filterPriority
        if (this.filterCategory) params.category = this.filterCategory
        const res = await axios.get('http://127.0.0.1:8000/accounts/admin/support/', { params, headers: this.headers() })
        this.tickets = res.data
      } catch (e) { console.error(e) }
      finally { this.loading = false }
    },
    async openTicket(id) {
      try {
        const res = await axios.get(`http://127.0.0.1:8000/accounts/admin/support/${id}/`, { headers: this.headers() })
        this.activeTicket = res.data
        this.editStatus = res.data.status
        this.editPriority = res.data.priority
        this.replyBody = ''
        this.replyError = ''
        await this.$nextTick()
        this.scrollThread()
      } catch (e) { console.error(e) }
    },
    scrollThread() {
      const el = this.$refs.thread
      if (el) el.scrollTop = el.scrollHeight
    },
    async updateTicket() {
      try {
        const res = await axios.patch(
          `http://127.0.0.1:8000/accounts/admin/support/${this.activeTicket.id}/`,
          { status: this.editStatus, priority: this.editPriority },
          { headers: this.headers() }
        )
        this.activeTicket.status = res.data.status
        this.activeTicket.priority = res.data.priority
      } catch (e) { console.error(e) }
    },
    async sendReply() {
      if (!this.replyBody.trim()) return
      this.replying = true
      this.replyError = ''
      try {
        const res = await axios.post(
          `http://127.0.0.1:8000/accounts/admin/support/${this.activeTicket.id}/`,
          { body: this.replyBody },
          { headers: this.headers() }
        )
        this.activeTicket = { ...res.data, username: this.activeTicket.username, user_email: this.activeTicket.user_email }
        this.editStatus = res.data.status
        this.replyBody = ''
        await this.$nextTick()
        this.scrollThread()
      } catch (e) {
        this.replyError = e.response?.data?.error || 'Failed to send reply.'
      } finally {
        this.replying = false
      }
    },
    statusLabel(s) { return { open: 'Open', in_progress: 'In Progress', resolved: 'Resolved', closed: 'Closed' }[s] || s },
    categoryLabel(c) {
      return { account: 'Account', transaction: 'Transaction', card: 'Card', loan: 'Loan', fd: 'Fixed Deposit', technical: 'Technical', other: 'Other' }[c] || c
    },
    capitalize(s) { return s ? s[0].toUpperCase() + s.slice(1) : '' },
    formatDate(iso) {
      return new Date(iso).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
    },
    timeAgo(iso) {
      const diff = (Date.now() - new Date(iso)) / 1000
      if (diff < 60) return 'just now'
      if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
      if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
      return `${Math.floor(diff / 86400)}d ago`
    },
  },
}
</script>

<style scoped>
.admin-support { display: flex; flex-direction: column; gap: 20px; }

/* Filter bar */
.filter-bar {
  display: flex; align-items: flex-end; gap: 14px; flex-wrap: wrap;
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 16px 20px;
}
.filter-group { display: flex; flex-direction: column; gap: 6px; }
.filter-group label { font-size: 11px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: .5px; }
.filter-group select {
  padding: 8px 12px; border: 1px solid var(--border); border-radius: var(--radius-sm);
  font-size: 13px; background: var(--bg); color: var(--text); min-width: 130px;
}
.stats-chips { display: flex; gap: 8px; margin-left: auto; }
.stat-chip { padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; }
.stat-chip.open        { background: #dbeafe; color: #1d4ed8; }
.stat-chip.in_progress { background: #fef3c7; color: #b45309; }
.stat-chip.urgent      { background: #fee2e2; color: #dc2626; }

/* State */
.state-box {
  display: flex; flex-direction: column; align-items: center; gap: 12px;
  padding: 60px 20px; color: var(--muted); font-size: 14px; text-align: center;
}
.state-box svg { width: 48px; height: 48px; opacity: .35; }
.spinner {
  width: 34px; height: 34px; border: 3px solid var(--border);
  border-top-color: #6366f1; border-radius: 50%; animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Table */
.ticket-table { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }
.table-header {
  display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 0.6fr 1fr;
  padding: 10px 16px; background: #f8fafc; border-bottom: 1px solid var(--border);
  font-size: 11px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: .5px; gap: 8px;
}
.table-row {
  display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 0.6fr 1fr;
  padding: 14px 16px; border-bottom: 1px solid #f1f5f9; cursor: pointer;
  transition: background .15s; align-items: center; gap: 8px;
}
.table-row:last-child { border-bottom: none; }
.table-row:hover { background: #f8fafc; }

.col-ticket { display: flex; flex-direction: column; gap: 2px; }
.tn { font-size: 11px; font-weight: 700; color: var(--muted); font-family: monospace; letter-spacing: .4px; }
.subject-text { font-size: 13px; font-weight: 600; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 200px; }
.col-user { display: flex; flex-direction: column; gap: 2px; }
.uname  { font-size: 13px; font-weight: 600; color: var(--text); }
.uemail { font-size: 11px; color: var(--muted); }
.col-date { font-size: 12px; color: var(--muted); }
.msg-count-col { display: flex; align-items: center; gap: 4px; font-size: 13px; color: var(--muted); }
.msg-count-col svg { width: 13px; height: 13px; }

/* Badges */
.status-badge {
  padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; white-space: nowrap;
}
.status-badge.open        { background: #dbeafe; color: #1d4ed8; }
.status-badge.in_progress { background: #fef3c7; color: #b45309; }
.status-badge.resolved    { background: #d1fae5; color: #065f46; }
.status-badge.closed      { background: #f1f5f9; color: #64748b; }

.priority-badge {
  padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; white-space: nowrap;
}
.priority-badge.low    { background: #f0fdf4; color: #15803d; }
.priority-badge.medium { background: #eff6ff; color: #1d4ed8; }
.priority-badge.high   { background: #fef3c7; color: #b45309; }
.priority-badge.urgent { background: #fee2e2; color: #dc2626; }

.cat-chip { padding: 3px 9px; border-radius: 12px; font-size: 11px; font-weight: 600; background: #f1f5f9; color: #475569; }
.cat-chip.sm { font-size: 11px; }

/* ── Detail view ── */
.detail-top {
  display: flex; align-items: center; gap: 16px; flex-wrap: wrap;
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 14px 18px; margin-bottom: 16px;
}
.back-btn {
  display: flex; align-items: center; gap: 6px;
  padding: 8px 14px; border-radius: var(--radius-sm); border: 1px solid var(--border);
  background: var(--bg); font-size: 13px; font-weight: 600; cursor: pointer; color: var(--text);
  transition: all .18s;
}
.back-btn:hover { background: #fff; border-color: #6366f1; color: #6366f1; }
.back-btn svg { width: 16px; height: 16px; }
.detail-controls { display: flex; gap: 10px; margin-left: auto; flex-wrap: wrap; }
.control-group { display: flex; align-items: center; gap: 8px; }
.control-group label { font-size: 12px; font-weight: 600; color: var(--muted); }
.control-group select {
  padding: 7px 12px; border: 1px solid var(--border); border-radius: var(--radius-sm);
  font-size: 13px; background: var(--bg);
}

.detail-info {
  display: flex; align-items: flex-start; justify-content: space-between; flex-wrap: wrap; gap: 16px;
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 18px 20px; margin-bottom: 16px;
}
.ticket-num { font-size: 12px; font-weight: 700; color: var(--muted); font-family: monospace; letter-spacing: .5px; margin-bottom: 4px; }
.detail-subject { font-size: 18px; font-weight: 700; color: var(--text); margin-bottom: 8px; }
.detail-badges { display: flex; gap: 8px; flex-wrap: wrap; }

.user-card {
  display: flex; align-items: center; gap: 12px;
  background: #f8fafc; border: 1px solid var(--border); border-radius: 10px; padding: 12px 16px;
}
.user-avatar-lg {
  width: 44px; height: 44px; border-radius: 50%; background: #6366f1;
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 18px; font-weight: 700; flex-shrink: 0;
}
.user-name   { font-size: 14px; font-weight: 700; color: var(--text); }
.user-email  { font-size: 12px; color: var(--muted); }
.user-opened { font-size: 11px; color: #94a3b8; margin-top: 2px; }

/* Thread */
.thread {
  display: flex; flex-direction: column; gap: 16px;
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 20px; max-height: 380px; overflow-y: auto; margin-bottom: 16px;
}
.message { display: flex; gap: 12px; }
.message.user  { flex-direction: row; }
.message.staff { flex-direction: row-reverse; }
.msg-avatar {
  width: 36px; height: 36px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700; color: #fff;
}
.user-avatar  { background: var(--blue); }
.staff-avatar { background: linear-gradient(135deg, #6366f1, #4f46e5); }
.msg-bubble { max-width: 72%; }
.message.staff .msg-bubble { display: flex; flex-direction: column; align-items: flex-end; }
.msg-sender { font-size: 11px; font-weight: 700; color: var(--muted); margin-bottom: 4px; }
.msg-body {
  font-size: 14px; line-height: 1.6; padding: 12px 16px; border-radius: 14px;
  white-space: pre-wrap; word-break: break-word;
}
.message.user  .msg-body { background: #f1f5f9; color: var(--text); border-bottom-left-radius: 4px; }
.message.staff .msg-body { background: linear-gradient(135deg, #6366f1, #4f46e5); color: #fff; border-bottom-right-radius: 4px; }
.msg-time { font-size: 11px; color: #94a3b8; margin-top: 4px; }
.message.staff .msg-time { text-align: right; }

/* Reply */
.reply-box { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 16px; }
.reply-box textarea {
  width: 100%; resize: vertical; border: 1px solid var(--border); border-radius: var(--radius-sm);
  padding: 12px; font-size: 14px; font-family: inherit; color: var(--text); background: var(--bg); min-height: 80px;
}
.reply-box textarea:focus { outline: none; border-color: #6366f1; }
.reply-actions { display: flex; align-items: center; justify-content: space-between; margin-top: 10px; }
.reply-hint { font-size: 12px; color: var(--muted); }
.send-btn {
  display: flex; align-items: center; gap: 7px;
  padding: 10px 22px; border-radius: var(--radius-sm); border: none;
  background: linear-gradient(135deg, #6366f1, #4f46e5); color: #fff;
  font-size: 14px; font-weight: 600; cursor: pointer; transition: all .18s;
}
.send-btn svg { width: 15px; height: 15px; }
.send-btn:hover:not(:disabled) { opacity: .9; }
.send-btn:disabled { opacity: .5; cursor: not-allowed; }
.form-error { font-size: 13px; color: var(--danger); font-weight: 500; margin-top: 8px; }
</style>
