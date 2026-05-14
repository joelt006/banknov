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

          <div v-if="error" class="alert-error">{{ error }}</div>

          <button type="submit" class="btn-primary" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            {{ loading ? 'Signing in…' : 'Sign In' }}
          </button>
        </form>

        <p class="form-footer">
          Don't have an account? <RouterLink to="/Register">Register here</RouterLink>
        </p>
        <p class="form-footer" style="margin-top:8px">
          New to MyBank? <RouterLink to="/CreateAccountoption">Open an account</RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

export default {
  data() {
    return { username: '', password: '', error: '', loading: false, showPass: false };
  },
  methods: {
    async handleLogin() {
      this.error = '';
      this.loading = true;
      try {
        const res = await apiClient.post('/accounts/login/', {
          username: this.username,
          password: this.password,
        });
        const token = res.data.token;
        this.$store.commit('setToken', token);
        this.$router.push('/Dashboard');
      } catch (err) {
        this.error = err.response?.data?.error || 'Invalid credentials. Please try again.';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.auth-page { display: flex; min-height: 100vh; }

/* Left */
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
.brand-icon {
  width: 44px; height: 44px; background: #2563eb; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 800; color: #fff;
}
.tagline { font-size: 40px; font-weight: 800; color: #fff; line-height: 1.18; margin-bottom: 18px; }
.tagline span { color: #f59e0b; }
.sub { color: rgba(255,255,255,.65); font-size: 15px; line-height: 1.7; margin-bottom: 36px; }
.features { display: flex; flex-direction: column; gap: 12px; }
.feature { display: flex; align-items: center; gap: 10px; color: rgba(255,255,255,.8); font-size: 14px; }
.dot { width: 8px; height: 8px; background: #f59e0b; border-radius: 50%; flex-shrink: 0; }

/* Right */
.right-panel {
  width: 480px; display: flex; align-items: center; justify-content: center;
  padding: 48px 40px; background: #f0f4f8;
}
.form-card { width: 100%; max-width: 380px; }
.form-title { font-size: 28px; font-weight: 800; color: #1e293b; margin-bottom: 6px; }
.form-subtitle { color: #64748b; font-size: 14px; margin-bottom: 32px; }

.form { display: flex; flex-direction: column; gap: 20px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 13px; font-weight: 600; color: #1e293b; }
.field input {
  width: 100%; padding: 12px 14px;
  border: 1.5px solid #e2e8f0; border-radius: 8px;
  font-size: 14px; color: #1e293b; background: #fff;
  transition: border-color .18s, box-shadow .18s; outline: none;
}
.field input:focus { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,.1); }

.input-wrap { position: relative; }
.input-wrap input { padding-right: 44px; }
.eye-btn {
  position: absolute; right: 12px; top: 50%; transform: translateY(-50%);
  background: none; border: none; cursor: pointer; padding: 0; color: #64748b;
}
.eye-btn svg { width: 18px; height: 18px; display: block; }

.alert-error { padding: 11px 14px; border-radius: 8px; font-size: 13px; font-weight: 500; background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }

.btn-primary {
  width: 100%; padding: 13px; background: #2563eb; color: #fff;
  border: none; border-radius: 8px; font-size: 15px; font-weight: 600;
  cursor: pointer; transition: background .18s; display: flex; align-items: center; justify-content: center; gap: 8px;
}
.btn-primary:hover:not(:disabled) { background: #1d4ed8; }
.btn-primary:disabled { opacity: .6; cursor: not-allowed; }

.spinner {
  width: 16px; height: 16px; border: 2px solid rgba(255,255,255,.3);
  border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.form-footer { text-align: center; margin-top: 20px; font-size: 13px; color: #64748b; }
.form-footer a { color: #2563eb; font-weight: 600; }

@media (max-width: 768px) {
  .auth-page { flex-direction: column; }
  .left-panel { padding: 40px 24px; }
  .tagline { font-size: 28px; }
  .right-panel { width: 100%; padding: 32px 20px; }
}
</style>
