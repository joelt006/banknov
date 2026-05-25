<template>
  <div class="auth-page">
    <div class="left-panel">
      <div class="left-content">
        <div class="brand">
          <div class="brand-icon">MB</div>
          <span>MyBank</span>
        </div>
        <h1 class="tagline">Banking made<br><span>simple &amp; secure</span></h1>
        <p class="sub">Access your accounts, transfer funds, and manage your finances — all in one place.</p>
        <div class="features">
          <div class="feature"><span class="dot"></span>256-bit encrypted transactions</div>
          <div class="feature"><span class="dot"></span>Real-time balance updates</div>
          <div class="feature"><span class="dot"></span>24/7 account access</div>
        </div>
      </div>
    </div>

    <div class="right-panel">
      <div class="form-card">

        <!-- Step 1: credentials -->
        <template v-if="step === 1">
          <h2 class="form-title">Welcome back</h2>
          <p class="form-subtitle">Sign in to your account</p>
          <form @submit.prevent="handleLogin" class="form">
            <div class="field">
              <label>Username</label>
              <input v-model="username" type="text" placeholder="Enter your username" required autocomplete="username" />
            </div>
            <div class="field">
              <label>Password</label>
              <div class="input-wrap">
                <input v-model="password" :type="showPass ? 'text' : 'password'" placeholder="Enter your password" required />
                <button type="button" class="eye-btn" @click="showPass = !showPass">
                  <svg v-if="!showPass" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                </button>
              </div>
            </div>

            <!-- CAPTCHA -->
            <div class="field captcha-field">
              <label>Security Check</label>
              <div class="captcha-row">
                <div class="captcha-question">{{ captchaQuestion }}</div>
                <button type="button" class="captcha-refresh" @click="loadCaptcha" title="Refresh">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>
                </button>
              </div>
              <input v-model="captchaAnswer" type="number" placeholder="Your answer" required />
            </div>

            <div v-if="error" class="alert-error">{{ error }}</div>

            <button type="submit" class="btn-primary" :disabled="loading">
              <span v-if="loading" class="spinner"></span>
              {{ loading ? 'Signing in…' : 'Sign In' }}
            </button>
          </form>
          <p class="form-footer"><RouterLink to="/ForgotPassword">Forgot password?</RouterLink></p>
          <p class="form-footer">Don't have an account? <RouterLink to="/Register">Register here</RouterLink></p>
          <p class="form-footer">New to MyBank? <RouterLink to="/CreateAccountoption">Open an account</RouterLink></p>
        </template>

        <!-- Step 2: OTP -->
        <template v-else>
          <div class="otp-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          </div>
          <h2 class="form-title">Check your email</h2>
          <p class="form-subtitle">We sent a 6-digit code to your registered email. It expires in 5 minutes.</p>
          <form @submit.prevent="verifyOtp" class="form">
            <div class="field">
              <label>OTP Code</label>
              <input v-model="otp" type="text" maxlength="6" placeholder="Enter 6-digit code" required class="otp-input" />
            </div>
            <div v-if="error" class="alert-error">{{ error }}</div>
            <button type="submit" class="btn-primary" :disabled="loading">
              <span v-if="loading" class="spinner"></span>
              {{ loading ? 'Verifying…' : 'Verify & Sign In' }}
            </button>
          </form>
          <p class="form-footer" style="margin-top:16px">
            <button class="link-btn" @click="step = 1; otp = ''; error = ''">← Back to login</button>
          </p>
        </template>

      </div>
    </div>
  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

