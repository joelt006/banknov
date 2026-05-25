<template>
  <div class="page">

    <!-- Add Beneficiary -->
    <div class="card">
      <div class="card-header">
        <div class="card-icon blue">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><line x1="19" y1="8" x2="19" y2="14"/><line x1="22" y1="11" x2="16" y2="11"/></svg>
        </div>
        <div>
          <h2 class="card-title">Add Beneficiary</h2>
          <p class="card-sub">Save a recipient for quick transfers</p>
        </div>
      </div>
      <form @submit.prevent="addBeneficiary" class="add-form">
        <div class="field">
          <label>Nickname</label>
          <input v-model="form.nickname" type="text" placeholder="e.g. Mom, Office Rent" maxlength="50" required />
        </div>
        <div class="field">
          <label>Account Number</label>
          <input v-model="form.account_number" type="text" placeholder="16-digit account number" maxlength="16" required />
        </div>
        <div v-if="form.error" class="alert-error">{{ form.error }}</div>
        <div v-if="form.success" class="alert-success">{{ form.success }}</div>
        <button type="submit" class="btn-add" :disabled="form.loading">
          <span v-if="form.loading" class="spinner"></span>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          {{ form.loading ? 'Adding…' : 'Add Beneficiary' }}
        </button>
      </form>
    </div>

    <!-- Beneficiary List -->
    <div class="card">
      <div class="card-header">
        <div class="card-icon purple">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        </div>
        <div>
          <h2 class="card-title">Saved Beneficiaries</h2>
          <p class="card-sub">{{ beneficiaries.length }} saved contact{{ beneficiaries.length !== 1 ? 's' : '' }}</p>
        </div>
      </div>

      <div v-if="loading" class="loading-row">
        <span class="spinner dark"></span> Loading…
      </div>
      <div v-else-if="beneficiaries.length === 0" class="empty">
        No beneficiaries saved yet. Add one above to get started.
      </div>
      <div v-else class="bene-list">
        <div v-for="b in beneficiaries" :key="b.id" class="bene-row">
          <div class="bene-avatar">{{ b.nickname[0].toUpperCase() }}</div>
          <div class="bene-info">
            <div class="bene-name">{{ b.nickname }}</div>
            <div class="bene-acct">{{ formatAcct(b.account_number) }}</div>
          </div>
          <div class="bene-actions">
            <RouterLink :to="`/SendMoney?to=${b.account_number}`" class="btn-send">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
              Send
            </RouterLink>
            <button class="btn-del" @click="deleteBeneficiary(b.id)" title="Remove">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/></svg>
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

export default {
  data() {
    return {
      beneficiaries: [],
      loading: true,
      form: { nickname: '', account_number: '', error: '', success: '', loading: false },
    };
  },
  mounted() {
    this.fetchBeneficiaries();
  },
  methods: {
    async fetchBeneficiaries() {
      this.loading = true;
      try {
        const res = await apiClient.get('/transactions/beneficiaries/');
        this.beneficiaries = res.data;
      } catch {
        /* silent */
      } finally {
        this.loading = false;
      }
    },
    async addBeneficiary() {
      this.form.error = '';
      this.form.success = '';
      this.form.loading = true;
      try {
        const res = await apiClient.post('/transactions/beneficiaries/', {
          nickname: this.form.nickname,
          account_number: this.form.account_number,
        });
        this.beneficiaries.push(res.data);
        this.beneficiaries.sort((a, b) => a.nickname.localeCompare(b.nickname));
        this.form.success = `${res.data.nickname} added successfully.`;
        this.form.nickname = '';
        this.form.account_number = '';
      } catch (err) {
        this.form.error = err.response?.data?.error || 'Failed to add beneficiary.';
      } finally {
        this.form.loading = false;
      }
    },
    async deleteBeneficiary(id) {
      if (!confirm('Remove this beneficiary?')) return;
      try {
        await apiClient.delete(`/transactions/beneficiaries/${id}/`);
        this.beneficiaries = this.beneficiaries.filter(b => b.id !== id);
      } catch (err) {
        alert(err.response?.data?.error || 'Failed to remove beneficiary.');
      }
    },
    formatAcct(n) {
      return n.replace(/(.{4})/g, '$1 ').trim();
    },
  },
};
</script>

