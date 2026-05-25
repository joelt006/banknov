<template>
  <div class="support-page">
    <!-- Ticket detail view -->
    <div v-if="activeTicket" class="ticket-detail">
      <div class="detail-header">
        <button class="back-btn" @click="activeTicket = null">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
          Back to tickets
        </button>
        <div class="detail-meta">
          <span class="ticket-num">{{ activeTicket.ticket_number }}</span>
          <span class="status-badge" :class="activeTicket.status">{{ statusLabel(activeTicket.status) }}</span>
          <span class="priority-badge" :class="activeTicket.priority">{{ capitalize(activeTicket.priority) }}</span>
          <span class="cat-chip">{{ categoryLabel(activeTicket.category) }}</span>
        </div>
      </div>
      <h2 class="detail-subject">{{ activeTicket.subject }}</h2>
      <p class="detail-opened">Opened {{ formatDate(activeTicket.created_at) }}</p>

      <!-- Message thread -->
      <div class="thread" ref="thread">
        <div
          v-for="msg in activeTicket.messages"
          :key="msg.id"
          class="message"
          :class="msg.is_staff ? 'staff' : 'user'"
        >
          <div class="msg-avatar" :class="msg.is_staff ? 'staff-avatar' : 'user-avatar'">
            {{ msg.is_staff ? 'MB' : userInitial }}
          </div>
          <div class="msg-bubble">
            <div class="msg-sender">{{ msg.is_staff ? 'MyBank Support' : msg.sender }}</div>
            <p class="msg-body">{{ msg.body }}</p>
            <div class="msg-time">{{ timeAgo(msg.created_at) }}</div>
          </div>
        </div>
      </div>

      <!-- Reply box -->
      <div v-if="activeTicket.status !== 'resolved' && activeTicket.status !== 'closed'" class="reply-box">
        <textarea
          v-model="replyBody"
          placeholder="Type your reply…"
          rows="3"
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
      <div v-else class="ticket-closed-notice">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        This ticket is {{ activeTicket.status }}. Open a new ticket if you need further help.
      </div>
    </div>

    <!-- Ticket list + create form -->
    <div v-else class="list-view">
      <div class="list-grid">
        <!-- My Tickets -->
        <div class="panel">
          <div class="panel-header">
            <h2>My Tickets</h2>
            <div class="status-filter">
              <select v-model="listFilter">
                <option value="">All</option>
                <option value="open">Open</option>
                <option value="in_progress">In Progress</option>
                <option value="resolved">Resolved</option>
                <option value="closed">Closed</option>
              </select>
            </div>
          </div>

          <div v-if="loading" class="state-box">
            <div class="spinner"></div>
            <p>Loading tickets…</p>
          </div>
          <div v-else-if="filteredTickets.length === 0" class="state-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            <p>No tickets yet. Raise one if you need help!</p>
          </div>
          <div v-else class="ticket-list">
            <div
              v-for="t in filteredTickets"
              :key="t.id"
              class="ticket-row"
              @click="openTicket(t.id)"
            >
              <div class="ticket-row-left">
                <div class="ticket-row-num">{{ t.ticket_number }}</div>
                <div class="ticket-row-subject">{{ t.subject }}</div>
                <div class="ticket-row-cat">{{ categoryLabel(t.category) }}</div>
              </div>
              <div class="ticket-row-right">
                <span class="status-badge sm" :class="t.status">{{ statusLabel(t.status) }}</span>
                <span class="ticket-date">{{ formatDate(t.created_at) }}</span>
                <span class="msg-count">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
                  {{ t.message_count }}
                </span>
                <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
              </div>
            </div>
          </div>
        </div>

        <!-- New Ticket form -->
        <div class="panel new-ticket-panel">
          <div class="panel-header"><h2>Raise a Ticket</h2></div>

          <form class="ticket-form" @submit.prevent="createTicket">
            <div class="form-group">
              <label>Category</label>
              <select v-model="form.category">
                <option value="account">Account Issue</option>
                <option value="transaction">Transaction Issue</option>
                <option value="card">Card Issue</option>
                <option value="loan">Loan Issue</option>
                <option value="fd">Fixed Deposit Issue</option>
                <option value="technical">Technical Problem</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div class="form-group">
              <label>Subject</label>
              <input
                v-model="form.subject"
                type="text"
                placeholder="Brief description of your issue"
                maxlength="150"
              />
              <span class="char-count">{{ form.subject.length }}/150</span>
            </div>

            <div class="form-group">
              <label>Describe your issue</label>
              <textarea
                v-model="form.body"
                rows="5"
                placeholder="Please provide as much detail as possible — account number, transaction ID, date, etc."
              ></textarea>
            </div>

            <p v-if="createError" class="form-error">{{ createError }}</p>
            <button type="submit" class="submit-btn" :disabled="creating">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
              {{ creating ? 'Submitting…' : 'Submit Ticket' }}
            </button>
          </form>

          <!-- FAQ -->
          <div class="faq-section">
            <h3>Quick Help</h3>
            <div v-for="(faq, i) in faqs" :key="i" class="faq-item">
              <button class="faq-q" @click="openFaq = openFaq === i ? null : i">
                {{ faq.q }}
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :style="{ transform: openFaq === i ? 'rotate(180deg)' : '' }"><polyline points="6 9 12 15 18 9"/></svg>
              </button>
              <div v-if="openFaq === i" class="faq-a">{{ faq.a }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Support',
  data() {
    return {
      tickets: [],
      loading: false,
      listFilter: '',
      activeTicket: null,
      replyBody: '',
      replying: false,
      replyError: '',
      form: { category: 'other', subject: '', body: '' },
      creating: false,
      createError: '',
      openFaq: null,
      faqs: [
        { q: 'How do I reset my transaction PIN?', a: 'Go to Security Settings from the sidebar, then select "Change Transaction PIN". You\'ll need to verify with OTP.' },
        { q: 'My transfer is showing as failed. What do I do?', a: 'Check your Transaction History for the failure reason. If funds were debited but not received, raise a ticket with the transaction date and amount.' },
        { q: 'How long does a card request take?', a: 'Card requests are typically reviewed within 1-2 business days. You\'ll receive a notification once a decision is made.' },
        { q: 'Can I withdraw my Fixed Deposit early?', a: 'Yes — go to Fixed Deposits and click "Close FD". A 1% penalty on interest earned is applied for premature closure.' },
        { q: 'What documents are needed for a loan?', a: 'Loan eligibility is assessed based on your account history. Apply through the Loans section — no document upload needed for the initial application.' },
      ],
    }
  },
  computed: {
    userInitial() {
      const u = this.$store?.getters?.getUser?.username || 'U'
      return u[0].toUpperCase()
    },
    filteredTickets() {
      if (!this.listFilter) return this.tickets
      return this.tickets.filter(t => t.status === this.listFilter)
    },
  },
  created() {
    this.fetchTickets()
  },
  methods: {
    headers() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}` }
    },
    async fetchTickets() {
      this.loading = true
      try {
        const res = await axios.get('http://127.0.0.1:8000/accounts/support/', { headers: this.headers() })
        this.tickets = res.data
      } catch (e) {
        console.error(e)
      } finally {
        this.loading = false
      }
    },
    async openTicket(id) {
      try {
        const res = await axios.get(`http://127.0.0.1:8000/accounts/support/${id}/`, { headers: this.headers() })
        this.activeTicket = res.data
        this.replyBody = ''
        this.replyError = ''
        await this.$nextTick()
        this.scrollThread()
      } catch (e) {
        console.error(e)
      }
    },
    scrollThread() {
      const el = this.$refs.thread
      if (el) el.scrollTop = el.scrollHeight
    },
    async sendReply() {
      if (!this.replyBody.trim()) return
      this.replying = true
      this.replyError = ''
      try {
        const res = await axios.post(
          `http://127.0.0.1:8000/accounts/support/${this.activeTicket.id}/`,
          { body: this.replyBody },
          { headers: this.headers() }
        )
        this.activeTicket = res.data
        this.replyBody = ''
        await this.$nextTick()
        this.scrollThread()
      } catch (e) {
        this.replyError = e.response?.data?.error || 'Failed to send reply.'
      } finally {
        this.replying = false
      }
    },
    async createTicket() {
      this.createError = ''
      if (!this.form.subject.trim()) { this.createError = 'Subject is required.'; return }
      if (!this.form.body.trim())    { this.createError = 'Please describe your issue.'; return }
      this.creating = true
      try {
        const res = await axios.post('http://127.0.0.1:8000/accounts/support/', this.form, { headers: this.headers() })
        this.tickets.unshift({
          id: res.data.id,
          ticket_number: res.data.ticket_number,
          subject: res.data.subject,
          category: res.data.category,
          status: res.data.status,
          priority: res.data.priority,
          created_at: res.data.created_at,
          message_count: 1,
        })
        this.form = { category: 'other', subject: '', body: '' }
        this.activeTicket = res.data
        await this.$nextTick()
        this.scrollThread()
      } catch (e) {
        this.createError = e.response?.data?.error || 'Failed to create ticket.'
      } finally {
        this.creating = false
      }
    },
    statusLabel(s) {
      return { open: 'Open', in_progress: 'In Progress', resolved: 'Resolved', closed: 'Closed' }[s] || s
    },
    categoryLabel(c) {
      return {
        account: 'Account', transaction: 'Transaction', card: 'Card',
        loan: 'Loan', fd: 'Fixed Deposit', technical: 'Technical', other: 'Other',
      }[c] || c
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
.support-page { display: flex; flex-direction: column; gap: 0; }

/* ── Ticket detail ── */
.detail-header {
  display: flex; align-items: center; gap: 16px; flex-wrap: wrap;
  margin-bottom: 12px;
}
.back-btn {
  display: flex; align-items: center; gap: 6px;
  padding: 8px 14px; border-radius: var(--radius-sm); border: 1px solid var(--border);
  background: var(--bg); font-size: 13px; font-weight: 600; cursor: pointer; color: var(--text);
  transition: all .18s;
}
.back-btn:hover { background: #fff; border-color: var(--blue); color: var(--blue); }
.back-btn svg { width: 16px; height: 16px; }
.detail-meta { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.ticket-num { font-size: 13px; font-weight: 700; color: var(--muted); font-family: monospace; letter-spacing: .5px; }
.detail-subject { font-size: 20px; font-weight: 700; color: var(--text); margin-bottom: 4px; }
.detail-opened { font-size: 12px; color: var(--muted); margin-bottom: 20px; }
.cat-chip { padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; background: #f1f5f9; color: #475569; }

/* Thread */
.thread {
  display: flex; flex-direction: column; gap: 16px;
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 20px; max-height: 420px; overflow-y: auto; margin-bottom: 16px;
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

.msg-bubble { max-width: 75%; }
.message.staff .msg-bubble { display: flex; flex-direction: column; align-items: flex-end; }

.msg-sender { font-size: 11px; font-weight: 700; color: var(--muted); margin-bottom: 4px; }
.msg-body {
  font-size: 14px; line-height: 1.6; padding: 12px 16px;
  border-radius: 14px; white-space: pre-wrap; word-break: break-word;
}
.message.user  .msg-body { background: #f1f5f9; color: var(--text); border-bottom-left-radius: 4px; }
.message.staff .msg-body { background: var(--blue); color: #fff; border-bottom-right-radius: 4px; }
.msg-time { font-size: 11px; color: #94a3b8; margin-top: 4px; }
.message.staff .msg-time { text-align: right; }

/* Reply */
.reply-box { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 16px; }
.reply-box textarea {
  width: 100%; resize: vertical; border: 1px solid var(--border); border-radius: var(--radius-sm);
  padding: 12px; font-size: 14px; font-family: inherit; color: var(--text); background: var(--bg);
  min-height: 80px;
}
.reply-box textarea:focus { outline: none; border-color: var(--blue); }
.reply-actions { display: flex; align-items: center; justify-content: space-between; margin-top: 10px; }
.reply-hint { font-size: 12px; color: var(--muted); }
.send-btn {
  display: flex; align-items: center; gap: 7px;
  padding: 10px 22px; border-radius: var(--radius-sm); border: none;
  background: var(--blue); color: #fff; font-size: 14px; font-weight: 600; cursor: pointer;
  transition: all .18s;
}
.send-btn svg { width: 15px; height: 15px; }
.send-btn:hover:not(:disabled) { background: #1d4ed8; }
.send-btn:disabled { opacity: .5; cursor: not-allowed; }

.ticket-closed-notice {
  display: flex; align-items: center; gap: 10px;
  padding: 14px 18px; border-radius: var(--radius-sm);
  background: #f0fdf4; border: 1px solid #bbf7d0; color: #15803d; font-size: 14px; font-weight: 500;
}
.ticket-closed-notice svg { width: 18px; height: 18px; flex-shrink: 0; }

/* ── List view ── */
.list-grid {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 20px;
  align-items: start;
}
@media (max-width: 900px) { .list-grid { grid-template-columns: 1fr; } }

.panel {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  overflow: hidden;
}
.panel-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 20px; border-bottom: 1px solid var(--border);
}
.panel-header h2 { font-size: 16px; font-weight: 700; color: var(--text); }
.status-filter select {
  padding: 6px 10px; border: 1px solid var(--border); border-radius: 6px;
  font-size: 13px; background: var(--bg); color: var(--text);
}

.state-box {
  display: flex; flex-direction: column; align-items: center; gap: 10px;
  padding: 48px 20px; color: var(--muted); font-size: 14px; text-align: center;
}
.state-box svg { width: 44px; height: 44px; opacity: .35; }
.spinner {
  width: 32px; height: 32px; border: 3px solid var(--border);
  border-top-color: var(--blue); border-radius: 50%; animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Ticket rows */
.ticket-list { display: flex; flex-direction: column; }
.ticket-row {
  display: flex; align-items: center; gap: 12px; justify-content: space-between;
  padding: 14px 20px; border-bottom: 1px solid #f1f5f9; cursor: pointer; transition: background .15s;
}
.ticket-row:last-child { border-bottom: none; }
.ticket-row:hover { background: #f8fafc; }
.ticket-row-left { display: flex; flex-direction: column; gap: 3px; flex: 1; min-width: 0; }
.ticket-row-num  { font-size: 11px; font-weight: 700; color: var(--muted); font-family: monospace; letter-spacing: .5px; }
.ticket-row-subject { font-size: 14px; font-weight: 600; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.ticket-row-cat { font-size: 11px; color: var(--muted); }
.ticket-row-right { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
.ticket-date { font-size: 11px; color: var(--muted); }
.msg-count {
  display: flex; align-items: center; gap: 4px;
  font-size: 12px; color: var(--muted);
}
.msg-count svg { width: 13px; height: 13px; }
.chevron { width: 16px; height: 16px; color: var(--muted); }

/* Status & priority badges */
.status-badge {
  padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; white-space: nowrap;
}
.status-badge.sm { font-size: 11px; padding: 3px 8px; }
.status-badge.open        { background: #dbeafe; color: #1d4ed8; }
.status-badge.in_progress { background: #fef3c7; color: #b45309; }
.status-badge.resolved    { background: #d1fae5; color: #065f46; }
.status-badge.closed      { background: #f1f5f9; color: #64748b; }

.priority-badge {
  padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600;
}
.priority-badge.low    { background: #f0fdf4; color: #15803d; }
.priority-badge.medium { background: #eff6ff; color: #1d4ed8; }
.priority-badge.high   { background: #fef3c7; color: #b45309; }
.priority-badge.urgent { background: #fee2e2; color: #dc2626; }

/* New ticket form */
.new-ticket-panel { }
.ticket-form { padding: 20px; display: flex; flex-direction: column; gap: 14px; }
.form-group { display: flex; flex-direction: column; gap: 6px; position: relative; }
.form-group label { font-size: 12px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: .5px; }
.form-group input, .form-group select, .form-group textarea {
  padding: 10px 12px; border: 1px solid var(--border); border-radius: var(--radius-sm);
  font-size: 14px; font-family: inherit; color: var(--text); background: var(--bg);
}
.form-group textarea { resize: vertical; min-height: 100px; }
.form-group input:focus, .form-group select:focus, .form-group textarea:focus {
  outline: none; border-color: var(--blue);
}
.char-count { position: absolute; right: 10px; bottom: 10px; font-size: 11px; color: var(--muted); }
.form-error { font-size: 13px; color: var(--danger); font-weight: 500; }
.submit-btn {
  display: flex; align-items: center; justify-content: center; gap: 8px;
  padding: 12px; border-radius: var(--radius-sm); border: none;
  background: var(--blue); color: #fff; font-size: 15px; font-weight: 700; cursor: pointer;
  transition: all .18s;
}
.submit-btn svg { width: 17px; height: 17px; }
.submit-btn:hover:not(:disabled) { background: #1d4ed8; }
.submit-btn:disabled { opacity: .55; cursor: not-allowed; }

/* FAQ */
.faq-section { padding: 0 20px 20px; border-top: 1px solid var(--border); margin-top: 4px; }
.faq-section h3 { font-size: 14px; font-weight: 700; color: var(--text); padding: 16px 0 10px; }
.faq-item { border-bottom: 1px solid #f1f5f9; }
.faq-q {
  display: flex; align-items: center; justify-content: space-between; width: 100%;
  padding: 12px 0; border: none; background: none; font-size: 13px; font-weight: 600;
  color: var(--text); cursor: pointer; text-align: left; gap: 8px;
}
.faq-q svg { width: 16px; height: 16px; flex-shrink: 0; transition: transform .2s; }
.faq-a {
  font-size: 13px; color: var(--muted); line-height: 1.6; padding: 0 0 12px;
}
</style>
