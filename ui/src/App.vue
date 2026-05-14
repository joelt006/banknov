<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, RouterLink, RouterView, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useStore()

const protectedRoutes = ['Dashboard', 'Profile', 'EditProfile', 'TransactionStatement', 'SendMoney', 'DepositMoney', 'MyCards', 'BankAdmin']
const adminRoutes = ['AdminDashboard', 'AdminAccounts', 'AdminCardRequests']

const isProtectedRoute = computed(() => protectedRoutes.includes(route.name))
const isAdminRoute = computed(() => adminRoutes.includes(route.name))

const pageTitles = {
  Dashboard: 'Dashboard',
  SendMoney: 'Send Money',
  DepositMoney: 'Deposit Money',
  TransactionStatement: 'Transaction History',
  Profile: 'My Profile',
  EditProfile: 'Edit Profile',
  MyCards: 'My Cards',
  BankAdmin: 'Admin Panel',
}
const adminPageTitles = {
  AdminDashboard: 'Dashboard',
  AdminAccounts: 'Account Management',
  AdminCardRequests: 'Card Requests',
}
const pageTitle = computed(() => pageTitles[route.name] || '')
const adminPageTitle = computed(() => adminPageTitles[route.name] || '')

const username = computed(() => store.getters.getUser?.username || '')
const userInitial = computed(() => (username.value?.[0] || 'U').toUpperCase())
const adminUsername = computed(() => localStorage.getItem('adminUsername') || 'Admin')
const adminInitial = computed(() => (adminUsername.value?.[0] || 'A').toUpperCase())

function logout() {
  store.dispatch('logout')
  router.push('/Login')
}

function adminLogout() {
  localStorage.removeItem('adminToken')
  localStorage.removeItem('adminUsername')
  router.push('/AdminLogin')
}

const pendingCardCount = ref(0)

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

watch(isAdminRoute, (val) => { if (val) fetchPendingCount() }, { immediate: true })
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
          <RouterLink to="/SendMoney" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
            Send Money
          </RouterLink>
          <RouterLink to="/DepositMoney" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></svg>
            Deposit
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
          <RouterLink to="/BankAdmin" class="nav-item" active-class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            Admin
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
</style>
