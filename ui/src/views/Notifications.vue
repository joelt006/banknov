<template>
  <div class="notifications-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
        <div class="filter-tabs">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            class="tab-btn"
            :class="{ active: activeTab === tab.key }"
            @click="activeTab = tab.key"
          >
            {{ tab.label }}
            <span v-if="tab.key === 'unread' && unreadCount > 0" class="tab-badge">{{ unreadCount }}</span>
          </button>
        </div>
        <div class="type-filter">
          <select v-model="typeFilter">
            <option value="">All Types</option>
            <option value="transaction">Transactions</option>
            <option value="loan">Loans</option>
            <option value="fd">Fixed Deposits</option>
            <option value="card">Cards</option>
            <option value="security">Security</option>
            <option value="system">System</option>
          </select>
        </div>
      </div>
      <div class="header-actions">
        <button class="action-btn" @click="markAllRead" :disabled="unreadCount === 0">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
          Mark all read
        </button>
        <button class="action-btn danger" @click="confirmDeleteAll" :disabled="notifications.length === 0">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6M14 11v6"/></svg>
          Clear all
        </button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="state-box">
      <div class="spinner"></div>
      <p>Loading notifications…</p>
    </div>

    <!-- Empty -->
    <div v-else-if="filtered.length === 0" class="state-box">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
      <p>{{ activeTab === 'unread' ? 'You\'re all caught up!' : 'No notifications yet' }}</p>
    </div>

    <!-- List -->
    <div v-else class="notif-list">
      <div
        v-for="n in filtered"
        :key="n.id"
        class="notif-card"
        :class="{ unread: !n.is_read }"
        @click="handleClick(n)"
      >
        <div class="notif-icon" :class="n.notification_type">
          <svg v-if="n.notification_type==='transaction'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          <svg v-else-if="n.notification_type==='loan'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M8 12h8M12 8v8"/></svg>
          <svg v-else-if="n.notification_type==='fd'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/><line x1="12" y1="12" x2="12" y2="16"/><line x1="10" y1="14" x2="14" y2="14"/></svg>
          <svg v-else-if="n.notification_type==='card'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
          <svg v-else-if="n.notification_type==='security'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
        </div>

        <div class="notif-body">
          <div class="notif-row">
            <div class="notif-title">{{ n.title }}</div>
            <div class="notif-meta">
              <span class="type-chip" :class="n.notification_type">{{ typeLabel(n.notification_type) }}</span>
              <span class="notif-time">{{ timeAgo(n.created_at) }}</span>
            </div>
          </div>
          <p class="notif-message">{{ n.message }}</p>
        </div>

        <div class="notif-actions">
          <div v-if="!n.is_read" class="unread-dot" title="Unread"></div>
          <button class="del-btn" @click.stop="deleteOne(n)" title="Delete">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Confirm delete all -->
    <div v-if="showConfirm" class="modal-overlay" @click.self="showConfirm = false">
      <div class="modal">
        <h3>Clear all notifications?</h3>
        <p>This will permanently delete all {{ notifications.length }} notifications. This cannot be undone.</p>
        <div class="modal-actions">
          <button class="btn-cancel" @click="showConfirm = false">Cancel</button>
          <button class="btn-delete" @click="deleteAll">Delete All</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Notifications',
  data() {
    return {
      notifications: [],
      loading: false,
      activeTab: 'all',
      typeFilter: '',
      showConfirm: false,
      tabs: [
        { key: 'all', label: 'All' },
        { key: 'unread', label: 'Unread' },
      ],
    }
  },
  computed: {
    unreadCount() {
      return this.notifications.filter(n => !n.is_read).length
    },
    filtered() {
      let list = this.notifications
      if (this.activeTab === 'unread') list = list.filter(n => !n.is_read)
      if (this.typeFilter) list = list.filter(n => n.notification_type === this.typeFilter)
      return list
    },
  },
  created() {
    this.fetchNotifications()
  },
  methods: {
    headers() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}` }
    },
    async fetchNotifications() {
      this.loading = true
      try {
        const res = await axios.get('http://127.0.0.1:8000/accounts/notifications/', { headers: this.headers() })
        this.notifications = res.data
      } catch (e) {
        console.error(e)
      } finally {
        this.loading = false
      }
    },
    async handleClick(n) {
      if (!n.is_read) {
        try {
          await axios.patch(`http://127.0.0.1:8000/accounts/notifications/${n.id}/`, {}, { headers: this.headers() })
          n.is_read = true
        } catch { /* ignore */ }
      }
      if (n.link) this.$router.push(n.link)
    },
    async markAllRead() {
      try {
        await axios.post('http://127.0.0.1:8000/accounts/notifications/', {}, { headers: this.headers() })
        this.notifications.forEach(n => { n.is_read = true })
      } catch (e) {
        console.error(e)
      }
    },
    async deleteOne(n) {
      try {
        await axios.delete(`http://127.0.0.1:8000/accounts/notifications/${n.id}/`, { headers: this.headers() })
        this.notifications = this.notifications.filter(x => x.id !== n.id)
      } catch (e) {
        console.error(e)
      }
    },
    confirmDeleteAll() {
      this.showConfirm = true
    },
    async deleteAll() {
      this.showConfirm = false
      await Promise.all(
        this.notifications.map(n =>
          axios.delete(`http://127.0.0.1:8000/accounts/notifications/${n.id}/`, { headers: this.headers() }).catch(() => {})
        )
      )
      this.notifications = []
    },
    typeLabel(t) {
      return { transaction: 'Transaction', loan: 'Loan', fd: 'Fixed Deposit', card: 'Card', security: 'Security', system: 'System' }[t] || t
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
.notifications-page { display: flex; flex-direction: column; gap: 20px; }

/* Header */
.page-header {
  display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 16px 20px;
}

.header-left { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }

.filter-tabs { display: flex; gap: 4px; background: var(--bg); border-radius: var(--radius-sm); padding: 4px; }
.tab-btn {
  display: flex; align-items: center; gap: 6px;
  padding: 7px 16px; border-radius: 6px; border: none; background: none;
  font-size: 13px; font-weight: 600; color: var(--muted); cursor: pointer; transition: all .18s;
}
.tab-btn.active { background: #fff; color: var(--text); box-shadow: 0 1px 4px rgba(0,0,0,.08); }
.tab-badge {
  background: var(--blue); color: #fff; font-size: 10px; font-weight: 700;
  min-width: 18px; height: 18px; border-radius: 9px;
  display: flex; align-items: center; justify-content: center; padding: 0 4px;
}

.type-filter select {
  padding: 8px 12px; border: 1px solid var(--border); border-radius: var(--radius-sm);
  font-size: 13px; background: var(--bg); color: var(--text); min-width: 140px;
}

.header-actions { display: flex; gap: 8px; }
.action-btn {
  display: flex; align-items: center; gap: 7px;
  padding: 8px 16px; border-radius: var(--radius-sm); border: 1px solid var(--border);
  background: var(--bg); font-size: 13px; font-weight: 600; color: var(--text);
  cursor: pointer; transition: all .18s;
}
.action-btn svg { width: 15px; height: 15px; }
.action-btn:hover:not(:disabled) { background: #fff; border-color: var(--blue); color: var(--blue); }
.action-btn.danger:hover:not(:disabled) { border-color: var(--danger); color: var(--danger); }
.action-btn:disabled { opacity: .4; cursor: not-allowed; }

/* State */
.state-box {
  display: flex; flex-direction: column; align-items: center; gap: 12px;
  padding: 60px 20px; color: var(--muted); font-size: 14px; text-align: center;
}
.state-box svg { width: 52px; height: 52px; opacity: .35; }
.spinner {
  width: 36px; height: 36px; border: 3px solid var(--border);
  border-top-color: var(--blue); border-radius: 50%; animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Notification list */
.notif-list { display: flex; flex-direction: column; gap: 8px; }

.notif-card {
  display: flex; align-items: flex-start; gap: 14px;
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 16px 18px; cursor: pointer; transition: all .18s;
  border-left: 3px solid transparent;
}
.notif-card:hover { border-color: var(--border); box-shadow: var(--shadow); }
.notif-card.unread { background: #eff6ff; border-left-color: var(--blue); }
.notif-card.unread:hover { background: #dbeafe; }

/* Icon */
.notif-icon {
  width: 42px; height: 42px; border-radius: 10px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
}
.notif-icon svg { width: 20px; height: 20px; }
.notif-icon.transaction { background: #d1fae5; color: #065f46; }
.notif-icon.loan        { background: #ede9fe; color: #5b21b6; }
.notif-icon.fd          { background: #fef3c7; color: #b45309; }
.notif-icon.card        { background: #dbeafe; color: #1d4ed8; }
.notif-icon.security    { background: #fee2e2; color: #991b1b; }
.notif-icon.system      { background: #f1f5f9; color: #475569; }

/* Body */
.notif-body { flex: 1; min-width: 0; }
.notif-row { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 6px; flex-wrap: wrap; }
.notif-title { font-size: 14px; font-weight: 700; color: var(--text); }
.notif-meta { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }

.type-chip {
  padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: .4px;
}
.type-chip.transaction { background: #d1fae5; color: #065f46; }
.type-chip.loan        { background: #ede9fe; color: #5b21b6; }
.type-chip.fd          { background: #fef3c7; color: #b45309; }
.type-chip.card        { background: #dbeafe; color: #1d4ed8; }
.type-chip.security    { background: #fee2e2; color: #991b1b; }
.type-chip.system      { background: #f1f5f9; color: #475569; }

.notif-time { font-size: 11px; color: #94a3b8; white-space: nowrap; }
.notif-message { font-size: 13px; color: var(--muted); line-height: 1.5; }

/* Right side */
.notif-actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.unread-dot {
  width: 9px; height: 9px; border-radius: 50%; background: var(--blue);
}
.del-btn {
  width: 28px; height: 28px; border-radius: 6px; border: none; background: none;
  cursor: pointer; color: #94a3b8; display: flex; align-items: center; justify-content: center;
  transition: all .15s; opacity: 0;
}
.notif-card:hover .del-btn { opacity: 1; }
.del-btn:hover { background: #fee2e2; color: var(--danger); }
.del-btn svg { width: 15px; height: 15px; }

/* Confirm modal */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,.45); z-index: 500;
  display: flex; align-items: center; justify-content: center;
}
.modal {
  background: #fff; border-radius: var(--radius); padding: 32px; max-width: 400px; width: 90%;
  box-shadow: var(--shadow-lg);
}
.modal h3 { font-size: 18px; font-weight: 700; margin-bottom: 10px; }
.modal p  { font-size: 14px; color: var(--muted); line-height: 1.5; margin-bottom: 24px; }
.modal-actions { display: flex; gap: 10px; justify-content: flex-end; }
.btn-cancel {
  padding: 9px 20px; border-radius: var(--radius-sm); border: 1px solid var(--border);
  background: var(--bg); font-size: 14px; font-weight: 600; cursor: pointer;
}
.btn-delete {
  padding: 9px 20px; border-radius: var(--radius-sm); border: none;
  background: var(--danger); color: #fff; font-size: 14px; font-weight: 600; cursor: pointer;
}
.btn-delete:hover { background: #dc2626; }
</style>
