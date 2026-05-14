<template>
  <div class="edit-page">
    <div class="edit-card">
      <div class="card-top">
        <h2 class="card-title">Update Profile</h2>
        <p class="card-sub">Keep your information up to date</p>
      </div>

      <div v-if="fetchError" class="alert-error">{{ fetchError }}</div>

      <form @submit.prevent="submitForm" class="form">
        <div class="section-label">Personal Details</div>
        <div class="row-2">
          <div class="field">
            <label>Account Holder Name</label>
            <input v-model="form.account_holder_name" type="text" placeholder="Full name" />
          </div>
          <div class="field">
            <label>Date of Birth</label>
            <input v-model="form.date_of_birth" type="date" />
          </div>
          <div class="field">
            <label>Gender</label>
            <select v-model="form.sex">
              <option value="">Select</option>
              <option>Male</option><option>Female</option><option>Other</option>
            </select>
          </div>
          <div class="field">
            <label>Occupation</label>
            <input v-model="form.occupation" type="text" placeholder="Your occupation" />
          </div>
          <div class="field">
            <label>Annual Income (₹)</label>
            <input v-model="form.annual_income" type="number" placeholder="0" min="0" />
          </div>
        </div>

        <div class="section-label">Contact</div>
        <div class="row-2">
          <div class="field">
            <label>Phone Number</label>
            <input v-model="form.phone_number" type="tel" placeholder="+91 XXXXXXXXXX" />
          </div>
          <div class="field">
            <label>Email</label>
            <input v-model="form.email" type="email" placeholder="your@email.com" />
          </div>
        </div>

        <div class="section-label">Address</div>
        <div class="row-2">
          <div class="field full">
            <label>Current Address</label>
            <textarea v-model="form.current_address" rows="2" placeholder="Current address"></textarea>
          </div>
          <div class="field full">
            <label>Permanent Address</label>
            <input v-model="form.permanent_address" type="text" placeholder="Permanent address" />
          </div>
          <div class="field">
            <label>City</label>
            <input v-model="form.city" type="text" />
          </div>
          <div class="field">
            <label>State</label>
            <input v-model="form.state" type="text" />
          </div>
          <div class="field">
            <label>Country</label>
            <input v-model="form.country" type="text" />
          </div>
          <div class="field">
            <label>Pincode</label>
            <input v-model="form.pincode" type="text" maxlength="10" />
          </div>
        </div>

        <div v-if="error" class="alert-error">{{ error }}</div>
        <div v-if="success" class="alert-success">{{ success }}</div>

        <div class="actions">
          <RouterLink to="/Profile" class="btn-secondary">Cancel</RouterLink>
          <button type="submit" class="btn-primary" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            {{ loading ? 'Saving…' : 'Save Changes' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

export default {
  data() {
    return {
      form: {
        account_holder_name: '', date_of_birth: '', sex: '', occupation: '',
        annual_income: '', phone_number: '', email: '',
        current_address: '', permanent_address: '',
        city: '', state: '', country: '', pincode: '',
      },
      error: '', success: '', fetchError: '', loading: false,
    };
  },
  async created() {
    try {
      const res = await apiClient.get('/accounts/edit-profile/');
      const d = res.data.bank_account || res.data;
      Object.keys(this.form).forEach(k => {
        if (d[k] !== undefined) this.form[k] = d[k];
      });
      if (d.Permanent_Address) this.form.permanent_address = d.Permanent_Address;
    } catch {
      this.fetchError = 'Could not load current profile data.';
    }
  },
  methods: {
    async submitForm() {
      this.error = ''; this.success = '';
      this.loading = true;
      try {
        await apiClient.put('/accounts/profile/', this.form);
        this.success = 'Profile updated successfully!';
        setTimeout(() => this.$router.push('/Profile'), 1200);
      } catch (err) {
        this.error = err.response?.data?.error || JSON.stringify(err.response?.data) || 'Update failed.';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.edit-page { max-width: 760px; margin: 0 auto; }

.edit-card {
  background: #fff; border-radius: 20px;
  box-shadow: 0 2px 16px rgba(15,32,68,.08); border: 1.5px solid #e2e8f0;
  overflow: hidden;
}
.card-top {
  padding: 28px 32px; border-bottom: 1px solid #f1f5f9;
  background: linear-gradient(135deg, #f8fafc, #eff6ff);
}
.card-title { font-size: 20px; font-weight: 800; color: #1e293b; margin-bottom: 4px; }
.card-sub { font-size: 13px; color: #64748b; }

.form { padding: 28px 32px; display: flex; flex-direction: column; gap: 10px; }

.section-label {
  font-size: 11px; text-transform: uppercase; letter-spacing: 1px;
  font-weight: 700; color: #2563eb; margin-top: 12px; margin-bottom: 4px;
  padding-bottom: 8px; border-bottom: 1px solid #e2e8f0;
}

.row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.field { display: flex; flex-direction: column; gap: 5px; }
.field.full { grid-column: 1 / -1; }
.field label { font-size: 12px; font-weight: 600; color: #475569; }

.field input, .field select, .field textarea {
  padding: 10px 13px; border: 1.5px solid #e2e8f0; border-radius: 8px;
  font-size: 14px; color: #1e293b; background: #f8fafc;
  outline: none; transition: border-color .18s, box-shadow .18s; resize: none; width: 100%;
}
.field input:focus, .field select:focus, .field textarea:focus {
  border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,.09); background: #fff;
}

.alert-error { padding: 11px 14px; border-radius: 8px; font-size: 13px; background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
.alert-success { padding: 11px 14px; border-radius: 8px; font-size: 13px; background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }

.actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 8px; }

.btn-primary {
  padding: 11px 28px; background: #2563eb; color: #fff;
  border: none; border-radius: 8px; font-size: 14px; font-weight: 600;
  cursor: pointer; transition: background .18s; display: flex; align-items: center; gap: 8px;
}
.btn-primary:hover:not(:disabled) { background: #1d4ed8; }
.btn-primary:disabled { opacity: .6; cursor: not-allowed; }

.btn-secondary {
  padding: 11px 24px; background: #f1f5f9; color: #475569;
  border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 14px; font-weight: 600;
  cursor: pointer; text-decoration: none; display: inline-flex; align-items: center;
  transition: background .18s;
}
.btn-secondary:hover { background: #e2e8f0; }

.spinner { width: 15px; height: 15px; border: 2px solid rgba(255,255,255,.3); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 600px) {
  .row-2 { grid-template-columns: 1fr; }
  .form { padding: 20px; }
  .card-top { padding: 20px; }
}
</style>
