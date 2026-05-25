<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, RouterLink, RouterView, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useStore()

const protectedRoutes = ['Dashboard', 'Profile', 'EditProfile', 'TransactionStatement', 'SendMoney', 'MyCards', 'Security', 'Beneficiaries', 'ScheduledTransfers', 'AccountDetails', 'Loans', 'FixedDeposits', 'Notifications', 'Support']
const adminRoutes = ['AdminDashboard', 'AdminAccounts', 'AdminCardRequests', 'AdminLoans', 'AdminSupport']

const isProtectedRoute = computed(() => protectedRoutes.includes(route.name))
const isAdminRoute = computed(() => adminRoutes.includes(route.name))

const pageTitles = {
  Dashboard: 'Dashboard',
  AccountDetails: 'Account Details',
  SendMoney: 'Send Money',
  TransactionStatement: 'Transaction History',
  Profile: 'My Profile',
  EditProfile: 'Edit Profile',
  MyCards: 'My Cards',
  Security: 'Security Settings',
  Beneficiaries: 'Beneficiaries',
  ScheduledTransfers: 'Scheduled Transfers',
  Loans: 'Loans',
  FixedDeposits: 'Fixed Deposits',
  Notifications: 'Notifications',
  Support: 'Customer Support',
}
const adminPageTitles = {
  AdminDashboard: 'Dashboard',
  AdminAccounts: 'Account Management',
  AdminCardRequests: 'Card Requests',
  AdminLoans: 'Loan Applications',
  AdminSupport: 'Customer Support',
}
const pageTitle = computed(() => pageTitles[route.name] || '')
const adminPageTitle = computed(() => adminPageTitles[route.name] || '')

const username = computed(() => store.getters.getUser?.username || '')
const userInitial = computed(() => (username.value?.[0] || 'U').toUpperCase())
const adminUsername = computed(() => localStorage.getItem('adminUsername') || 'Admin')
const adminInitial = computed(() => (adminUsername.value?.[0] || 'A').toUpperCase())

async function logout() {
  try { await axios.post('http://127.0.0.1:8000/accounts/logout/', {}, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }) } catch { /* silent */ }
  store.dispatch('logout')
  router.push('/Login')
}

function adminLogout() {
  localStorage.removeItem('adminToken')
  localStorage.removeItem('adminUsername')
  router.push('/AdminLogin')
}

const pendingCardCount = ref(0)
const unreadCount = ref(0)
const notifOpen = ref(false)
const recentNotifs = ref([])

async function fetchPendingCount() {
  const token = localStorage.getItem('adminToken')
  if (!token) return
  try {
    const res = await axios.get('http://127.0.0.1:8000/accounts/admin/card-requests/?status=pending', {
      headers: { Authorization: `Bearer ${token}` },
    })
    pendingCardCount.value = res.data.length
  } catch { /* ignore */ }
}

async function fetchUnreadCount() {
  const token = localStorage.getItem('token')
  if (!token) return
  try {
    const res = await axios.get('http://127.0.0.1:8000/accounts/notifications/unread-count/', {
      headers: { Authorization: `Bearer ${token}` },
    })
    unreadCount.value = res.data.count
  } catch { /* ignore */ }
}

async function fetchRecentNotifs() {
  const token = localStorage.getItem('token')
  if (!token) return
  try {
    const res = await axios.get('http://127.0.0.1:8000/accounts/notifications/', {
      headers: { Authorization: `Bearer ${token}` },
    })
    recentNotifs.value = res.data.slice(0, 6)
  } catch { /* ignore */ }
}

async function markAllRead() {
  const token = localStorage.getItem('token')
  if (!token) return
  try {
    await axios.post('http://127.0.0.1:8000/accounts/notifications/', {}, {
      headers: { Authorization: `Bearer ${token}` },
    })
    unreadCount.value = 0
    recentNotifs.value.forEach(n => { n.is_read = true })
  } catch { /* ignore */ }
}

