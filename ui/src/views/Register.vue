<template>
  <div class="auth-page">
    <div class="left-panel">
      <div class="left-content">
        <div class="brand">
          <div class="brand-icon">MB</div>
          <span>MyBank</span>
        </div>
        <h1 class="tagline">Join thousands<br><span>of smart bankers</span></h1>
        <p class="sub">Create your net banking account in minutes. Safe, fast, and always available.</p>
        <div class="steps">
          <div class="step"><div class="step-num">1</div><span>Open a bank account first</span></div>
          <div class="step"><div class="step-num">2</div><span>Register with your account number</span></div>
          <div class="step"><div class="step-num">3</div><span>Verify via email OTP</span></div>
        </div>
      </div>
    </div>

    <div class="right-panel">
      <div class="form-card">
        <h2 class="form-title">Create account</h2>
        <p class="form-subtitle">Register for net banking access</p>

        <form @submit.prevent="register" class="form">
          <div class="row-2">
            <div class="field">
              <label>Username</label>
              <input v-model="username" type="text" placeholder="Choose a username" required />
            </div>
            <div class="field">
              <label>Email</label>
              <input v-model="email" type="email" placeholder="your@email.com" required />
            </div>
          </div>
          <div class="field">
            <label>Account Number</label>
            <input v-model="account_number" type="text" placeholder="Your 16-digit bank account number" required maxlength="16" />
            <span class="hint">Your account number is on your bank passbook / welcome letter</span>
          </div>
          <div class="field">
            <label>Password</label>
            <div class="input-wrap">
              <input v-model="password" :type="showPass ? 'text' : 'password'" placeholder="Create a strong password" required />
              <button type="button" class="eye-btn" @click="showPass = !showPass">
                <svg v-if="!showPass" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
              </button>
            </div>
          </div>

          <div v-if="error" class="alert-error">{{ error }}</div>
          <div v-if="success" class="alert-success">{{ success }}</div>

          <button type="submit" class="btn-primary" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            {{ loading ? 'Registering…' : 'Create Account' }}
          </button>
        </form>

        <p class="form-footer">Already registered? <RouterLink to="/Login">Sign in</RouterLink></p>
        <p class="form-footer" style="margin-top:8px">
          No bank account yet? <RouterLink to="/CreateAccountoption">Open one here</RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

export default {
  data() {
    return { username: '', email: '', password: '', account_number: '', error: '', success: '', loading: false, showPass: false };
  },
  methods: {
    async register() {
      this.error = ''; this.success = '';
      this.loading = true;
      try {
        const res = await apiClient.post('/accounts/register/', {
          username: this.username,
          email: this.email,
          password: this.password,
          account_number: this.account_number,
        });
        if (res.data.isOTPSent) {
          this.success = 'OTP sent to your email. Redirecting…';
          setTimeout(() => this.$router.push({ path: '/VerifyOtp', query: { email: this.email } }), 1200);
        }
      } catch (err) {
        this.error = err.response?.data?.error || 'Registration failed. Please check your details.';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.auth-page { display: flex; min-height: 100vh; }

.left-panel {
  flex: 1;
  background: linear-gradient(145deg, #0f2044 0%, #1a3360 60%, #162d5a 100%);
  display: flex; align-items: center; justify-content: center;
  padding: 48px; position: relative; overflow: hidden;
}
.left-panel::before {
  content: ''; position: absolute; width: 380px; height: 380px;
  background: rgba(37,99,235,.14); border-radius: 50%; top: -100px; right: -100px;
}
.left-panel::after {
  content: ''; position: absolute; width: 300px; height: 300px;
  background: rgba(16,185,129,.09); border-radius: 50%; bottom: -80px; left: -80px;
}
.left-content { position: relative; z-index: 1; max-width: 400px; }

.brand { display: flex; align-items: center; gap: 12px; color: #fff; font-size: 22px; font-weight: 700; margin-bottom: 48px; }
.brand-icon { width: 44px; height: 44px; background: #2563eb; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 800; color: #fff; }
.tagline { font-size: 38px; font-weight: 800; color: #fff; line-height: 1.18; margin-bottom: 18px; }
.tagline span { color: #10b981; }
.sub { color: rgba(255,255,255,.65); font-size: 15px; line-height: 1.7; margin-bottom: 36px; }

.steps { display: flex; flex-direction: column; gap: 16px; }
.step { display: flex; align-items: center; gap: 14px; color: rgba(255,255,255,.8); font-size: 14px; }
.step-num {
  width: 28px; height: 28px; background: rgba(255,255,255,.15); border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700; color: #fff; flex-shrink: 0;
}

.right-panel { width: 520px; display: flex; align-items: center; justify-content: center; padding: 48px 40px; background: #f0f4f8; }
.form-card { width: 100%; max-width: 420px; }
.form-title { font-size: 28px; font-weight: 800; color: #1e293b; margin-bottom: 6px; }
.form-subtitle { color: #64748b; font-size: 14px; margin-bottom: 32px; }

.form { display: flex; flex-direction: column; gap: 18px; }
.row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }

.field { display: flex; flex-direction: column; gap: 5px; }
.field label { font-size: 13px; font-weight: 600; color: #1e293b; }
.field input {
  width: 100%; padding: 11px 14px;
  border: 1.5px solid #e2e8f0; border-radius: 8px;
  font-size: 14px; color: #1e293b; background: #fff;
  transition: border-color .18s, box-shadow .18s; outline: none;
}
.field input:focus { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,.1); }
.hint { font-size: 11px; color: #94a3b8; margin-top: 2px; }

.input-wrap { position: relative; }
.input-wrap input { padding-right: 44px; }
.eye-btn { position: absolute; right: 12px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; padding: 0; color: #64748b; }
.eye-btn svg { width: 18px; height: 18px; display: block; }

.alert-error { padding: 11px 14px; border-radius: 8px; font-size: 13px; font-weight: 500; background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
.alert-success { padding: 11px 14px; border-radius: 8px; font-size: 13px; font-weight: 500; background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }

.btn-primary {
  width: 100%; padding: 13px; background: #2563eb; color: #fff;
  border: none; border-radius: 8px; font-size: 15px; font-weight: 600;
  cursor: pointer; transition: background .18s; display: flex; align-items: center; justify-content: center; gap: 8px;
}
.btn-primary:hover:not(:disabled) { background: #1d4ed8; }
.btn-primary:disabled { opacity: .6; cursor: not-allowed; }
.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,.3); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.form-footer { text-align: center; margin-top: 18px; font-size: 13px; color: #64748b; }
.form-footer a { color: #2563eb; font-weight: 600; }

@media (max-width: 768px) {
  .auth-page { flex-direction: column; }
  .left-panel { padding: 36px 24px; }
  .tagline { font-size: 26px; }
  .right-panel { width: 100%; padding: 32px 20px; }
  .row-2 { grid-template-columns: 1fr; }
}
</style>
