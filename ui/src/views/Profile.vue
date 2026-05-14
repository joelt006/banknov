<template>
  <div class="profile-page">

    <!-- Header card -->
    <div class="profile-header">
      <div class="avatar-ring">
        <div class="avatar">{{ initials }}</div>
      </div>
      <div class="header-info">
        <h2 class="name">{{ profile.account_holder_name || '—' }}</h2>
        <p class="acct-no">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
          {{ profile.account_number || '—' }}
        </p>
        <p class="email-line">{{ profile.email || '' }}</p>
      </div>
      <RouterLink to="/EditProfile" class="edit-btn">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
        Edit Profile
      </RouterLink>
    </div>

    <div v-if="error" class="alert-error">{{ error }}</div>

    <!-- Info sections -->
    <div class="sections-grid">

      <div class="info-card">
        <div class="card-header">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          Personal Information
        </div>
        <div class="info-grid">
          <div class="info-item"><span class="info-label">Date of Birth</span><span class="info-value">{{ profile.date_of_birth || '—' }}</span></div>
          <div class="info-item"><span class="info-label">Gender</span><span class="info-value">{{ profile.sex || '—' }}</span></div>
          <div class="info-item"><span class="info-label">Occupation</span><span class="info-value">{{ profile.occupation || '—' }}</span></div>
          <div class="info-item"><span class="info-label">Annual Income</span><span class="info-value">{{ profile.annual_income ? '₹ ' + formatAmount(profile.annual_income) : '—' }}</span></div>
        </div>
      </div>

      <div class="info-card">
        <div class="card-header">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
          Address
        </div>
        <div class="info-grid">
          <div class="info-item full"><span class="info-label">Current Address</span><span class="info-value">{{ profile.current_address || '—' }}</span></div>
          <div class="info-item full"><span class="info-label">Permanent Address</span><span class="info-value">{{ profile.permanent_address || '—' }}</span></div>
          <div class="info-item"><span class="info-label">City</span><span class="info-value">{{ profile.city || '—' }}</span></div>
          <div class="info-item"><span class="info-label">State</span><span class="info-value">{{ profile.state || '—' }}</span></div>
          <div class="info-item"><span class="info-label">Country</span><span class="info-value">{{ profile.country || '—' }}</span></div>
          <div class="info-item"><span class="info-label">Pincode</span><span class="info-value">{{ profile.pincode || '—' }}</span></div>
        </div>
      </div>

      <div class="info-card">
        <div class="card-header">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          Contact
        </div>
        <div class="info-grid">
          <div class="info-item"><span class="info-label">Phone</span><span class="info-value">{{ profile.phone_number || '—' }}</span></div>
          <div class="info-item"><span class="info-label">Email</span><span class="info-value">{{ profile.email || '—' }}</span></div>
        </div>
      </div>

      <div class="info-card">
        <div class="card-header">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          Identification
        </div>
        <div class="info-grid">
          <div class="info-item"><span class="info-label">Aadhar Number</span><span class="info-value masked">{{ maskId(profile.aadhar_number) }}</span></div>
          <div class="info-item"><span class="info-label">PAN Card</span><span class="info-value">{{ profile.pan_card_number || '—' }}</span></div>
          <div class="info-item"><span class="info-label">Voter ID</span><span class="info-value masked">{{ maskId(profile.voter_id_number) }}</span></div>
          <div class="info-item"><span class="info-label">Passport</span><span class="info-value masked">{{ maskId(profile.passport_number) }}</span></div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

export default {
  data() {
    return { profile: {}, error: '' };
  },
  computed: {
    initials() {
      const n = this.profile.account_holder_name || '';
      return n.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase() || 'U';
    },
  },
  async created() {
    try {
      const res = await apiClient.get('/accounts/profile/');
      this.profile = res.data;
    } catch {
      this.error = 'Failed to load profile data.';
    }
  },
  methods: {
    maskId(val) {
      if (!val) return '—';
      const s = String(val);
      return s.slice(0, 2) + '•'.repeat(Math.max(0, s.length - 4)) + s.slice(-2);
    },
    formatAmount(val) {
      return parseFloat(val || 0).toLocaleString('en-IN');
    },
  },
};
</script>

<style scoped>
.profile-page { display: flex; flex-direction: column; gap: 24px; }

.profile-header {
  background: linear-gradient(135deg, #1a2f5e 0%, #2563eb 100%);
  border-radius: 20px; padding: 32px 36px;
  display: flex; align-items: center; gap: 24px;
  color: #fff; box-shadow: 0 8px 32px rgba(37,99,235,.25);
  flex-wrap: wrap;
}
.avatar-ring {
  width: 80px; height: 80px; border-radius: 50%;
  border: 3px solid rgba(255,255,255,.3);
  padding: 3px; flex-shrink: 0;
}
.avatar {
  width: 100%; height: 100%; border-radius: 50%;
  background: rgba(255,255,255,.2);
  display: flex; align-items: center; justify-content: center;
  font-size: 26px; font-weight: 800; color: #fff;
}
.header-info { flex: 1; min-width: 0; }
.name { font-size: 22px; font-weight: 800; margin-bottom: 6px; }
.acct-no {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(255,255,255,.12); border-radius: 40px;
  padding: 5px 14px; font-size: 13px; font-weight: 600; margin-bottom: 6px;
}
.acct-no svg { width: 14px; height: 14px; }
.email-line { font-size: 13px; color: rgba(255,255,255,.7); }

.edit-btn {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(255,255,255,.15); border: 1.5px solid rgba(255,255,255,.25);
  color: #fff; border-radius: 10px; padding: 10px 20px;
  font-size: 13px; font-weight: 600; text-decoration: none;
  transition: background .18s;
}
.edit-btn:hover { background: rgba(255,255,255,.25); }
.edit-btn svg { width: 15px; height: 15px; }

.alert-error { padding: 12px 16px; border-radius: 10px; font-size: 13px; background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }

.sections-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }

.info-card {
  background: #fff; border-radius: 16px; overflow: hidden;
  box-shadow: 0 2px 8px rgba(15,32,68,.06); border: 1.5px solid #e2e8f0;
}
.card-header {
  display: flex; align-items: center; gap: 10px;
  padding: 16px 20px; font-size: 14px; font-weight: 700; color: #1e293b;
  border-bottom: 1px solid #f1f5f9; background: #f8fafc;
}
.card-header svg { width: 18px; height: 18px; color: #2563eb; }

.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0; }
.info-item { padding: 14px 20px; border-bottom: 1px solid #f1f5f9; }
.info-item:nth-last-child(-n+2):not(.full + .full) { border-bottom: none; }
.info-item.full { grid-column: 1 / -1; }

.info-label { display: block; font-size: 11px; text-transform: uppercase; letter-spacing: .6px; color: #94a3b8; margin-bottom: 4px; font-weight: 600; }
.info-value { display: block; font-size: 14px; font-weight: 500; color: #1e293b; word-break: break-word; }
.info-value.masked { font-family: 'Courier New', monospace; letter-spacing: 1px; }

@media (max-width: 900px) {
  .sections-grid { grid-template-columns: 1fr; }
  .profile-header { flex-direction: column; align-items: flex-start; }
}
@media (max-width: 540px) {
  .info-grid { grid-template-columns: 1fr; }
}
</style>