export default {
  data() {
    return {
      step: 1,
      username: '', password: '', showPass: false,
      captchaId: '', captchaQuestion: '', captchaAnswer: '',
      otp: '', tempToken: '',
      error: '', loading: false,
    };
  },
  mounted() {
    this.loadCaptcha();
  },
  methods: {
    async loadCaptcha() {
      try {
        const res = await apiClient.get('/accounts/captcha/');
        this.captchaId = res.data.captcha_id;
        this.captchaQuestion = res.data.question;
        this.captchaAnswer = '';
      } catch { /* silent */ }
    },
    async handleLogin() {
      this.error = '';
      this.loading = true;
      try {
        const res = await apiClient.post('/accounts/login/', {
          username: this.username,
          password: this.password,
          captcha_id: this.captchaId,
          captcha_answer: this.captchaAnswer,
        });
        if (res.data.requires_otp) {
          this.tempToken = res.data.temp_token;
          this.step = 2;
        }
      } catch (err) {
        this.error = err.response?.data?.error || 'Login failed. Please try again.';
        this.loadCaptcha();
      } finally {
        this.loading = false;
      }
    },
    async verifyOtp() {
      this.error = '';
      this.loading = true;
      try {
        const res = await apiClient.post('/accounts/login/verify-otp/', {
          temp_token: this.tempToken,
          otp: this.otp,
        });
        this.$store.commit('setToken', res.data.token);
        this.$router.push('/Dashboard');
      } catch (err) {
        this.error = err.response?.data?.error || 'Invalid OTP. Please try again.';
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
  background: linear-gradient(145deg, #0f2044 0%, #1e3a6e 60%, #1a3a6e 100%);
  display: flex; align-items: center; justify-content: center;
  padding: 48px; position: relative; overflow: hidden;
}
.left-panel::before {
  content: ''; position: absolute;
  width: 420px; height: 420px;
  background: rgba(37,99,235,.14); border-radius: 50%;
  top: -120px; right: -120px;
}
.left-panel::after {
  content: ''; position: absolute;
  width: 320px; height: 320px;
  background: rgba(245,158,11,.09); border-radius: 50%;
  bottom: -80px; left: -80px;
}
.left-content { position: relative; z-index: 1; max-width: 400px; }

.brand { display: flex; align-items: center; gap: 12px; color: #fff; font-size: 22px; font-weight: 700; margin-bottom: 48px; }
.brand-icon { width: 44px; height: 44px; background: #2563eb; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 800; color: #fff; }
.tagline { font-size: 40px; font-weight: 800; color: #fff; line-height: 1.18; margin-bottom: 18px; }
.tagline span { color: #f59e0b; }
.sub { color: rgba(255,255,255,.65); font-size: 15px; line-height: 1.7; margin-bottom: 36px; }
.features { display: flex; flex-direction: column; gap: 12px; }
.feature { display: flex; align-items: center; gap: 10px; color: rgba(255,255,255,.8); font-size: 14px; }
.dot { width: 8px; height: 8px; background: #f59e0b; border-radius: 50%; flex-shrink: 0; }

.right-panel { width: 480px; display: flex; align-items: center; justify-content: center; padding: 48px 40px; background: #f0f4f8; }
.form-card { width: 100%; max-width: 380px; }
.form-title { font-size: 28px; font-weight: 800; color: #1e293b; margin-bottom: 6px; }
.form-subtitle { color: #64748b; font-size: 14px; margin-bottom: 32px; }

.form { display: flex; flex-direction: column; gap: 20px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 13px; font-weight: 600; color: #1e293b; }
.field input { width: 100%; padding: 12px 14px; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 14px; color: #1e293b; background: #fff; transition: border-color .18s, box-shadow .18s; outline: none; box-sizing: border-box; }
.field input:focus { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,.1); }

.input-wrap { position: relative; }
.input-wrap input { padding-right: 44px; }
.eye-btn { position: absolute; right: 12px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; padding: 0; color: #64748b; }
.eye-btn svg { width: 18px; height: 18px; display: block; }

.captcha-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.captcha-question { flex: 1; padding: 10px 14px; background: #eff6ff; border: 1.5px solid #bfdbfe; border-radius: 8px; font-size: 15px; font-weight: 700; color: #1e3a6e; letter-spacing: 1px; }
.captcha-refresh { background: none; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 8px 10px; cursor: pointer; color: #64748b; display: flex; align-items: center; transition: border-color .18s; }
.captcha-refresh:hover { border-color: #2563eb; color: #2563eb; }
.captcha-refresh svg { width: 16px; height: 16px; }

.otp-icon { width: 64px; height: 64px; background: #eff6ff; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 20px; }
.otp-icon svg { width: 28px; height: 28px; stroke: #2563eb; }
.otp-input { font-size: 22px; font-weight: 700; letter-spacing: 6px; text-align: center; }

.alert-error { padding: 11px 14px; border-radius: 8px; font-size: 13px; font-weight: 500; background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }

.btn-primary { width: 100%; padding: 13px; background: #2563eb; color: #fff; border: none; border-radius: 8px; font-size: 15px; font-weight: 600; cursor: pointer; transition: background .18s; display: flex; align-items: center; justify-content: center; gap: 8px; }
.btn-primary:hover:not(:disabled) { background: #1d4ed8; }
.btn-primary:disabled { opacity: .6; cursor: not-allowed; }

.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,.3); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.form-footer { text-align: center; margin-top: 12px; font-size: 13px; color: #64748b; }
.form-footer a { color: #2563eb; font-weight: 600; }
.link-btn { background: none; border: none; color: #2563eb; font-weight: 600; cursor: pointer; font-size: 13px; padding: 0; }

@media (max-width: 768px) {
  .auth-page { flex-direction: column; }
  .left-panel { padding: 40px 24px; }
  .tagline { font-size: 28px; }
  .right-panel { width: 100%; padding: 32px 20px; }
}
</style>
