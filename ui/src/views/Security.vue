<template>
  <div class="page">

    <!-- Change Password -->
    <div class="section-card">
      <div class="section-header">
        <div class="section-icon blue">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
        </div>
        <div><h2 class="section-title">Change Password</h2><p class="section-sub">Update your login password</p></div>
      </div>
      <form @submit.prevent="changePassword" class="form">
        <div class="field">
          <label>Current Password</label>
          <input v-model="pw.current" type="password" placeholder="Enter current password" required />
        </div>
        <div class="field">
          <label>New Password</label>
          <input v-model="pw.new" type="password" placeholder="Min 8 characters" required />
        </div>
        <div class="field">
          <label>Confirm New Password</label>
          <input v-model="pw.confirm" type="password" placeholder="Repeat new password" required />
        </div>
        <div v-if="pw.error" class="alert-error">{{ pw.error }}</div>
        <div v-if="pw.success" class="alert-success">{{ pw.success }}</div>
        <button type="submit" class="btn" :disabled="pw.loading">
          <span v-if="pw.loading" class="spinner"></span>
          {{ pw.loading ? 'Updating…' : 'Update Password' }}
        </button>
      </form>
    </div>

    <!-- Transaction PIN -->
    <div class="section-card">
      <div class="section-header">
        <div class="section-icon amber">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        </div>
        <div>
          <h2 class="section-title">Transaction PIN</h2>
          <p class="section-sub">Required for all money transfers — 4 digits</p>
        </div>
        <span class="pin-badge" :class="hasPin ? 'set' : 'unset'">{{ hasPin ? 'PIN Set' : 'Not Set' }}</span>
      </div>
      <form @submit.prevent="setPin" class="form">
        <div v-if="hasPin" class="field">
          <label>Current PIN</label>
          <input v-model="pin.current" type="password" maxlength="4" placeholder="Current 4-digit PIN" inputmode="numeric" />
        </div>
        <div class="field">
          <label>{{ hasPin ? 'New PIN' : 'Set PIN' }}</label>
          <input v-model="pin.new" type="password" maxlength="4" placeholder="4-digit PIN" required inputmode="numeric" />
        </div>
        <div class="field">
          <label>Confirm PIN</label>
          <input v-model="pin.confirm" type="password" maxlength="4" placeholder="Repeat PIN" required inputmode="numeric" />
        </div>
        <div v-if="pin.error" class="alert-error">{{ pin.error }}</div>
        <div v-if="pin.success" class="alert-success">{{ pin.success }}</div>
        <button type="submit" class="btn amber-btn" :disabled="pin.loading">
          <span v-if="pin.loading" class="spinner"></span>
          {{ pin.loading ? 'Saving…' : (hasPin ? 'Change PIN' : 'Set PIN') }}
        </button>
      </form>
    </div>

    <!-- Active Sessions -->
    <div class="section-card">
      <div class="section-header">
        <div class="section-icon green">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
        </div>
        <div><h2 class="section-title">Active Sessions</h2><p class="section-sub">Devices currently logged into your account</p></div>
      </div>
      <div v-if="sessions.length === 0" class="empty">No active sessions found.</div>
      <div v-else class="sessions-list">
        <div v-for="s in sessions" :key="s.id" class="session-row" :class="{ current: s.is_current }">
          <div class="session-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>
          </div>
          <div class="session-info">
            <div class="session-ip">{{ s.ip_address }} <span v-if="s.is_current" class="current-badge">This device</span></div>
            <div class="session-meta">Last seen: {{ formatDate(s.last_seen) }}</div>
            <div class="session-meta ua">{{ truncateUA(s.user_agent) }}</div>
          </div>
          <button v-if="!s.is_current" class="btn-revoke" @click="revokeSession(s.session_key)">Revoke</button>
        </div>
      </div>
    </div>

    <!-- Login History -->
    <div class="section-card">
      <div class="section-header">
        <div class="section-icon red">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="12 8 12 12 14 14"/><path d="M3.05 11a9 9 0 1 0 .5-4"/><polyline points="3 3 3 7 7 7"/></svg>
        </div>
        <div><h2 class="section-title">Login History</h2><p class="section-sub">Last 20 login attempts to your account</p></div>
      </div>
      <div v-if="history.length === 0" class="empty">No login history found.</div>
      <table v-else class="history-table">
        <thead><tr><th>Date &amp; Time</th><th>IP Address</th><th>Status</th><th>Note</th></tr></thead>
        <tbody>
          <tr v-for="h in history" :key="h.timestamp">
            <td>{{ formatDate(h.timestamp) }}</td>
            <td>{{ h.ip_address }}</td>
            <td><span class="badge" :class="h.success ? 'badge-success' : 'badge-fail'">{{ h.success ? 'Success' : 'Failed' }}</span></td>
            <td class="note">{{ h.failure_reason || '—' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

export default {
  data() {
    return {
      hasPin: false,
      pw: { current: '', new: '', confirm: '', error: '', success: '', loading: false },
      pin: { current: '', new: '', confirm: '', error: '', success: '', loading: false },
      sessions: [],
      history: [],
    };
  },
  mounted() {
    this.fetchAll();
  },
  methods: {
    async fetchAll() {
      const [pinRes, sessRes, histRes] = await Promise.allSettled([
        apiClient.get('/accounts/pin-status/'),
        apiClient.get('/accounts/sessions/'),
        apiClient.get('/accounts/login-history/'),
      ]);
      if (pinRes.status === 'fulfilled') this.hasPin = pinRes.value.data.has_pin;
      if (sessRes.status === 'fulfilled') this.sessions = sessRes.value.data;
      if (histRes.status === 'fulfilled') this.history = histRes.value.data;
    },
    async changePassword() {
      this.pw.error = '';
      this.pw.success = '';
      if (this.pw.new !== this.pw.confirm) { this.pw.error = 'Passwords do not match.'; return; }
      this.pw.loading = true;
      try {
        const res = await apiClient.post('/accounts/change-password/', {
          current_password: this.pw.current,
          new_password: this.pw.new,
        });
        this.pw.success = res.data.message;
        this.pw.current = '';
        this.pw.new = '';
        this.pw.confirm = '';
      } catch (err) {
        this.pw.error = err.response?.data?.error || 'Failed to change password.';
      } finally {
        this.pw.loading = false;
      }
    },
    async setPin() {
      this.pin.error = '';
      this.pin.success = '';
      if (this.pin.new !== this.pin.confirm) { this.pin.error = 'PINs do not match.'; return; }
      if (!/^\d{4}$/.test(this.pin.new)) { this.pin.error = 'PIN must be exactly 4 digits.'; return; }
      this.pin.loading = true;
      try {
        const res = await apiClient.post('/accounts/set-pin/', {
          current_pin: this.pin.current,
          new_pin: this.pin.new,
        });
        this.pin.success = res.data.message;
        this.pin.current = '';
        this.pin.new = '';
        this.pin.confirm = '';
        this.hasPin = true;
      } catch (err) {
        this.pin.error = err.response?.data?.error || 'Failed to set PIN.';
      } finally {
        this.pin.loading = false;
      }
    },
    async revokeSession(sessionKey) {
      try {
        await apiClient.delete(`/accounts/sessions/${sessionKey}/`);
        this.sessions = this.sessions.filter(s => s.session_key !== sessionKey);
      } catch (err) {
        alert(err.response?.data?.error || 'Failed to revoke session.');
      }
    },
    formatDate(iso) {
      return new Date(iso).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' });
    },
    truncateUA(ua) {
      return ua ? ua.substring(0, 60) + (ua.length > 60 ? '…' : '') : 'Unknown device';
    },
  },
};
</script>

<style scoped>
.page { max-width: 760px; margin: 0 auto; display: flex; flex-direction: column; gap: 24px; }

.section-card { background: #fff; border-radius: 16px; padding: 28px; box-shadow: 0 2px 12px rgba(15,32,68,.07); border: 1.5px solid #e2e8f0; }
.section-header { display: flex; align-items: center; gap: 14px; margin-bottom: 24px; }
.section-icon { width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.section-icon svg { width: 20px; height: 20px; }
.section-icon.blue { background: #eff6ff; color: #2563eb; }
.section-icon.amber { background: #fffbeb; color: #d97706; }
.section-icon.green { background: #f0fdf4; color: #16a34a; }
.section-icon.red { background: #fef2f2; color: #dc2626; }
.section-title { font-size: 16px; font-weight: 700; color: #1e293b; margin-bottom: 2px; }
.section-sub { font-size: 13px; color: #64748b; }

.pin-badge { margin-left: auto; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; }
.pin-badge.set { background: #dcfce7; color: #16a34a; }
.pin-badge.unset { background: #fef2f2; color: #dc2626; }

.form { display: flex; flex-direction: column; gap: 16px; }
.field { display: flex; flex-direction: column; gap: 5px; }
.field label { font-size: 12px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: .5px; }
.field input { padding: 11px 14px; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 14px; color: #1e293b; background: #f8fafc; outline: none; transition: border-color .18s; }
.field input:focus { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,.1); background: #fff; }

.alert-error { padding: 10px 14px; border-radius: 8px; font-size: 13px; background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
.alert-success { padding: 10px 14px; border-radius: 8px; font-size: 13px; background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }

.btn { padding: 11px 24px; background: #2563eb; color: #fff; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; transition: background .18s; display: inline-flex; align-items: center; gap: 8px; align-self: flex-start; }
.btn:hover:not(:disabled) { background: #1d4ed8; }
.btn:disabled { opacity: .6; cursor: not-allowed; }
.amber-btn { background: #d97706; }
.amber-btn:hover:not(:disabled) { background: #b45309; }

.spinner { width: 14px; height: 14px; border: 2px solid rgba(255,255,255,.3); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.empty { color: #94a3b8; font-size: 14px; text-align: center; padding: 24px 0; }

.sessions-list { display: flex; flex-direction: column; gap: 10px; }
.session-row { display: flex; align-items: center; gap: 14px; padding: 14px; border-radius: 10px; background: #f8fafc; border: 1.5px solid #e2e8f0; }
.session-row.current { border-color: #bfdbfe; background: #eff6ff; }
.session-icon { width: 36px; height: 36px; border-radius: 8px; background: #fff; border: 1.5px solid #e2e8f0; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.session-icon svg { width: 18px; height: 18px; stroke: #64748b; }
.session-info { flex: 1; min-width: 0; }
.session-ip { font-size: 14px; font-weight: 600; color: #1e293b; display: flex; align-items: center; gap: 8px; }
.current-badge { background: #2563eb; color: #fff; border-radius: 4px; font-size: 11px; padding: 1px 7px; font-weight: 700; }
.session-meta { font-size: 12px; color: #64748b; margin-top: 2px; }
.session-meta.ua { font-size: 11px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.btn-revoke { padding: 7px 14px; background: #fef2f2; color: #dc2626; border: 1.5px solid #fecaca; border-radius: 7px; font-size: 13px; font-weight: 600; cursor: pointer; white-space: nowrap; transition: background .18s; flex-shrink: 0; }
.btn-revoke:hover { background: #fee2e2; }

.history-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.history-table th { text-align: left; padding: 10px 12px; font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: .5px; border-bottom: 1.5px solid #e2e8f0; }
.history-table td { padding: 11px 12px; border-bottom: 1px solid #f1f5f9; color: #334155; }
.history-table tr:last-child td { border-bottom: none; }
.badge { padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; }
.badge-success { background: #dcfce7; color: #16a34a; }
.badge-fail { background: #fef2f2; color: #dc2626; }
.note { color: #94a3b8; font-size: 12px; }
</style>