<style scoped>
.page { max-width: 680px; margin: 0 auto; display: flex; flex-direction: column; gap: 24px; }

.card {
  background: #fff; border-radius: 20px; padding: 28px;
  box-shadow: 0 2px 16px rgba(15,32,68,.08); border: 1.5px solid #e2e8f0;
}

.card-header { display: flex; align-items: center; gap: 14px; margin-bottom: 24px; }
.card-icon { width: 48px; height: 48px; border-radius: 13px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.card-icon svg { width: 22px; height: 22px; }
.card-icon.blue { background: #eff6ff; color: #2563eb; }
.card-icon.purple { background: #f5f3ff; color: #7c3aed; }
.card-title { font-size: 17px; font-weight: 800; color: #1e293b; margin-bottom: 2px; }
.card-sub { font-size: 13px; color: #64748b; }

.add-form { display: flex; flex-direction: column; gap: 16px; }
.field { display: flex; flex-direction: column; gap: 5px; }
.field label { font-size: 12px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: .6px; }
.field input {
  padding: 11px 14px; border: 1.5px solid #e2e8f0; border-radius: 10px;
  font-size: 14px; color: #1e293b; background: #f8fafc; outline: none;
  transition: border-color .18s;
}
.field input:focus { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,.1); background: #fff; }

.alert-error { padding: 10px 14px; border-radius: 8px; font-size: 13px; background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
.alert-success { padding: 10px 14px; border-radius: 8px; font-size: 13px; background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }

.btn-add {
  align-self: flex-start; padding: 11px 22px; background: #2563eb; color: #fff;
  border: none; border-radius: 10px; font-size: 14px; font-weight: 700;
  cursor: pointer; display: flex; align-items: center; gap: 8px; transition: background .18s;
}
.btn-add svg { width: 16px; height: 16px; }
.btn-add:hover:not(:disabled) { background: #1d4ed8; }
.btn-add:disabled { opacity: .6; cursor: not-allowed; }

.loading-row { display: flex; align-items: center; gap: 10px; color: #64748b; font-size: 14px; padding: 16px 0; }
.empty { color: #94a3b8; font-size: 14px; text-align: center; padding: 32px 0; }

.bene-list { display: flex; flex-direction: column; gap: 10px; }
.bene-row {
  display: flex; align-items: center; gap: 14px;
  padding: 14px; border-radius: 12px; background: #f8fafc; border: 1.5px solid #e2e8f0;
  transition: border-color .18s;
}
.bene-row:hover { border-color: #bfdbfe; }

.bene-avatar {
  width: 44px; height: 44px; border-radius: 50%;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 18px; font-weight: 700; flex-shrink: 0;
}
.bene-info { flex: 1; min-width: 0; }
.bene-name { font-size: 15px; font-weight: 700; color: #1e293b; }
.bene-acct { font-size: 12px; color: #64748b; font-family: monospace; margin-top: 2px; letter-spacing: 1px; }

.bene-actions { display: flex; align-items: center; gap: 8px; }
.btn-send {
  display: flex; align-items: center; gap: 6px;
  padding: 7px 14px; background: #eff6ff; color: #2563eb;
  border: 1.5px solid #bfdbfe; border-radius: 8px; font-size: 13px; font-weight: 600;
  cursor: pointer; text-decoration: none; transition: background .18s;
}
.btn-send svg { width: 14px; height: 14px; }
.btn-send:hover { background: #dbeafe; }

.btn-del {
  width: 36px; height: 36px; border-radius: 8px;
  background: #fef2f2; border: 1.5px solid #fecaca; color: #dc2626;
  display: flex; align-items: center; justify-content: center; cursor: pointer; transition: background .18s;
}
.btn-del svg { width: 15px; height: 15px; }
.btn-del:hover { background: #fee2e2; }

.spinner { width: 14px; height: 14px; border: 2px solid rgba(255,255,255,.3); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; display: inline-block; }
.spinner.dark { border-color: rgba(0,0,0,.15); border-top-color: #64748b; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