async function markOneRead(notif) {
  if (notif.is_read) return
  const token = localStorage.getItem('token')
  try {
    await axios.patch(`http://127.0.0.1:8000/accounts/notifications/${notif.id}/`, {}, {
      headers: { Authorization: `Bearer ${token}` },
    })
    notif.is_read = true
    if (unreadCount.value > 0) unreadCount.value--
  } catch { /* ignore */ }
}

function openNotifDropdown() {
  notifOpen.value = !notifOpen.value
  if (notifOpen.value) fetchRecentNotifs()
}

function closeNotifDropdown() { notifOpen.value = false }

let unreadTimer = null
watch(isProtectedRoute, (val) => {
  if (val) {
    fetchUnreadCount()
    unreadTimer = setInterval(fetchUnreadCount, 30000)
  } else {
    clearInterval(unreadTimer)
  }
}, { immediate: true })

watch(isAdminRoute, (val) => { if (val) fetchPendingCount() }, { immediate: true })

function timeAgo(iso) {
  const diff = (Date.now() - new Date(iso)) / 1000
  if (diff < 60) return 'just now'
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  return `${Math.floor(diff / 86400)}d ago`
}

// v-click-outside directive
const vClickOutside = {
  mounted(el, binding) {
    el._clickOutside = (e) => { if (!el.contains(e.target)) binding.value(e) }
    document.addEventListener('click', el._clickOutside)
  },
  unmounted(el) { document.removeEventListener('click', el._clickOutside) },
}
</script>

