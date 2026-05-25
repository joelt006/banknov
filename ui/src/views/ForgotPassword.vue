<template>
  <div class="auth-page">
    <div class="left-panel">
      <div class="left-content">
        <div class="brand"><div class="brand-icon">MB</div><span>MyBank</span></div>
        <h1 class="tagline">Reset your<br><span>password</span></h1>
        <p class="sub">We'll send a one-time code to your registered email address to verify your identity.</p>
      </div>
    </div>

    <div class="right-panel">
      <div class="form-card">

        <!-- Step 1: enter email -->
        <template v-if="step === 1">
          <h2 class="form-title">Forgot password?</h2>
          <p class="form-subtitle">Enter your registered email and we'll send you a verification code.</p>
          <form @submit.prevent="sendOtp" class="form">
            <div class="field">
              <label>Email Address</label>
              <input v-model="email" type="email" placeholder="you@example.com" required />
            </div>
            <div v-if="error" class="alert-error">{{ error }}</div>
            <button type="submit" class="btn-primary" :disabled="loading">
              <span v-if="loading" class="spinner"></span>
              {{ loading ? 'Sending…' : 'Send OTP' }}
            </button>
          </form>
          <p class="form-footer"><RouterLink to="/Login">← Back to login</RouterLink></p>
        </template>

        <!-- Step 2: OTP + new password -->
        <template v-else-if="step === 2">
          <div class="otp-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          </div>
          <h2 class="form-title">Check your email</h2>
          <p class="form-subtitle">Enter the 6-digit code sent to <strong>{{ email }}</strong> and choose a new password.</p>
          <form @submit.prevent="resetPassword" class="form">
            <div class="field">
              <label>OTP Code</label>
              <input v-model="otp" type="text" maxlength="6" placeholder="6-digit code" required class="otp-input" />
            </div>
            <div class="field">
              <label>New Password</label>
              <div class="input-wrap">
                <input v-model="newPassword" :type="showPass ? 'text' : 'password'" placeholder="Min 8 characters" required />
                <button type="button" class="eye-btn" @click="showPass = !showPass">
                  <svg v-if="!showPass" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                </button>
              </div>
            </div>
            <div v-if="error" class="alert-error">{{ error }}</div>
            <button type="submit" class="btn-primary" :disabled="loading">
              <span v-if="loading" class="spinner"></span>
              {{ loading ? 'Resetting…' : 'Reset Password' }}
            </button>
          </form>
          <p class="form-footer"><button class="link-btn" @click="step = 1; otp = ''">← Change email</button></p>
        </template>

        <!-- Step 3: success -->
        <template v-else>
          <div class="success-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
          </div>
          <h2 class="form-title">Password reset!</h2>
          <p class="form-subtitle">Your password has been reset successfully. You can now sign in with your new password.</p>
          <RouterLink to="/Login" class="btn-primary" style="text-decoration:none;justify-content:center;display:flex;margin-top:8px">Go to Login</RouterLink>
        </template>

      </div>
    </div>
  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

export default {
  data() {
    return { step: 1, email: '', otp: '', newPassword: '', showPass: false, error: '', loading: false };
  },
  methods: {
    async sendOtp() {
      this.error = '';
      this.loading = true;
      try {
        await apiClient.post('/accounts/forgot-password/', { email: this.email });
        this.step = 2;
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to send OTP. Please try again.';
      } finally {
        this.loading = false;
      }
    },
    async resetPassword() {
      this.error = '';
      this.loading = true;
      try {
        await apiClient.post('/accounts/reset-password/', {
          email: this.email,
          otp: this.otp,
          new_password: this.newPassword,
        });
        this.step = 3;
      } catch (err) {
        this.error = err.response?.data?.error || 'Reset failed. Please try again.';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.auth-page { display: flex; min-height: 100vh; }
.left-panel { flex: 1; background: linear-gradient(145deg, #0f2044 0%, #1e3a6e 60%); display: flex; align-items: center; justify-content: center; padding: 48px; }
.left-content { max-width: 380px; }
.brand { display: flex; align-items: center; gap: 12px; color: #fff; font-size: 22px; font-weight: 700; margin-bottom: 48px; }
.brand-icon { width: 44px; height: 44px; background: #2563eb; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 800; color: #fff; }
.tagline { font-size: 38px; font-weight: 800; color: #fff; line-height: 1.2; margin-bottom: 16px; }
.tagline span { color: #f59e0b; }
.sub { color: rgba(255,255,255,.65); font-size: 15px; line-height: 1.7; }
.right-panel { width: 480px; display: flex; align-items: center; justify-content: center; padding: 48px 40px; background: #f0f4f8; }
.form-card { width: 100%; max-width: 380px; }
.form-title { font-size: 26px; font-weight: 800; color: #1e293b; margin-bottom: 6px; }
.form-subtitle { color: #64748b; font-size: 14px; margin-bottom: 28px; line-height: 1.6; }
.form { display: flex; flex-direction: column; gap: 18px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 13px; font-weight: 600; color: #1e293b; }
.field input { width: 100%; padding: 12px 14px; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 14px; color: #1e293b; background: #fff; outline: none; transition: border-color .18s; box-sizing: border-box; }
.field input:focus { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,.1); }
.input-wrap { position: relative; }
.input-wrap input { padding-right: 44px; }
.eye-btn { position: absolute; right: 12px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; color: #64748b; padding: 0; }
.eye-btn svg { width: 18px; height: 18px; display: block; }
.otp-input { font-size: 22px; font-weight: 700; letter-spacing: 6px; text-align: center; }
.otp-icon { width: 64px; height: 64px; background: #eff6ff; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 20px; }
.otp-icon svg { width: 28px; height: 28px; stroke: #2563eb; }
.success-icon { width: 72px; height: 72px; background: #f0fdf4; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 20px; }
.success-icon svg { width: 32px; height: 32px; stroke: #16a34a; }
.alert-error { padding: 11px 14px; border-radius: 8px; font-size: 13px; background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
.btn-primary { width: 100%; padding: 13px; background: #2563eb; color: #fff; border: none; border-radius: 8px; font-size: 15px; font-weight: 600; cursor: pointer; transition: background .18s; display: flex; align-items: center; justify-content: center; gap: 8px; }
.btn-primary:hover:not(:disabled) { background: #1d4ed8; }
.btn-primary:disabled { opacity: .6; cursor: not-allowed; }
.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,.3); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.form-footer { text-align: center; margin-top: 16px; font-size: 13px; color: #64748b; }
.form-footer a { color: #2563eb; font-weight: 600; }
.link-btn { background: none; border: none; color: #2563eb; font-weight: 600; cursor: pointer; font-size: 13px; padding: 0; }
@media (max-width: 768px) { .auth-page { flex-direction: column; } .left-panel { padding: 32px 20px; } .right-panel { width: 100%; padding: 32px 20px; } }
</style>
