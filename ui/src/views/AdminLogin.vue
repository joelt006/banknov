<template>
  <div class="admin-login-page">
    <div class="login-left">
      <div class="brand">
        <div class="brand-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        </div>
        <div>
          <div class="brand-name">MyBank</div>
          <div class="brand-tag">Staff Portal</div>
        </div>
      </div>

      <div class="login-info">
        <h1>Banking<br><span>Administration</span></h1>
        <p>Secure access for authorised bank staff only. All activity is monitored and logged.</p>

        <div class="feature-list">
          <div class="feature">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
            Account management & oversight
          </div>
          <div class="feature">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/></svg>
            Transaction monitoring
          </div>
          <div class="feature">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
            Customer data access
          </div>
          <div class="feature">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            Balance & financial controls
          </div>
        </div>
      </div>

      <div class="login-footer">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
        256-bit encrypted · Session monitored · Unauthorized access is a criminal offence
      </div>
    </div>

    <div class="login-right">
      <div class="login-card">
        <div class="card-header">
          <div class="shield-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          </div>
          <h2>Staff Sign In</h2>
          <p>Enter your staff credentials to continue</p>
        </div>

        <form @submit.prevent="login" class="login-form">
          <div class="field">
            <label>Staff Username</label>
            <div class="input-wrap">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
              <input v-model="username" type="text" placeholder="Enter staff username" required autocomplete="username" />
            </div>
          </div>

          <div class="field">
            <label>Password</label>
            <div class="input-wrap">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              <input v-model="password" :type="showPass ? 'text' : 'password'" placeholder="Enter password" required autocomplete="current-password" />
              <button type="button" class="eye-btn" @click="showPass = !showPass">
                <svg v-if="!showPass" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
              </button>
            </div>
          </div>

          <div v-if="error" class="error-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            {{ error }}
          </div>

          <button type="submit" class="login-btn" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
            {{ loading ? 'Signing in…' : 'Sign In to Staff Portal' }}
          </button>
        </form>

        <div class="back-link">
          <RouterLink to="/Login">← Back to Customer Login</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdminLogin',
  data() {
    return { username: '', password: '', error: '', loading: false, showPass: false };
  },
  methods: {
    async login() {
      this.error = ''; this.loading = true;
      try {
        const res = await axios.post('http://127.0.0.1:8000/accounts/admin/login/', {
          username: this.username,
          password: this.password,
        });
        localStorage.setItem('adminToken', res.data.token);
        localStorage.setItem('adminUsername', res.data.username);
        this.$router.push('/Admin/Dashboard');
      } catch (err) {
        this.error = err.response?.data?.error || 'Login failed. Please try again.';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.admin-login-page { display: flex; min-height: 100vh; }

/* Left panel */
.login-left {
  flex: 1;
  background: linear-gradient(145deg, #020617 0%, #0f172a 40%, #1e1b4b 100%);
  display: flex; flex-direction: column; justify-content: space-between;
  padding: 48px; position: relative; overflow: hidden;
}
.login-left::before {
  content: ''; position: absolute; width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(99,102,241,.15) 0%, transparent 70%);
  top: -100px; right: -100px; pointer-events: none;
}
.login-left::after {
  content: ''; position: absolute; width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(16,185,129,.08) 0%, transparent 70%);
  bottom: -100px; left: -100px; pointer-events: none;
}

.brand { display: flex; align-items: center; gap: 14px; position: relative; z-index: 1; }
.brand-icon {
  width: 48px; height: 48px; background: linear-gradient(135deg, #6366f1, #4f46e5);
  border-radius: 12px; display: flex; align-items: center; justify-content: center;
}
.brand-icon svg { width: 24px; height: 24px; color: #fff; }
.brand-name { font-size: 20px; font-weight: 800; color: #fff; }
.brand-tag { font-size: 11px; color: #6366f1; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }

.login-info { position: relative; z-index: 1; }
.login-info h1 { font-size: 48px; font-weight: 900; color: #fff; line-height: 1.1; margin-bottom: 16px; }
.login-info h1 span { color: #6366f1; }
.login-info p { color: rgba(255,255,255,.5); font-size: 15px; line-height: 1.7; margin-bottom: 40px; }

.feature-list { display: flex; flex-direction: column; gap: 16px; }
.feature {
  display: flex; align-items: center; gap: 14px;
  color: rgba(255,255,255,.7); font-size: 14px; font-weight: 500;
}
.feature svg { width: 18px; height: 18px; color: #6366f1; flex-shrink: 0; }

.login-footer {
  display: flex; align-items: center; gap: 8px;
  color: rgba(255,255,255,.3); font-size: 11px; position: relative; z-index: 1;
}
.login-footer svg { width: 14px; height: 14px; flex-shrink: 0; }

/* Right panel */
.login-right {
  width: 520px; background: #f8fafc;
  display: flex; align-items: center; justify-content: center; padding: 48px 40px;
}

.login-card { width: 100%; max-width: 420px; }

.card-header { text-align: center; margin-bottom: 36px; }
.shield-icon {
  width: 64px; height: 64px; background: linear-gradient(135deg, #6366f1, #4f46e5);
  border-radius: 18px; display: flex; align-items: center; justify-content: center;
  margin: 0 auto 16px;
}
.shield-icon svg { width: 28px; height: 28px; color: #fff; }
.card-header h2 { font-size: 26px; font-weight: 800; color: #0f172a; margin-bottom: 6px; }
.card-header p { font-size: 14px; color: #64748b; }

.login-form { display: flex; flex-direction: column; gap: 20px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 13px; font-weight: 700; color: #1e293b; letter-spacing: .3px; }

.input-wrap {
  display: flex; align-items: center;
  border: 2px solid #e2e8f0; border-radius: 10px;
  background: #fff; transition: border-color .18s, box-shadow .18s;
  overflow: hidden;
}
.input-wrap:focus-within { border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,.12); }
.input-wrap > svg { width: 18px; height: 18px; color: #94a3b8; margin-left: 14px; flex-shrink: 0; }
.input-wrap input {
  flex: 1; padding: 13px 14px; border: none; outline: none;
  font-size: 14px; color: #1e293b; background: transparent;
}
.eye-btn { background: none; border: none; cursor: pointer; padding: 0 14px; color: #94a3b8; }
.eye-btn svg { width: 18px; height: 18px; display: block; }

.error-box {
  display: flex; align-items: center; gap: 10px;
  background: #fef2f2; border: 1px solid #fecaca; border-radius: 10px;
  padding: 12px 16px; color: #b91c1c; font-size: 13px; font-weight: 500;
}
.error-box svg { width: 18px; height: 18px; flex-shrink: 0; }

.login-btn {
  display: flex; align-items: center; justify-content: center; gap: 10px;
  padding: 14px; background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: #fff; border: none; border-radius: 10px;
  font-size: 15px; font-weight: 700; cursor: pointer;
  transition: opacity .18s, transform .18s;
  box-shadow: 0 4px 16px rgba(99,102,241,.35);
}
.login-btn:hover:not(:disabled) { opacity: .92; transform: translateY(-1px); }
.login-btn:disabled { opacity: .6; cursor: not-allowed; transform: none; }
.login-btn svg { width: 18px; height: 18px; }

.spinner { width: 18px; height: 18px; border: 2px solid rgba(255,255,255,.3); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.back-link { text-align: center; margin-top: 20px; font-size: 13px; }
.back-link a { color: #6366f1; font-weight: 600; }

@media (max-width: 900px) {
  .admin-login-page { flex-direction: column; }
  .login-left { padding: 36px 24px; min-height: 300px; }
  .login-info h1 { font-size: 32px; }
  .login-right { width: 100%; padding: 32px 20px; }
}
</style>
