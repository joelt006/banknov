<template>
  <div class="cards-page">

    <div class="cards-header">
      <h2 class="section-title">My Cards</h2>
      <p class="section-sub">Select a card design and request it from the bank</p>
    </div>

    <!-- No account banner -->
    <div v-if="!accountNumber && !loading" class="info-banner warn">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      No bank account linked. Complete your registration to request cards.
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner-lg"></div>
      <p>Loading your cards…</p>
    </div>

    <template v-else>
      <!-- Cards grid -->
      <div class="cards-grid">
        <!-- Classic -->
        <div class="card-wrapper" :class="wrapperClass('classic')" @click="selectedCard = 'classic'">
          <div class="bank-card classic">
            <div class="card-top">
              <div class="card-brand">MyBank</div>
              <div class="card-chip"><div class="chip-line h"></div><div class="chip-line v"></div></div>
            </div>
            <div class="card-number">{{ maskedNumber }}</div>
            <div class="card-bottom">
              <div class="card-field">
                <span class="card-label">Card Holder</span>
                <span class="card-value">{{ holderName }}</span>
              </div>
              <div class="card-field">
                <span class="card-label">Valid Thru</span>
                <span class="card-value">{{ validThru }}</span>
              </div>
              <div class="card-network">
                <svg viewBox="0 0 50 30" fill="none"><circle cx="18" cy="15" r="12" fill="rgba(255,255,255,0.6)"/><circle cx="32" cy="15" r="12" fill="rgba(255,255,255,0.35)"/></svg>
              </div>
            </div>
            <div class="card-watermark">CLASSIC</div>
          </div>
          <div class="card-info">
            <div class="card-type-name">Classic</div>
            <div class="card-type-desc">Standard everyday banking with zero annual fee</div>
            <ul class="card-perks">
              <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> Free online transfers</li>
              <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> Zero annual fee</li>
              <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> Worldwide ATM access</li>
            </ul>
          </div>
          <div class="card-status-badge" :class="statusBadgeClass('classic')">
            <svg v-if="cardStatus('classic') === 'approved'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
            <svg v-else-if="cardStatus('classic') === 'pending'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <svg v-else-if="cardStatus('classic') === 'rejected'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
            {{ statusLabel('classic') }}
          </div>
        </div>

        <!-- Gold -->
        <div class="card-wrapper" :class="wrapperClass('gold')" @click="selectedCard = 'gold'">
          <div class="bank-card gold">
            <div class="card-top">
              <div class="card-brand">MyBank</div>
              <div class="card-chip gold-chip"><div class="chip-line h"></div><div class="chip-line v"></div></div>
            </div>
            <div class="card-number">{{ maskedNumber }}</div>
            <div class="card-bottom">
              <div class="card-field">
                <span class="card-label">Card Holder</span>
                <span class="card-value">{{ holderName }}</span>
              </div>
              <div class="card-field">
                <span class="card-label">Valid Thru</span>
                <span class="card-value">{{ validThru }}</span>
              </div>
              <div class="card-network">
                <svg viewBox="0 0 50 30" fill="none"><circle cx="18" cy="15" r="12" fill="rgba(255,215,0,0.7)"/><circle cx="32" cy="15" r="12" fill="rgba(255,215,0,0.4)"/></svg>
              </div>
            </div>
            <div class="card-watermark">GOLD</div>
          </div>
          <div class="card-info">
            <div class="card-type-name gold-text">Gold</div>
            <div class="card-type-desc">Premium benefits with higher transaction limits</div>
            <ul class="card-perks">
              <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> 2× reward points</li>
              <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> Higher transfer limits</li>
              <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> Priority customer support</li>
              <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> Travel insurance</li>
            </ul>
          </div>
          <div class="card-status-badge" :class="statusBadgeClass('gold')">
            <svg v-if="cardStatus('gold') === 'approved'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
            <svg v-else-if="cardStatus('gold') === 'pending'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <svg v-else-if="cardStatus('gold') === 'rejected'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
            {{ statusLabel('gold') }}
          </div>
        </div>

        <!-- Platinum -->
        <div class="card-wrapper" :class="wrapperClass('platinum')" @click="selectedCard = 'platinum'">
          <div class="bank-card platinum">
            <div class="card-top">
              <div class="card-brand">MyBank</div>
              <div class="card-chip plat-chip"><div class="chip-line h"></div><div class="chip-line v"></div></div>
            </div>
            <div class="card-number">{{ maskedNumber }}</div>
            <div class="card-bottom">
              <div class="card-field">
                <span class="card-label">Card Holder</span>
                <span class="card-value">{{ holderName }}</span>
              </div>
              <div class="card-field">
                <span class="card-label">Valid Thru</span>
                <span class="card-value">{{ validThru }}</span>
              </div>
              <div class="card-network">
                <svg viewBox="0 0 50 30" fill="none"><circle cx="18" cy="15" r="12" fill="rgba(229,228,226,0.5)"/><circle cx="32" cy="15" r="12" fill="rgba(229,228,226,0.3)"/></svg>
              </div>
            </div>
            <div class="card-watermark">PLATINUM</div>
          </div>
          <div class="card-info">
            <div class="card-type-name platinum-text">Platinum</div>
            <div class="card-type-desc">Elite privileges with unlimited access worldwide</div>
            <ul class="card-perks">
              <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> 5× reward points</li>
              <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> Unlimited transactions</li>
              <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> Airport lounge access</li>
              <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> Concierge service 24/7</li>
              <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> Comprehensive insurance</li>
            </ul>
          </div>
          <div class="card-status-badge" :class="statusBadgeClass('platinum')">
            <svg v-if="cardStatus('platinum') === 'approved'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
            <svg v-else-if="cardStatus('platinum') === 'pending'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <svg v-else-if="cardStatus('platinum') === 'rejected'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
            {{ statusLabel('platinum') }}
          </div>
        </div>
      </div>

      <!-- Request action panel -->
      <div v-if="accountNumber" class="action-panel">
        <div class="action-left">
          <div class="selected-card-info">
            <div class="selected-label">Selected Card</div>
            <div class="selected-name" :class="selectedCard + '-text'">
              {{ selectedCard.charAt(0).toUpperCase() + selectedCard.slice(1) }}
            </div>
          </div>

          <!-- Status-aware CTA -->
          <div v-if="cardStatus(selectedCard) === 'approved'" class="status-cta approved-cta">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            This card is active on your account
          </div>

          <div v-else-if="cardStatus(selectedCard) === 'pending'" class="status-cta pending-cta">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            Request pending — awaiting staff review
          </div>

          <div v-else-if="cardStatus(selectedCard) === 'rejected'" class="status-cta rejected-cta">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            <span>
              Previous request was rejected.
              <span v-if="latestRequest(selectedCard)?.admin_note" class="note-text">
                Reason: {{ latestRequest(selectedCard).admin_note }}
              </span>
            </span>
          </div>

          <button
            v-if="canRequest(selectedCard)"
            class="request-btn"
            :class="'request-' + selectedCard"
            :disabled="requesting"
            @click="requestCard"
          >
            <span v-if="requesting" class="btn-spinner"></span>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
            {{ requesting ? 'Submitting…' : 'Request ' + selectedCard.charAt(0).toUpperCase() + selectedCard.slice(1) + ' Card' }}
          </button>

          <div v-if="requestError" class="request-error">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            {{ requestError }}
          </div>
        </div>

        <div class="action-right">
          <div class="details-label-head">Account Details</div>
          <div class="details-row">
            <span class="details-label">Account Number</span>
            <span class="details-value mono">{{ accountNumber }}</span>
            <button class="copy-btn" @click="copyNumber" :class="{ copied }">
              <svg v-if="!copied" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              {{ copied ? 'Copied!' : 'Copy' }}
            </button>
          </div>
          <div class="details-row">
            <span class="details-label">Card Holder</span>
            <span class="details-value">{{ holderName }}</span>
          </div>
          <div class="details-row">
            <span class="details-label">Valid Thru</span>
            <span class="details-value">{{ validThru }}</span>
          </div>
        </div>
      </div>

      <!-- Request history -->
      <div v-if="accountNumber && cardRequests.length" class="history-section">
        <h3 class="history-title">Card Request History</h3>
        <div class="history-table-wrap">
          <table class="history-table">
            <thead>
              <tr>
                <th>Card Type</th>
                <th>Requested On</th>
                <th>Status</th>
                <th>Reviewed On</th>
                <th>Staff Note</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="r in cardRequests" :key="r.id">
                <td>
                  <span class="type-pill" :class="'type-' + r.card_type">
                    {{ r.card_type.charAt(0).toUpperCase() + r.card_type.slice(1) }}
                  </span>
                </td>
                <td class="date-cell">{{ formatDate(r.requested_at) }}</td>
                <td>
                  <span class="status-pill" :class="'status-' + r.status">
                    {{ r.status.charAt(0).toUpperCase() + r.status.slice(1) }}
                  </span>
                </td>
                <td class="date-cell">{{ r.reviewed_at ? formatDate(r.reviewed_at) : '—' }}</td>
                <td class="note-cell">{{ r.admin_note || '—' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

export default {
  name: 'MyCards',
  data() {
    return {
      accountNumber: '',
      holderName: '',
      loading: true,
      selectedCard: 'classic',
      copied: false,
      cardRequests: [],
      requesting: false,
      requestError: '',
    };
  },
  computed: {
    maskedNumber() {
      if (!this.accountNumber) return '**** **** **** ****';
      const n = this.accountNumber.replace(/\D/g, '');
      return `**** **** **** ${n.slice(-4).padStart(4, '*')}`;
    },
    validThru() {
      const now = new Date();
      const exp = new Date(now.getFullYear() + 4, now.getMonth());
      return `${String(exp.getMonth() + 1).padStart(2, '0')}/${String(exp.getFullYear()).slice(-2)}`;
    },
  },
  async created() {
    try {
      const [profileRes, requestsRes] = await Promise.allSettled([
        apiClient.get('/accounts/profile/'),
        apiClient.get('/accounts/card-requests/'),
      ]);
      if (profileRes.status === 'fulfilled') {
        this.accountNumber = profileRes.value.data.account_number || '';
        this.holderName = (profileRes.value.data.account_holder_name || '').toUpperCase();
      }
      if (requestsRes.status === 'fulfilled') {
        this.cardRequests = requestsRes.value.data;
      }
    } finally {
      this.loading = false;
    }
  },
  methods: {
    latestRequest(cardType) {
      return this.cardRequests.find(r => r.card_type === cardType) || null;
    },
    cardStatus(cardType) {
      const req = this.latestRequest(cardType);
      return req ? req.status : null;
    },
    canRequest(cardType) {
      const s = this.cardStatus(cardType);
      return !s || s === 'rejected';
    },
    wrapperClass(cardType) {
      const s = this.cardStatus(cardType);
      return {
        selected: this.selectedCard === cardType,
        'has-approved': s === 'approved',
        'has-pending': s === 'pending',
        'has-rejected': s === 'rejected',
      };
    },
    statusBadgeClass(cardType) {
      const s = this.cardStatus(cardType);
      if (s === 'approved') return 'badge-approved';
      if (s === 'pending')  return 'badge-pending';
      if (s === 'rejected') return 'badge-rejected';
      if (this.selectedCard === cardType) return 'badge-selected';
      return 'badge-hidden';
    },
    statusLabel(cardType) {
      const s = this.cardStatus(cardType);
      if (s === 'approved') return 'Active';
      if (s === 'pending')  return 'Pending';
      if (s === 'rejected') return 'Rejected';
      if (this.selectedCard === cardType) return 'Selected';
      return '';
    },
    async requestCard() {
      this.requestError = '';
      this.requesting = true;
      try {
        const res = await apiClient.post('/accounts/card-requests/', { card_type: this.selectedCard });
        this.cardRequests.unshift(res.data);
      } catch (err) {
        this.requestError = err.response?.data?.error || 'Failed to submit request. Try again.';
      } finally {
        this.requesting = false;
      }
    },
    copyNumber() {
      navigator.clipboard.writeText(this.accountNumber).then(() => {
        this.copied = true;
        setTimeout(() => { this.copied = false; }, 2000);
      });
    },
    formatDate(iso) {
      return new Date(iso).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
    },
  },
};
</script>

<style scoped>
.cards-page { display: flex; flex-direction: column; gap: 28px; }

.section-title { font-size: 22px; font-weight: 800; color: #1e293b; }
.section-sub { font-size: 14px; color: #64748b; margin-top: 4px; }

.info-banner {
  display: flex; align-items: center; gap: 12px;
  border-radius: 12px; padding: 14px 20px;
  font-size: 14px; font-weight: 500;
}
.info-banner svg { width: 20px; height: 20px; flex-shrink: 0; }
.warn { background: #fffbeb; border: 1.5px solid #fde68a; color: #92400e; }

.loading-state { display: flex; flex-direction: column; align-items: center; gap: 14px; padding: 60px; color: #94a3b8; font-size: 14px; }
.spinner-lg { width: 36px; height: 36px; border: 3px solid #e2e8f0; border-top-color: #2563eb; border-radius: 50%; animation: spin .7s linear infinite; }

/* Grid */
.cards-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }

.card-wrapper {
  position: relative; background: #fff; border-radius: 20px;
  border: 2px solid #e2e8f0; padding: 0 0 24px;
  cursor: pointer; transition: all .2s;
  box-shadow: 0 2px 8px rgba(15,32,68,.06); overflow: hidden;
}
.card-wrapper:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(15,32,68,.12); }
.card-wrapper.selected { border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37,99,235,.12), 0 12px 32px rgba(15,32,68,.1); }
.card-wrapper.has-approved { border-color: #16a34a; box-shadow: 0 0 0 3px rgba(22,163,74,.1); }
.card-wrapper.has-pending  { border-color: #d97706; box-shadow: 0 0 0 3px rgba(217,119,6,.1); }
.card-wrapper.has-rejected { border-color: #dc2626; box-shadow: 0 0 0 3px rgba(220,38,38,.08); }

/* Bank card */
.bank-card {
  position: relative; width: 100%; aspect-ratio: 1.586/1;
  border-radius: 0; padding: 20px 24px;
  display: flex; flex-direction: column; justify-content: space-between;
  color: #fff; overflow: hidden; font-family: 'Courier New', monospace;
}
.bank-card.classic  { background: linear-gradient(135deg, #1a2f5e 0%, #2563eb 60%, #3b82f6 100%); }
.bank-card.gold     { background: linear-gradient(135deg, #78350f 0%, #d97706 55%, #f59e0b 100%); }
.bank-card.platinum { background: linear-gradient(135deg, #1e293b 0%, #374151 50%, #4b5563 100%); }

.card-top { display: flex; justify-content: space-between; align-items: flex-start; }
.card-brand { font-size: 15px; font-weight: 800; letter-spacing: .5px; font-family: 'Segoe UI', sans-serif; }

.card-chip { width: 36px; height: 28px; background: rgba(255,255,255,.15); border-radius: 5px; position: relative; border: 1px solid rgba(255,255,255,.3); }
.gold-chip { background: rgba(255,215,0,.3); border-color: rgba(255,215,0,.5); }
.plat-chip { background: rgba(229,228,226,.2); border-color: rgba(229,228,226,.4); }
.chip-line { position: absolute; background: rgba(255,255,255,.3); }
.chip-line.h { width: 100%; height: 1px; top: 50%; left: 0; }
.chip-line.v { width: 1px; height: 100%; left: 50%; top: 0; }

.card-number { font-size: 17px; letter-spacing: 3px; font-weight: 600; text-align: center; }
.card-bottom { display: flex; justify-content: space-between; align-items: flex-end; }
.card-field { display: flex; flex-direction: column; gap: 2px; }
.card-label { font-size: 8px; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,.6); font-family: 'Segoe UI', sans-serif; }
.card-value { font-size: 12px; font-weight: 700; letter-spacing: .5px; max-width: 130px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.card-network svg { width: 44px; }
.card-watermark { position: absolute; bottom: 12px; right: 0; left: 0; text-align: center; font-size: 36px; font-weight: 900; color: rgba(255,255,255,.05); letter-spacing: 6px; pointer-events: none; }

/* Card info */
.card-info { padding: 20px 20px 0; }
.card-type-name { font-size: 17px; font-weight: 800; color: #1e293b; margin-bottom: 4px; }
.gold-text { color: #92400e; }
.platinum-text { color: #374151; }
.card-type-desc { font-size: 12px; color: #64748b; margin-bottom: 16px; }
.card-perks { list-style: none; display: flex; flex-direction: column; gap: 7px; }
.card-perks li { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #475569; font-weight: 500; }
.card-perks li svg { width: 14px; height: 14px; color: #10b981; flex-shrink: 0; }

/* Status badge on card corner */
.card-status-badge {
  position: absolute; top: 12px; right: 12px;
  border-radius: 20px; padding: 5px 12px;
  font-size: 11px; font-weight: 700;
  display: flex; align-items: center; gap: 5px;
}
.card-status-badge svg { width: 12px; height: 12px; }
.badge-approved  { background: #16a34a; color: #fff; }
.badge-pending   { background: #d97706; color: #fff; }
.badge-rejected  { background: #dc2626; color: #fff; }
.badge-selected  { background: #2563eb; color: #fff; }
.badge-hidden    { display: none; }

/* Action panel */
.action-panel {
  display: flex; gap: 24px; flex-wrap: wrap;
  background: #fff; border: 1.5px solid #e2e8f0; border-radius: 16px;
  box-shadow: 0 2px 8px rgba(15,32,68,.06); overflow: hidden;
}
.action-left {
  flex: 1; min-width: 280px;
  padding: 28px; display: flex; flex-direction: column; gap: 16px;
  border-right: 1px solid #f1f5f9;
}
.action-right { flex: 1; min-width: 260px; padding: 28px; }

.selected-label { font-size: 12px; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 4px; }
.selected-name { font-size: 24px; font-weight: 900; color: #1e293b; }
.classic-text  { color: #1d4ed8; }
.gold-text     { color: #92400e; }
.platinum-text { color: #374151; }

.status-cta {
  display: flex; align-items: flex-start; gap: 10px;
  padding: 14px 16px; border-radius: 10px;
  font-size: 13px; font-weight: 600;
}
.status-cta svg { width: 18px; height: 18px; flex-shrink: 0; margin-top: 1px; }
.approved-cta { background: #f0fdf4; color: #16a34a; }
.pending-cta  { background: #fffbeb; color: #92400e; }
.rejected-cta { background: #fff1f2; color: #dc2626; }
.note-text { display: block; font-weight: 500; margin-top: 4px; font-style: italic; }

.request-btn {
  display: flex; align-items: center; justify-content: center; gap: 10px;
  padding: 13px 20px; border: none; border-radius: 10px;
  font-size: 14px; font-weight: 700; color: #fff; cursor: pointer;
  transition: opacity .18s, transform .18s;
  box-shadow: 0 4px 14px rgba(0,0,0,.2);
}
.request-btn:disabled { opacity: .6; cursor: not-allowed; transform: none; }
.request-btn:hover:not(:disabled) { opacity: .9; transform: translateY(-1px); }
.request-btn svg { width: 16px; height: 16px; }
.request-classic  { background: linear-gradient(135deg, #1a2f5e, #2563eb); }
.request-gold     { background: linear-gradient(135deg, #78350f, #d97706); }
.request-platinum { background: linear-gradient(135deg, #1e293b, #374151); }

.btn-spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,.3); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; }

.request-error {
  display: flex; align-items: center; gap: 8px;
  background: #fff1f2; border: 1px solid #fecaca;
  border-radius: 8px; padding: 10px 14px; color: #dc2626; font-size: 13px;
}
.request-error svg { width: 16px; height: 16px; flex-shrink: 0; }

/* Account details */
.details-label-head { font-size: 12px; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 16px; }
.details-row { display: flex; align-items: center; gap: 12px; padding: 10px 0; border-bottom: 1px solid #f1f5f9; }
.details-row:last-child { border-bottom: none; }
.details-label { font-size: 13px; color: #64748b; min-width: 120px; }
.details-value { font-size: 13px; font-weight: 600; color: #1e293b; flex: 1; }
.details-value.mono { font-family: 'Courier New', monospace; letter-spacing: 1px; }

.copy-btn {
  display: flex; align-items: center; gap: 5px;
  padding: 5px 10px; border-radius: 6px; border: 1.5px solid #e2e8f0;
  background: #f8fafc; color: #475569; font-size: 11px; font-weight: 600; cursor: pointer;
  transition: all .15s;
}
.copy-btn:hover { background: #eff6ff; border-color: #bfdbfe; color: #2563eb; }
.copy-btn.copied { background: #f0fdf4; border-color: #bbf7d0; color: #16a34a; }
.copy-btn svg { width: 13px; height: 13px; }

/* History */
.history-section { }
.history-title { font-size: 16px; font-weight: 700; color: #1e293b; margin-bottom: 14px; }
.history-table-wrap { background: #fff; border: 1.5px solid #e2e8f0; border-radius: 14px; overflow: hidden; }
.history-table { width: 100%; border-collapse: collapse; }
.history-table thead tr { background: #f8fafc; border-bottom: 2px solid #e2e8f0; }
.history-table th { padding: 12px 18px; font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: .6px; text-align: left; }
.history-table tbody tr { border-bottom: 1px solid #f1f5f9; }
.history-table tbody tr:last-child { border-bottom: none; }
.history-table td { padding: 13px 18px; font-size: 13px; }

.date-cell { color: #64748b; }
.note-cell { color: #64748b; font-style: italic; max-width: 200px; }

.type-pill { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; }
.type-classic  { background: #eff6ff; color: #1d4ed8; }
.type-gold     { background: #fffbeb; color: #92400e; }
.type-platinum { background: #f1f5f9; color: #374151; }

.status-pill { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; }
.status-pending  { background: #fffbeb; color: #92400e; }
.status-approved { background: #f0fdf4; color: #16a34a; }
.status-rejected { background: #fff1f2; color: #dc2626; }

@keyframes spin { to { transform: rotate(360deg); } }
@media (max-width: 900px) { .cards-grid { grid-template-columns: 1fr; } .action-panel { flex-direction: column; } .action-left { border-right: none; border-bottom: 1px solid #f1f5f9; } }
</style>