<template>
  <div class="app">
    <!-- ── Customer authenticated shell ── -->
    <div v-if="isProtectedRoute" class="shell">
      <aside class="sidebar">
        <div class="sidebar-brand">
          <div class="brand-icon">MB</div>
          <span class="brand-name">MyBank</span>
        </div>

        <nav class="sidebar-nav">
          <RouterLink to="/Dashboard" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
            Dashboard
          </RouterLink>
          <RouterLink to="/AccountDetails" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
            Account
          </RouterLink>
          <RouterLink to="/SendMoney" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
            Send Money
          </RouterLink>
          <RouterLink to="/Beneficiaries" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><line x1="19" y1="8" x2="19" y2="14"/><line x1="22" y1="11" x2="16" y2="11"/></svg>
            Beneficiaries
          </RouterLink>
          <RouterLink to="/ScheduledTransfers" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            Scheduled
          </RouterLink>
          <RouterLink to="/TransactionStatement" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
            Transactions
          </RouterLink>
          <RouterLink to="/Profile" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            Profile
          </RouterLink>
          <RouterLink to="/EditProfile" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            Edit Profile
          </RouterLink>
          <RouterLink to="/MyCards" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
            My Cards
          </RouterLink>
          <RouterLink to="/Loans" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/><path d="M8 12h8M12 8v8"/></svg>
            Loans
          </RouterLink>
          <RouterLink to="/FixedDeposits" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/><line x1="12" y1="12" x2="12" y2="16"/><line x1="10" y1="14" x2="14" y2="14"/></svg>
            Fixed Deposits
          </RouterLink>
          <RouterLink to="/Security" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            Security
          </RouterLink>
          <RouterLink to="/Notifications" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
            Notifications
            <span v-if="unreadCount > 0" class="nav-badge">{{ unreadCount > 99 ? '99+' : unreadCount }}</span>
          </RouterLink>
          <RouterLink to="/Support" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            Support
          </RouterLink>
        </nav>

        <div class="sidebar-footer">
          <button class="logout-btn" @click="logout">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
            Logout
          </button>
        </div>
      </aside>

      <div class="main-area">
        <header class="topbar">
          <h1 class="page-title">{{ pageTitle }}</h1>
          <div class="topbar-right">
            <!-- Notification bell -->
            <div class="notif-wrap" v-click-outside="closeNotifDropdown">
              <button class="notif-btn" @click="openNotifDropdown" :class="{ active: notifOpen }">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
                <span v-if="unreadCount > 0" class="notif-badge">{{ unreadCount > 99 ? '99+' : unreadCount }}</span>
              </button>
              <div v-if="notifOpen" class="notif-dropdown">
                <div class="notif-dropdown-header">
                  <span>Notifications</span>
                  <button v-if="unreadCount > 0" class="mark-all-btn" @click="markAllRead">Mark all read</button>
                </div>
                <div class="notif-list" v-if="recentNotifs.length > 0">
                  <RouterLink
                    v-for="n in recentNotifs"
                    :key="n.id"
                    :to="n.link || '/Notifications'"
                    class="notif-item"
                    :class="{ unread: !n.is_read }"
                    @click="markOneRead(n); closeNotifDropdown()"
                  >
                    <div class="notif-icon" :class="n.notification_type">
                      <svg v-if="n.notification_type==='transaction'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
                      <svg v-else-if="n.notification_type==='loan'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M8 12h8M12 8v8"/></svg>
                      <svg v-else-if="n.notification_type==='fd'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/></svg>
                      <svg v-else-if="n.notification_type==='card'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
                      <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
                    </div>
                    <div class="notif-content">
                      <div class="notif-title">{{ n.title }}</div>
                      <div class="notif-msg">{{ n.message }}</div>
                      <div class="notif-time">{{ timeAgo(n.created_at) }}</div>
                    </div>
                    <div v-if="!n.is_read" class="unread-dot"></div>
                  </RouterLink>
                </div>
                <div v-else class="notif-empty">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
                  <p>No notifications yet</p>
                </div>
                <RouterLink to="/Notifications" class="notif-see-all" @click="closeNotifDropdown">
                  View all notifications
                </RouterLink>
              </div>
            </div>
            <div class="user-chip">
              <div class="user-avatar">{{ userInitial }}</div>
              <span class="user-name">{{ username }}</span>
            </div>
          </div>
        </header>
        <main class="content">
          <RouterView />
        </main>
      </div>
    </div>

    <!-- ── Admin staff shell ── -->
    <div v-else-if="isAdminRoute" class="shell admin-shell">
      <aside class="sidebar admin-sidebar">
        <div class="sidebar-brand">
          <div class="brand-icon admin-brand-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          </div>
          <div>
            <span class="brand-name">MyBank</span>
            <div class="brand-tag">Staff Portal</div>
          </div>
        </div>

        <nav class="sidebar-nav">
          <RouterLink to="/Admin/Dashboard" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
            Dashboard
          </RouterLink>
          <RouterLink to="/Admin/Accounts" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            Accounts
          </RouterLink>
          <RouterLink to="/Admin/CardRequests" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
            Card Requests
            <span v-if="pendingCardCount > 0" class="nav-badge">{{ pendingCardCount }}</span>
          </RouterLink>
          <RouterLink to="/Admin/Loans" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/><path d="M8 12h8M12 8v8"/></svg>
            Loan Applications
          </RouterLink>
          <RouterLink to="/Admin/Support" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            Support Tickets
          </RouterLink>
        </nav>

        <div class="sidebar-footer">
          <div class="admin-user-info">
            <div class="admin-avatar">{{ adminInitial }}</div>
            <div>
              <div class="admin-uname">{{ adminUsername }}</div>
              <div class="admin-role">Staff Member</div>
            </div>
          </div>
          <button class="logout-btn admin-logout-btn" @click="adminLogout">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
            Sign Out
          </button>
        </div>
      </aside>

      <div class="main-area">
        <header class="topbar admin-topbar">
          <h1 class="page-title">{{ adminPageTitle }}</h1>
          <div class="topbar-right">
            <div class="admin-badge">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              Staff Portal
            </div>
          </div>
        </header>
        <main class="content admin-content">
          <RouterView />
        </main>
      </div>
    </div>

    <!-- ── Public shell ── -->
    <RouterView v-else />
  </div>
</template>

