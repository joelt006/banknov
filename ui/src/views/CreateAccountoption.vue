<template>
  <div class="co-page">
    <div class="co-header">
      <RouterLink to="/Login" class="back-link">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
        Back to Login
      </RouterLink>
      <div class="brand">
        <div class="brand-icon">MB</div>
        <span>MyBank</span>
      </div>
    </div>

    <div class="co-body">
      <h1 class="co-title">Open a Bank Account</h1>
      <p class="co-sub">Choose the account type that best suits you</p>

      <div class="cards-grid">

        <RouterLink to="/CreateBankAccount" class="type-card">
          <div class="type-icon blue">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          </div>
          <h3 class="type-name">Standard Account</h3>
          <p class="type-desc">For adults 18 years and above. Full banking privileges with no restrictions.</p>
          <ul class="type-features">
            <li>✓ Unlimited transactions</li>
            <li>✓ Internet banking access</li>
            <li>✓ Debit card eligibility</li>
          </ul>
          <div class="type-cta">Open Account <span>→</span></div>
        </RouterLink>

        <RouterLink to="/CreateBankAccountMinor" class="type-card">
          <div class="type-icon purple">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          </div>
          <h3 class="type-name">Minor Account</h3>
          <p class="type-desc">For children below 18 years. Operated jointly with a guardian for financial literacy.</p>
          <ul class="type-features">
            <li>✓ Guardian-managed access</li>
            <li>✓ Savings-focused features</li>
            <li>✓ Converts at 18 years</li>
          </ul>
          <div class="type-cta">Open Account <span>→</span></div>
        </RouterLink>

        <RouterLink to="/CreateBankAccountSenior" class="type-card">
          <div class="type-icon gold">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          </div>
          <h3 class="type-name">Senior Citizen Account</h3>
          <p class="type-desc">Exclusive benefits for citizens aged 65+. Priority service and higher interest rates.</p>
          <ul class="type-features">
            <li>✓ Higher interest rates</li>
            <li>✓ Priority customer service</li>
            <li>✓ Special benefits & offers</li>
          </ul>
          <div class="type-cta">Open Account <span>→</span></div>
        </RouterLink>

      </div>

      <p class="note">Already have an account? <RouterLink to="/Register">Register for net banking</RouterLink></p>
    </div>
  </div>
</template>

<style scoped>
.co-page { min-height: 100vh; background: #f0f4f8; }

.co-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 20px 40px; background: #fff; border-bottom: 1px solid #e2e8f0;
}
.back-link { display: flex; align-items: center; gap: 6px; font-size: 14px; font-weight: 600; color: #475569; text-decoration: none; transition: color .15s; }
.back-link svg { width: 18px; height: 18px; }
.back-link:hover { color: #2563eb; }

.brand { display: flex; align-items: center; gap: 10px; font-size: 18px; font-weight: 700; color: #1e293b; }
.brand-icon { width: 36px; height: 36px; background: #2563eb; border-radius: 9px; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 800; color: #fff; }

.co-body { max-width: 1000px; margin: 0 auto; padding: 60px 24px; text-align: center; }
.co-title { font-size: 36px; font-weight: 800; color: #1e293b; margin-bottom: 12px; }
.co-sub { font-size: 16px; color: #64748b; margin-bottom: 48px; }

.cards-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; text-align: left; margin-bottom: 40px; }

.type-card {
  background: #fff; border-radius: 20px; padding: 32px 28px;
  border: 2px solid #e2e8f0; text-decoration: none; color: #1e293b;
  display: flex; flex-direction: column; gap: 14px;
  transition: transform .2s, box-shadow .2s, border-color .2s;
  box-shadow: 0 2px 8px rgba(15,32,68,.06);
}
.type-card:hover { transform: translateY(-5px); box-shadow: 0 12px 32px rgba(15,32,68,.12); border-color: #bfdbfe; }

.type-icon { width: 56px; height: 56px; border-radius: 16px; display: flex; align-items: center; justify-content: center; }
.type-icon svg { width: 26px; height: 26px; }
.type-icon.blue   { background: #eff6ff; color: #2563eb; }
.type-icon.purple { background: #faf5ff; color: #7c3aed; }
.type-icon.gold   { background: #fffbeb; color: #d97706; }

.type-name { font-size: 18px; font-weight: 800; color: #1e293b; }
.type-desc { font-size: 13px; color: #64748b; line-height: 1.6; }

.type-features { list-style: none; display: flex; flex-direction: column; gap: 6px; flex: 1; }
.type-features li { font-size: 13px; color: #475569; }

.type-cta {
  display: flex; align-items: center; justify-content: space-between;
  font-size: 14px; font-weight: 700; color: #2563eb;
  padding-top: 12px; border-top: 1px solid #f1f5f9;
}
.type-cta span { font-size: 18px; transition: transform .18s; }
.type-card:hover .type-cta span { transform: translateX(4px); }

.note { font-size: 14px; color: #64748b; }
.note a { color: #2563eb; font-weight: 600; }

@media (max-width: 768px) { .cards-grid { grid-template-columns: 1fr; } .co-title { font-size: 26px; } }
</style>
