<template>
  <div class="form-page">
    <div class="page-header">
      <RouterLink to="/CreateAccountoption" class="back-link">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
        Back
      </RouterLink>
      <div class="brand"><div class="brand-icon">MB</div><span>MyBank</span></div>
    </div>

    <div class="form-body">
      <div class="form-card">
        <div class="form-card-header">
          <div class="hdr-icon purple"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></div>
          <div>
            <h2 class="form-title">Minor Account</h2>
            <p class="form-sub">For children below 18 years — requires guardian information</p>
          </div>
        </div>

        <form @submit.prevent="submitForm" class="form">

          <div class="section-label">Minor's Information</div>
          <div class="row-2">
            <div class="field full"><label>Minor's Full Name *</label><input v-model="accountHolderName" type="text" placeholder="Child's full name" required /></div>
            <div class="field"><label>Date of Birth *</label><input v-model="dateOfBirth" type="date" required /></div>
            <div class="field"><label>Gender *</label>
              <select v-model="sex" required><option value="">Select</option><option>Male</option><option>Female</option><option>Other</option></select>
            </div>
          </div>

          <div class="section-label">Guardian Information</div>
          <div class="row-2">
            <div class="field full"><label>Guardian's Full Name *</label><input v-model="guardian_name" type="text" placeholder="Parent/Guardian name" required /></div>
          </div>

          <div class="section-label">Address</div>
          <div class="row-2">
            <div class="field full"><label>Current Address *</label><textarea v-model="currentAddress" rows="2" required></textarea></div>
            <div class="field full"><label>Permanent Address *</label><input v-model="permanentAddress" type="text" required /></div>
            <div class="field"><label>Country *</label><input v-model="country" type="text" required /></div>
            <div class="field"><label>State *</label><input v-model="state" type="text" required /></div>
            <div class="field"><label>City *</label><input v-model="city" type="text" required /></div>
            <div class="field"><label>Pincode *</label><input v-model="pincode" type="text" maxlength="10" required /></div>
          </div>

          <div class="section-label">Contact &amp; Income</div>
          <div class="row-2">
            <div class="field"><label>Guardian's Phone *</label><input v-model="phoneNumber" type="tel" required /></div>
            <div class="field"><label>Email</label><input v-model="email" type="email" /></div>
            <div class="field"><label>Occupation</label><input v-model="occupation" type="text" placeholder="Student" /></div>
            <div class="field"><label>Annual Income (₹)</label><input v-model="annualIncome" type="number" min="0" value="0" /></div>
          </div>

          <div class="section-label">Identification (at least one required)</div>
          <div class="row-2">
            <div class="field"><label>Aadhar Number</label><input v-model="aadharNumber" type="text" maxlength="12" /></div>
            <div class="field"><label>PAN Card</label><input v-model="panCardNumber" type="text" /></div>
            <div class="field"><label>Voter ID</label><input v-model="voterIdNumber" type="text" /></div>
            <div class="field"><label>Passport</label><input v-model="passportNumber" type="text" /></div>
          </div>

          <div class="section-label">Photo</div>
          <div class="upload-area" @click="$refs.photoInput.click()">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
            <p>{{ photo ? photo.name : 'Click to upload photo' }}</p>
            <span>JPG, PNG up to 10MB</span>
            <input ref="photoInput" type="file" accept="image/*" @change="onFileChange" hidden />
          </div>

          <div v-if="message" class="alert" :class="message.startsWith('Error') || message.startsWith('Failed') ? 'alert-error' : 'alert-success'">{{ message }}</div>

          <div class="form-actions">
            <RouterLink to="/CreateAccountoption" class="btn-secondary">Cancel</RouterLink>
            <button type="submit" class="btn-primary" :disabled="loading">
              <span v-if="loading" class="spinner"></span>
              {{ loading ? 'Creating…' : 'Create Minor Account' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CreateBankAccountMinor',
  data() {
    return {
      accountHolderName: '', guardian_name: '', dateOfBirth: '', currentAddress: '',
      permanentAddress: '', sex: '', annualIncome: 0, occupation: 'Student',
      country: 'India', state: '', city: '', street: '', pincode: '',
      phoneNumber: '', email: '', aadharNumber: '', passportNumber: '',
      voterIdNumber: '', panCardNumber: '', photo: null, message: '', loading: false,
    };
  },
  methods: {
    onFileChange(e) { this.photo = e.target.files[0]; },
    async submitForm() {
      this.message = ''; this.loading = true;
      try {
        const formData = new FormData();
        formData.append('account_holder_name', this.accountHolderName);
        formData.append('guardian_name', this.guardian_name);
        formData.append('date_of_birth', this.dateOfBirth);
        formData.append('current_address', this.currentAddress);
        formData.append('Permanent_Address', this.permanentAddress);
        formData.append('sex', this.sex);
        formData.append('annual_income', this.annualIncome);
        formData.append('occupation', this.occupation);
        formData.append('country', this.country);
        formData.append('state', this.state);
        formData.append('city', this.city);
        formData.append('street', this.street);
        formData.append('pincode', this.pincode);
        formData.append('phone_number', this.phoneNumber);
        formData.append('email', this.email);
        formData.append('aadhar_number', this.aadharNumber);
        formData.append('passport_number', this.passportNumber);
        formData.append('voter_id_number', this.voterIdNumber);
        formData.append('pan_card_number', this.panCardNumber);
        if (this.photo) formData.append('photo', this.photo);

        const token = localStorage.getItem('token');
        await axios.post('http://127.0.0.1:8000/accounts/CreateBankAccountForMinor/', formData, {
          headers: { 'Content-Type': 'multipart/form-data', Authorization: `Token ${token}` },
        });
        this.message = 'Minor account created successfully!';
        setTimeout(() => this.$router.push('/Profile'), 1500);
      } catch (err) {
        this.message = err.response?.data ? JSON.stringify(err.response.data) : 'Failed to create account.';
      } finally { this.loading = false; }
    },
  },
};
</script>

<style scoped>
.form-page { min-height: 100vh; background: #f0f4f8; }
.page-header { display: flex; align-items: center; justify-content: space-between; padding: 16px 40px; background: #fff; border-bottom: 1px solid #e2e8f0; }
.back-link { display: flex; align-items: center; gap: 6px; font-size: 14px; font-weight: 600; color: #475569; text-decoration: none; }
.back-link svg { width: 18px; height: 18px; }
.back-link:hover { color: #7c3aed; }
.brand { display: flex; align-items: center; gap: 10px; font-size: 18px; font-weight: 700; color: #1e293b; }
.brand-icon { width: 34px; height: 34px; background: #7c3aed; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 800; color: #fff; }

.form-body { max-width: 780px; margin: 0 auto; padding: 36px 24px; }
.form-card { background: #fff; border-radius: 20px; box-shadow: 0 2px 16px rgba(15,32,68,.08); border: 1.5px solid #e2e8f0; overflow: hidden; }
.form-card-header { display: flex; align-items: center; gap: 16px; padding: 28px 32px; border-bottom: 1.5px solid #f1f5f9; background: linear-gradient(135deg, #f8fafc, #faf5ff); }
.hdr-icon { width: 48px; height: 48px; border-radius: 14px; display: flex; align-items: center; justify-content: center; }
.hdr-icon svg { width: 22px; height: 22px; }
.hdr-icon.purple { background: #faf5ff; color: #7c3aed; }
.form-title { font-size: 20px; font-weight: 800; color: #1e293b; }
.form-sub { font-size: 13px; color: #64748b; }

.form { padding: 28px 32px; display: flex; flex-direction: column; gap: 10px; }
.section-label { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; color: #7c3aed; margin-top: 14px; padding-bottom: 8px; border-bottom: 1px solid #e2e8f0; }
.row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.field { display: flex; flex-direction: column; gap: 5px; }
.field.full { grid-column: 1 / -1; }
.field label { font-size: 12px; font-weight: 600; color: #475569; }
.field input, .field select, .field textarea { padding: 10px 13px; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 14px; color: #1e293b; background: #f8fafc; outline: none; transition: border-color .18s, box-shadow .18s; resize: none; width: 100%; }
.field input:focus, .field select:focus, .field textarea:focus { border-color: #7c3aed; box-shadow: 0 0 0 3px rgba(124,58,237,.09); background: #fff; }

.upload-area { border: 2px dashed #ddd6fe; border-radius: 12px; padding: 28px; text-align: center; cursor: pointer; transition: all .18s; display: flex; flex-direction: column; align-items: center; gap: 8px; color: #64748b; }
.upload-area:hover { border-color: #7c3aed; background: #faf5ff; }
.upload-area svg { width: 32px; height: 32px; color: #94a3b8; }
.upload-area p { font-size: 14px; font-weight: 500; color: #475569; }
.upload-area span { font-size: 12px; color: #94a3b8; }

.alert { padding: 12px 16px; border-radius: 10px; font-size: 13px; }
.alert-error { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
.alert-success { background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }

.form-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 8px; }
.btn-primary { padding: 11px 28px; background: #7c3aed; color: #fff; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: background .18s; }
.btn-primary:hover:not(:disabled) { background: #6d28d9; }
.btn-primary:disabled { opacity: .6; cursor: not-allowed; }
.btn-secondary { padding: 11px 24px; background: #f1f5f9; color: #475569; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 14px; font-weight: 600; text-decoration: none; display: inline-flex; align-items: center; }
.btn-secondary:hover { background: #e2e8f0; }
.spinner { width: 15px; height: 15px; border: 2px solid rgba(255,255,255,.3); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
@media (max-width: 600px) { .row-2 { grid-template-columns: 1fr; } .form { padding: 20px; } }
</style>