<style>
/* ── Global reset & variables ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --navy:       #0f2044;
  --navy-mid:   #1a2f5e;
  --navy-light: #253d7a;
  --blue:       #2563eb;
  --blue-light: #3b82f6;
  --gold:       #f59e0b;
  --success:    #10b981;
  --danger:     #ef4444;
  --bg:         #f0f4f8;
  --card:       #ffffff;
  --text:       #1e293b;
  --muted:      #64748b;
  --border:     #e2e8f0;
  --radius:     14px;
  --radius-sm:  8px;
  --shadow:     0 2px 12px rgba(15,32,68,.08);
  --shadow-md:  0 4px 24px rgba(15,32,68,.12);
  --shadow-lg:  0 8px 40px rgba(15,32,68,.16);
  --sidebar-w:  256px;
  --topbar-h:   64px;
  --font:       'Segoe UI', system-ui, -apple-system, sans-serif;
}

body {
  font-family: var(--font);
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}

input, select, textarea, button { font-family: inherit; }

a { text-decoration: none; color: inherit; }

.app { min-height: 100vh; }
</style>

<style scoped>
/* ── Shell layout ── */
.shell {
  display: flex;
  min-height: 100vh;
}

/* ── Sidebar ── */
.sidebar {
  width: var(--sidebar-w);
  min-height: 100vh;
  background: var(--navy);
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0; top: 0;
  z-index: 100;
  overflow-y: auto;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 24px 20px;
  border-bottom: 1px solid rgba(255,255,255,.08);
}

.brand-icon {
  width: 40px; height: 40px;
  background: var(--blue);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 14px; color: #fff;
  letter-spacing: .5px;
  flex-shrink: 0;
}

.brand-name {
  font-size: 20px;
  font-weight: 700;
  color: #fff;
  letter-spacing: .3px;
}

.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 14px;
  border-radius: 10px;
  color: rgba(255,255,255,.65);
  font-size: 14px;
  font-weight: 500;
  transition: all .18s;
  cursor: pointer;
}

.nav-item svg {
  width: 18px; height: 18px;
  flex-shrink: 0;
}

.nav-item:hover {
  background: rgba(255,255,255,.08);
  color: #fff;
}

.nav-item.active {
  background: var(--blue);
  color: #fff;
  box-shadow: 0 4px 12px rgba(37,99,235,.35);
}

.sidebar-footer {
  padding: 16px 12px 24px;
  border-top: 1px solid rgba(255,255,255,.08);
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 14px;
  border-radius: 10px;
  border: none;
  background: rgba(239,68,68,.12);
  color: #fca5a5;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all .18s;
}

.logout-btn svg { width: 18px; height: 18px; }

.logout-btn:hover {
  background: rgba(239,68,68,.22);
  color: #fff;
}

/* ── Main area ── */
.main-area {
  margin-left: var(--sidebar-w);
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* ── Topbar ── */
.topbar {
  height: var(--topbar-h);
  background: var(--card);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  position: sticky; top: 0;
  z-index: 50;
  box-shadow: var(--shadow);
}

.page-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text);
}

.topbar-right { display: flex; align-items: center; gap: 16px; }

.user-chip {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 40px;
  padding: 6px 14px 6px 6px;
}

.user-avatar {
  width: 32px; height: 32px;
  background: var(--blue);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  color: #fff;
  font-size: 13px;
  font-weight: 700;
}

.user-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
}

/* ── Content ── */
.content {
  flex: 1;
  padding: 28px;
  overflow-y: auto;
}

