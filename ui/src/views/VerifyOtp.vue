<template>
  <div class="otp-page">
    <div class="otp-card">
      <div class="card-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
      </div>
      <h2 class="title">Check your email</h2>
      <p class="subtitle">We've sent a 6-digit verification code to<br><strong>{{ email }}</strong></p>

      <form @submit.prevent="verifyOTP" class="form">
        <div class="field">
          <label>Email Address</label>
          <input v-model="email" type="email" placeholder="your@email.com" required />
        </div>
        <div class="field">
          <label>OTP Code</label>
          <input v-model="otp" type="text" placeholder="Enter 6-digit OTP" maxlength="6" required class="otp-input" />
        </div>

        <div v-if="error" class="alert-error">{{ error }}</div>
        <div v-if="success" class="alert-success">{{ success }}</div>

        <button type="submit" class="btn-primary" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          {{ loading ? 'Verifying…' : 'Verify OTP' }}
        </button>
      </form>

      <p class="footer-text">Didn't receive the code? Check your spam folder or <RouterLink to="/Register">go back</RouterLink>.</p>
    </div>
  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

export default {
  data() {
    return { email: this.$route.query.email || '', otp: '', error: '', success: '', loading: false };
  },
  methods: {
    async verifyOTP() {
      this.error = ''; this.success = '';
      this.loading = true;
      try {
        await apiClient.post('/accounts/verify_otp/', { email: this.email, otp: this.otp });
        this.success = 'Email verified! Redirecting to login…';
        setTimeout(() => this.$router.push('/Login'), 1400);
      } catch (err) {
        this.error = err.response?.data?.error || 'Invalid or expired OTP.';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.otp-page {
  min-height: 100vh; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, #0f2044 0%, #1e3a6e 100%);
  padding: 24px;
}
.otp-card {
  background: #fff; border-radius: 20px; padding: 48px 40px;
  width: 100%; max-width: 420px; text-align: center;
  box-shadow: 0 24px 64px rgba(15,32,68,.25);
}
.card-icon {
  width: 64px; height: 64px; background: #eff6ff; border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 24px; color: #2563eb;
}
.card-icon svg { width: 30px; height: 30px; }
.title { font-size: 24px; font-weight: 800; color: #1e293b; margin-bottom: 10px; }
.subtitle { color: #64748b; font-size: 14px; line-height: 1.6; margin-bottom: 32px; }
.subtitle strong { color: #1e293b; }

.form { display: flex; flex-direction: column; gap: 18px; text-align: left; }
.field { display: flex; flex-direction: column; gap: 5px; }
.field label { font-size: 13px; font-weight: 600; color: #1e293b; }
.field input {
  width: 100%; padding: 12px 14px;
  border: 1.5px solid #e2e8f0; border-radius: 8px;
  font-size: 14px; color: #1e293b; background: #f8fafc;
  outline: none; transition: border-color .18s, box-shadow .18s;
}
.field input:focus { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,.1); background: #fff; }
.otp-input { font-size: 22px; letter-spacing: 8px; text-align: center; font-weight: 700; }

.alert-error { padding: 11px 14px; border-radius: 8px; font-size: 13px; background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
.alert-success { padding: 11px 14px; border-radius: 8px; font-size: 13px; background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }

.btn-primary {
  width: 100%; padding: 13px; background: #2563eb; color: #fff;
  border: none; border-radius: 8px; font-size: 15px; font-weight: 600;
  cursor: pointer; transition: background .18s; display: flex; align-items: center; justify-content: center; gap: 8px;
}
.btn-primary:hover:not(:disabled) { background: #1d4ed8; }
.btn-primary:disabled { opacity: .6; cursor: not-allowed; }
.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,.3); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.footer-text { margin-top: 20px; font-size: 13px; color: #64748b; }
.footer-text a { color: #2563eb; font-weight: 600; }
</style>