/* ── Admin shell overrides ── */
.admin-sidebar {
  background: linear-gradient(180deg, #020617 0%, #0f172a 50%, #1e1b4b 100%);
}

.admin-brand-icon {
  background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
  border-radius: 10px;
  width: 40px; height: 40px;
  display: flex; align-items: center; justify-content: center;
}
.admin-brand-icon svg { width: 20px; height: 20px; color: #fff; }

.brand-tag {
  font-size: 10px;
  color: #6366f1;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.admin-sidebar .nav-item.active {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  box-shadow: 0 4px 12px rgba(99,102,241,.4);
}

.admin-sidebar .nav-item:hover:not(.active) {
  background: rgba(99,102,241,.15);
}

.admin-user-info {
  display: flex; align-items: center; gap: 10px;
  padding: 12px 14px; margin-bottom: 8px;
  background: rgba(255,255,255,.05); border-radius: 10px;
}
.admin-avatar {
  width: 36px; height: 36px; border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 14px; font-weight: 700; flex-shrink: 0;
}
.admin-uname { font-size: 13px; font-weight: 600; color: #fff; }
.admin-role  { font-size: 11px; color: #6366f1; font-weight: 600; text-transform: uppercase; letter-spacing: .5px; }

.admin-logout-btn {
  background: rgba(99,102,241,.15) !important;
  color: #a5b4fc !important;
}
.admin-logout-btn:hover {
  background: rgba(99,102,241,.3) !important;
  color: #fff !important;
}

.admin-topbar {
  border-bottom: 1px solid #e2e8f0;
  background: #fff;
}

.admin-badge {
  display: flex; align-items: center; gap: 6px;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: #fff; border-radius: 8px;
  padding: 6px 14px; font-size: 12px; font-weight: 700;
}
.admin-badge svg { width: 14px; height: 14px; }

.admin-content { background: #f8fafc; }

.nav-badge {
  margin-left: auto;
  background: #ef4444;
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  min-width: 18px;
  height: 18px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 5px;
}

/* ── Notification bell ── */
.notif-wrap {
  position: relative;
}

.notif-btn {
  position: relative;
  width: 40px; height: 40px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: var(--bg);
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all .18s;
  color: var(--muted);
}
.notif-btn svg { width: 20px; height: 20px; }
.notif-btn:hover, .notif-btn.active {
  background: var(--blue);
  border-color: var(--blue);
  color: #fff;
}

.notif-badge {
  position: absolute;
  top: -5px; right: -5px;
  background: #ef4444;
  color: #fff;
  font-size: 10px; font-weight: 800;
  min-width: 18px; height: 18px;
  border-radius: 9px;
  display: flex; align-items: center; justify-content: center;
  padding: 0 4px;
  border: 2px solid #fff;
  pointer-events: none;
}

.notif-dropdown {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  width: 360px;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
  z-index: 200;
  overflow: hidden;
}

.notif-dropdown-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
  font-size: 14px; font-weight: 700; color: var(--text);
}

.mark-all-btn {
  background: none; border: none; cursor: pointer;
  font-size: 12px; font-weight: 600; color: var(--blue);
  padding: 0;
}
.mark-all-btn:hover { text-decoration: underline; }

.notif-list { max-height: 340px; overflow-y: auto; }

.notif-item {
  display: flex; align-items: flex-start; gap: 12px;
  padding: 12px 16px;
  border-bottom: 1px solid #f1f5f9;
  transition: background .15s;
  cursor: pointer;
  text-decoration: none;
  color: inherit;
}
.notif-item:hover { background: #f8fafc; }
.notif-item.unread { background: #eff6ff; }
.notif-item.unread:hover { background: #dbeafe; }

.notif-icon {
  width: 34px; height: 34px; border-radius: 8px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
}
.notif-icon svg { width: 16px; height: 16px; }
.notif-icon.transaction { background: #d1fae5; color: #065f46; }
.notif-icon.loan        { background: #ede9fe; color: #5b21b6; }
.notif-icon.fd          { background: #fef3c7; color: #b45309; }
.notif-icon.card        { background: #dbeafe; color: #1d4ed8; }
.notif-icon.security    { background: #fee2e2; color: #991b1b; }
.notif-icon.system      { background: #f1f5f9; color: #475569; }

.notif-content { flex: 1; min-width: 0; }
.notif-title { font-size: 13px; font-weight: 700; color: var(--text); margin-bottom: 2px; }
.notif-msg   { font-size: 12px; color: var(--muted); line-height: 1.4; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.notif-time  { font-size: 11px; color: #94a3b8; margin-top: 4px; }

.unread-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--blue); flex-shrink: 0; margin-top: 4px;
}

.notif-empty {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 8px; padding: 32px 20px; color: var(--muted); font-size: 13px;
}
.notif-empty svg { width: 36px; height: 36px; opacity: .35; }

.notif-see-all {
  display: block; text-align: center;
  padding: 12px; font-size: 13px; font-weight: 600;
  color: var(--blue); border-top: 1px solid var(--border);
  transition: background .15s;
}
.notif-see-all:hover { background: #eff6ff; }
</style>
