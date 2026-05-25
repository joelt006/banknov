<template>
  <div class="cards-page">

    <div class="cards-header">
      <h2 class="section-title">My Cards</h2>
      <p class="section-sub">Select a card design and request it from the bank</p>
    </div>

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
        <div
          v-for="type in ['classic', 'gold', 'platinum']"
          :key="type"
          class="card-wrapper"
          :class="wrapperClass(type)"
          @click="selectedCard = type"
        >
          <div class="bank-card" :class="type">
            <div class="card-top">
              <div class="card-brand">MyBank</div>
              <div class="card-chip" :class="type + '-chip'">
                <div class="chip-line h"></div>
                <div class="chip-line v"></div>
              </div>
            </div>
            <div class="card-number">{{ cardFaceNumber(type) }}</div>
            <div class="card-bottom">
              <div class="card-field">
                <span class="card-label">Card Holder</span>
                <span class="card-value">{{ holderName }}</span>
              </div>
              <div class="card-field">
                <span class="card-label">Valid Thru</span>
                <span class="card-value">{{ cardFaceExpiry(type) }}</span>
              </div>
              <div class="card-network">
                <svg v-if="type === 'classic'" viewBox="0 0 50 30" fill="none"><circle cx="18" cy="15" r="12" fill="rgba(255,255,255,0.6)"/><circle cx="32" cy="15" r="12" fill="rgba(255,255,255,0.35)"/></svg>
                <svg v-else-if="type === 'gold'" viewBox="0 0 50 30" fill="none"><circle cx="18" cy="15" r="12" fill="rgba(255,215,0,0.7)"/><circle cx="32" cy="15" r="12" fill="rgba(255,215,0,0.4)"/></svg>
                <svg v-else viewBox="0 0 50 30" fill="none"><circle cx="18" cy="15" r="12" fill="rgba(229,228,226,0.5)"/><circle cx="32" cy="15" r="12" fill="rgba(229,228,226,0.3)"/></svg>
              </div>
            </div>
            <div class="card-watermark">{{ type.toUpperCase() }}</div>
          </div>

          <div class="card-info">
            <div class="card-type-name" :class="type + '-text'">
              {{ type.charAt(0).toUpperCase() + type.slice(1) }}
            </div>
            <div class="card-type-desc">{{ cardDesc[type] }}</div>
            <ul class="card-perks">
              <li v-for="perk in cardPerks[type]" :key="perk">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                {{ perk }}
              </li>
            </ul>
          </div>

          <div class="card-status-badge" :class="statusBadgeClass(type)">
            <svg v-if="cardStatus(type) === 'approved'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
            <svg v-else-if="cardStatus(type) === 'pending'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <svg v-else-if="cardStatus(type) === 'rejected'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
            {{ statusLabel(type) }}
          </div>
        </div>
      </div>

      <!-- Action + details panel -->
      <div v-if="accountNumber" class="action-panel">

        <!-- Left: request CTA -->
        <div class="action-left">
          <div>
            <div class="selected-label">Selected Card</div>
            <div class="selected-name" :class="selectedCard + '-text'">
              {{ selectedCard.charAt(0).toUpperCase() + selectedCard.slice(1) }}
            </div>
          </div>

          <div v-if="cardStatus(selectedCard) === 'approved'" class="status-cta approved-cta">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            Your {{ selectedCard }} card is active
          </div>
          <div v-else-if="cardStatus(selectedCard) === 'pending'" class="status-cta pending-cta">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            Request pending — awaiting staff review
          </div>
          <div v-else-if="cardStatus(selectedCard) === 'rejected'" class="status-cta rejected-cta">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            <span>
              Request was rejected.
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

        <!-- Right: card details -->
        <div class="action-right">
          <!-- Approved card details -->
          <template v-if="cardStatus(selectedCard) === 'approved' && approvedCard(selectedCard)">
            <div class="details-section-head">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
              Card Details
            </div>

            <!-- Card number -->
            <div class="detail-row">
              <span class="detail-label">Card Number</span>
              <div class="detail-value-wrap">
                <span class="detail-value mono">
                  {{ showCardNumber ? formatCardNumber(approvedCard(selectedCard).card_number) : maskCardNumber(approvedCard(selectedCard).card_number) }}
                </span>
                <button class="icon-btn" @click="showCardNumber = !showCardNumber" :title="showCardNumber ? 'Hide' : 'Show'">
                  <svg v-if="!showCardNumber" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                </button>
                <button class="icon-btn copy-icon" @click="copyValue(approvedCard(selectedCard).card_number, 'card')" :title="copied === 'card' ? 'Copied!' : 'Copy'">
                  <svg v-if="copied !== 'card'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                </button>
              </div>
            </div>

            <!-- Expiry -->
            <div class="detail-row">
              <span class="detail-label">Expiry Date</span>
              <div class="detail-value-wrap">
                <span class="detail-value mono">{{ approvedCard(selectedCard).expiry_date }}</span>
              </div>
            </div>

            <!-- CVV -->
            <div class="detail-row">
              <span class="detail-label">CVV</span>
              <div class="detail-value-wrap">
                <span class="detail-value mono cvv-value">{{ showCvv ? approvedCard(selectedCard).cvv : '•••' }}</span>
                <button class="icon-btn" @click="revealCvv" :title="showCvv ? 'Hide CVV' : 'Reveal CVV'">
                  <svg v-if="!showCvv" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                </button>
                <span v-if="showCvv" class="cvv-timer">hides in {{ cvvCountdown }}s</span>
              </div>
            </div>

            <!-- Network type -->
            <div class="detail-row">
              <span class="detail-label">Network</span>
              <div class="detail-value-wrap">
                <span class="detail-value">{{ networkName(selectedCard) }}</span>
                <span class="network-badge" :class="'net-' + selectedCard">{{ networkName(selectedCard) }}</span>
              </div>
            </div>

            <!-- Block card -->
            <div class="detail-row" style="margin-top:8px">
              <span class="detail-label">Card Status</span>
              <div class="detail-value-wrap">
                <span class="card-block-badge" :class="cardControls(selectedCard)?.is_blocked ? 'blocked' : 'active-badge'">
                  {{ cardControls(selectedCard)?.is_blocked ? '● Blocked' : '● Active' }}
                </span>
                <button
                  class="icon-btn block-btn"
                  :class="cardControls(selectedCard)?.is_blocked ? 'unblock' : 'block'"
                  @click="toggleBlock(selectedCard)"
                  :disabled="controlsSaving"
                >
                  {{ cardControls(selectedCard)?.is_blocked ? 'Unblock' : 'Block Card' }}
                </button>
              </div>
            </div>

            <!-- Card controls -->
            <div class="controls-section">
              <div class="controls-head">Card Controls</div>
              <div class="control-row" v-for="ctrl in controlsList" :key="ctrl.key">
                <div class="control-info">
                  <div class="control-name">{{ ctrl.label }}</div>
                  <div class="control-desc">{{ ctrl.desc }}</div>
                </div>
                <label class="toggle-label">
                  <input
                    type="checkbox"
                    :checked="cardControls(selectedCard)?.[ctrl.key]"
                    @change="updateControl(selectedCard, ctrl.key, $event.target.checked)"
                    :disabled="controlsSaving || cardControls(selectedCard)?.is_blocked"
                  />
                  <span class="toggle-track"><span class="toggle-thumb"></span></span>
                </label>
              </div>
            </div>

            <div class="security-note">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              Never share your CVV or full card number with anyone
            </div>
          </template>

          <!-- Not approved: show account info -->
          <template v-else>
            <div class="details-section-head">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
              Account Details
            </div>
            <div class="detail-row">
              <span class="detail-label">Account Number</span>
              <div class="detail-value-wrap">
                <span class="detail-value mono">{{ accountNumber }}</span>
                <button class="icon-btn copy-icon" @click="copyValue(accountNumber, 'acc')" :title="copied === 'acc' ? 'Copied!' : 'Copy'">
                  <svg v-if="copied !== 'acc'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                </button>
              </div>
            </div>
            <div class="detail-row">
              <span class="detail-label">Card Holder</span>
              <span class="detail-value">{{ holderName }}</span>
            </div>
            <div class="no-card-hint">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              Request a card to see your card number, expiry, and CVV here
            </div>
          </template>
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
                <th>Card Number</th>
                <th>Expiry</th>
                <th>Requested On</th>
                <th>Status</th>
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
                <td class="mono-cell">
                  <span v-if="r.card_number">{{ maskCardNumber(r.card_number) }}</span>
                  <span v-else class="muted">—</span>
                </td>
                <td class="mono-cell">{{ r.expiry_date || '—' }}</td>
                <td class="date-cell">{{ formatDate(r.requested_at) }}</td>
                <td>
                  <span class="status-pill" :class="'status-' + r.status">
                    {{ r.status.charAt(0).toUpperCase() + r.status.slice(1) }}
                  </span>
                </td>
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
      copied: null,
      cardRequests: [],
      requesting: false,
      requestError: '',
      showCardNumber: false,
      showCvv: false,
      cvvCountdown: 10,
      cvvTimer: null,
      controlsSaving: false,
      cardControlsMap: {},   // card id → controls object
      controlsList: [
        { key: 'allow_international', label: 'International Transactions', desc: 'Allow payments outside India' },
        { key: 'allow_online',        label: 'Online Payments',            desc: 'Allow e-commerce & app payments' },
        { key: 'allow_contactless',   label: 'Contactless / NFC',          desc: 'Allow tap-to-pay transactions' },
      ],
      cardDesc: {
        classic: 'Standard everyday banking with zero annual fee',
        gold: 'Premium benefits with higher transaction limits',
        platinum: 'Elite privileges with unlimited access worldwide',
      },
      cardPerks: {
        classic: ['Free online transfers', 'Zero annual fee', 'Worldwide ATM access'],
        gold: ['2× reward points', 'Higher transfer limits', 'Travel insurance'],
        platinum: ['5× reward points', 'Airport lounge access', 'Concierge 24/7'],
      },
    };
  },
  computed: {
    validThru() {
      const now = new Date();
      return `${String(now.getMonth() + 1).padStart(2, '0')}/${String(now.getFullYear() + 4).slice(-2)}`;
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
    // Load controls for whichever card starts selected
    if (this.cardStatus(this.selectedCard) === 'approved') {
      this.loadControls(this.selectedCard);
    }
  },
  watch: {
    selectedCard(type) {
      this.showCardNumber = false;
      this.stopCvvTimer();
      if (this.cardStatus(type) === 'approved') this.loadControls(type);
    },
  },
  beforeUnmount() { this.stopCvvTimer(); },
  methods: {
    approvedCard(cardType) {
      return this.cardRequests.find(r => r.card_type === cardType && r.status === 'approved') || null;
    },
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

    cardFaceNumber(cardType) {
      const approved = this.approvedCard(cardType);
      if (approved?.card_number) {
        const n = approved.card_number;
        return `${n.slice(0,4)} **** **** ${n.slice(-4)}`;
      }
      if (!this.accountNumber) return '**** **** **** ****';
      return `**** **** **** ${this.accountNumber.slice(-4)}`;
    },
    cardFaceExpiry(cardType) {
      const approved = this.approvedCard(cardType);
      return approved?.expiry_date || this.validThru;
    },

    formatCardNumber(num) {
      if (!num) return '';
      return num.replace(/(.{4})/g, '$1 ').trim();
    },
    maskCardNumber(num) {
      if (!num) return '';
      return `${num.slice(0,4)} **** **** ${num.slice(-4)}`;
    },

    networkName(cardType) {
      return { classic: 'Visa', gold: 'Mastercard', platinum: 'Amex' }[cardType] || 'Visa';
    },

    wrapperClass(cardType) {
      const s = this.cardStatus(cardType);
      return {
        selected: this.selectedCard === cardType,
        'has-approved': s === 'approved',
        'has-pending':  s === 'pending',
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

    revealCvv() {
      if (this.showCvv) { this.stopCvvTimer(); return; }
      this.showCvv = true;
      this.cvvCountdown = 10;
      this.cvvTimer = setInterval(() => {
        this.cvvCountdown--;
        if (this.cvvCountdown <= 0) this.stopCvvTimer();
      }, 1000);
    },
    stopCvvTimer() {
      clearInterval(this.cvvTimer);
      this.showCvv = false;
      this.cvvCountdown = 10;
    },

    copyValue(val, key) {
      navigator.clipboard.writeText(val).then(() => {
        this.copied = key;
        setTimeout(() => { this.copied = null; }, 2000);
      });
    },
    formatDate(iso) {
      return new Date(iso).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
    },

    // Card controls
    cardControls(cardType) {
      const card = this.approvedCard(cardType);
      if (!card) return null;
      return this.cardControlsMap[card.id] ?? null;
    },
    async loadControls(cardType) {
      const card = this.approvedCard(cardType);
      if (!card || this.cardControlsMap[card.id]) return;
      try {
        const res = await apiClient.get(`/accounts/card-requests/${card.id}/settings/`);
        this.cardControlsMap = { ...this.cardControlsMap, [card.id]: res.data };
      } catch { /* silent */ }
    },
    async toggleBlock(cardType) {
      const card = this.approvedCard(cardType);
      const ctrl = this.cardControls(cardType);
      if (!card || !ctrl) return;
      this.controlsSaving = true;
      try {
        const res = await apiClient.patch(`/accounts/card-requests/${card.id}/settings/`, {
          is_blocked: !ctrl.is_blocked,
        });
        this.cardControlsMap = { ...this.cardControlsMap, [card.id]: res.data };
      } catch { /* silent */ } finally {
        this.controlsSaving = false;
      }
    },
    async updateControl(cardType, field, value) {
      const card = this.approvedCard(cardType);
      if (!card) return;
      this.controlsSaving = true;
      try {
        const res = await apiClient.patch(`/accounts/card-requests/${card.id}/settings/`, { [field]: value });
        this.cardControlsMap = { ...this.cardControlsMap, [card.id]: res.data };
      } catch { /* silent */ } finally {
        this.controlsSaving = false;
      }
    },
  },
};
</script>

<style scoped>
.cards-page { display: flex; flex-direction: column; gap: 28px; }
.section-title { font-size: 22px; font-weight: 800; color: #1e293b; }
.section-sub   { font-size: 14px; color: #64748b; margin-top: 4px; }

.info-banner { display: flex; align-items: center; gap: 12px; border-radius: 12px; padding: 14px 20px; font-size: 14px; font-weight: 500; }
.info-banner svg { width: 20px; height: 20px; flex-shrink: 0; }
.warn { background: #fffbeb; border: 1.5px solid #fde68a; color: #92400e; }

.loading-state { display: flex; flex-direction: column; align-items: center; gap: 14px; padding: 60px; color: #94a3b8; font-size: 14px; }
.spinner-lg { width: 36px; height: 36px; border: 3px solid #e2e8f0; border-top-color: #2563eb; border-radius: 50%; animation: spin .7s linear infinite; }

/* Grid */
.cards-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }

.card-wrapper { position: relative; background: #fff; border-radius: 20px; border: 2px solid #e2e8f0; padding: 0 0 24px; cursor: pointer; transition: all .2s; box-shadow: 0 2px 8px rgba(15,32,68,.06); overflow: hidden; }
.card-wrapper:hover        { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(15,32,68,.12); }
.card-wrapper.selected     { border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37,99,235,.12); }
.card-wrapper.has-approved { border-color: #16a34a; box-shadow: 0 0 0 3px rgba(22,163,74,.12); }
.card-wrapper.has-pending  { border-color: #d97706; box-shadow: 0 0 0 3px rgba(217,119,6,.1); }
.card-wrapper.has-rejected { border-color: #dc2626; box-shadow: 0 0 0 3px rgba(220,38,38,.08); }

/* Bank card face */
.bank-card { position: relative; width: 100%; aspect-ratio: 1.586/1; padding: 20px 24px; display: flex; flex-direction: column; justify-content: space-between; color: #fff; overflow: hidden; font-family: 'Courier New', monospace; }
.classic  { background: linear-gradient(135deg, #1a2f5e 0%, #2563eb 60%, #3b82f6 100%); }
.gold     { background: linear-gradient(135deg, #78350f 0%, #d97706 55%, #f59e0b 100%); }
.platinum { background: linear-gradient(135deg, #1e293b 0%, #374151 50%, #4b5563 100%); }

.card-top   { display: flex; justify-content: space-between; align-items: flex-start; }
.card-brand { font-size: 15px; font-weight: 800; letter-spacing: .5px; font-family: 'Segoe UI', sans-serif; }
.card-chip  { width: 36px; height: 28px; background: rgba(255,255,255,.15); border-radius: 5px; position: relative; border: 1px solid rgba(255,255,255,.3); }
.gold-chip      { background: rgba(255,215,0,.3); border-color: rgba(255,215,0,.5); }
.platinum-chip  { background: rgba(229,228,226,.2); border-color: rgba(229,228,226,.4); }
.chip-line   { position: absolute; background: rgba(255,255,255,.3); }
.chip-line.h { width: 100%; height: 1px; top: 50%; left: 0; }
.chip-line.v { width: 1px; height: 100%; left: 50%; top: 0; }

.card-number { font-size: 15px; letter-spacing: 3px; font-weight: 600; text-align: center; }
.card-bottom { display: flex; justify-content: space-between; align-items: flex-end; }
.card-field  { display: flex; flex-direction: column; gap: 2px; }
.card-label  { font-size: 8px; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,.6); font-family: 'Segoe UI', sans-serif; }
.card-value  { font-size: 11px; font-weight: 700; max-width: 120px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.card-network svg { width: 44px; }
.card-watermark { position: absolute; bottom: 12px; right: 0; left: 0; text-align: center; font-size: 34px; font-weight: 900; color: rgba(255,255,255,.05); letter-spacing: 6px; pointer-events: none; }

/* Card info below face */
.card-info { padding: 18px 18px 0; }
.card-type-name { font-size: 16px; font-weight: 800; color: #1e293b; margin-bottom: 4px; }
.classic-text  { color: #1d4ed8; }
.gold-text     { color: #92400e; }
.platinum-text { color: #374151; }
.card-type-desc { font-size: 12px; color: #64748b; margin-bottom: 12px; }
.card-perks { list-style: none; display: flex; flex-direction: column; gap: 6px; }
.card-perks li { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #475569; font-weight: 500; }
.card-perks li svg { width: 13px; height: 13px; color: #10b981; flex-shrink: 0; }

/* Status badge */
.card-status-badge { position: absolute; top: 12px; right: 12px; border-radius: 20px; padding: 5px 12px; font-size: 11px; font-weight: 700; display: flex; align-items: center; gap: 5px; }
.card-status-badge svg { width: 12px; height: 12px; }
.badge-approved { background: #16a34a; color: #fff; }
.badge-pending  { background: #d97706; color: #fff; }
.badge-rejected { background: #dc2626; color: #fff; }
.badge-selected { background: #2563eb; color: #fff; }
.badge-hidden   { display: none; }

/* Action panel */
.action-panel { display: flex; gap: 0; background: #fff; border: 1.5px solid #e2e8f0; border-radius: 16px; box-shadow: 0 2px 8px rgba(15,32,68,.06); overflow: hidden; }
.action-left  { flex: 1; min-width: 260px; padding: 28px; display: flex; flex-direction: column; gap: 16px; border-right: 1px solid #f1f5f9; }
.action-right { flex: 1.2; min-width: 300px; padding: 28px; }

.selected-label { font-size: 11px; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 4px; }
.selected-name  { font-size: 26px; font-weight: 900; }

.status-cta { display: flex; align-items: flex-start; gap: 10px; padding: 14px 16px; border-radius: 10px; font-size: 13px; font-weight: 600; }
.status-cta svg { width: 18px; height: 18px; flex-shrink: 0; margin-top: 1px; }
.approved-cta { background: #f0fdf4; color: #16a34a; }
.pending-cta  { background: #fffbeb; color: #92400e; }
.rejected-cta { background: #fff1f2; color: #dc2626; }
.note-text    { display: block; font-weight: 500; margin-top: 4px; font-style: italic; }

.request-btn { display: flex; align-items: center; justify-content: center; gap: 10px; padding: 13px 20px; border: none; border-radius: 10px; font-size: 14px; font-weight: 700; color: #fff; cursor: pointer; transition: opacity .18s, transform .18s; box-shadow: 0 4px 14px rgba(0,0,0,.2); }
.request-btn:disabled { opacity: .6; cursor: not-allowed; }
.request-btn:hover:not(:disabled) { opacity: .9; transform: translateY(-1px); }
.request-btn svg { width: 16px; height: 16px; }
.request-classic  { background: linear-gradient(135deg, #1a2f5e, #2563eb); }
.request-gold     { background: linear-gradient(135deg, #78350f, #d97706); }
.request-platinum { background: linear-gradient(135deg, #1e293b, #374151); }
.btn-spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,.3); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; }

.request-error { display: flex; align-items: center; gap: 8px; background: #fff1f2; border: 1px solid #fecaca; border-radius: 8px; padding: 10px 14px; color: #dc2626; font-size: 13px; }
.request-error svg { width: 16px; height: 16px; flex-shrink: 0; }

/* Card details section */
.details-section-head { display: flex; align-items: center; gap: 8px; font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 18px; }
.details-section-head svg { width: 15px; height: 15px; }

.detail-row { display: flex; align-items: center; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #f1f5f9; flex-wrap: wrap; gap: 8px; }
.detail-row:last-of-type { border-bottom: none; }
.detail-label { font-size: 13px; color: #64748b; min-width: 110px; }
.detail-value-wrap { display: flex; align-items: center; gap: 6px; }
.detail-value { font-size: 13px; font-weight: 600; color: #1e293b; }
.detail-value.mono { font-family: 'Courier New', monospace; letter-spacing: 1.5px; }

.cvv-value { font-size: 18px; letter-spacing: 4px; }
.cvv-timer { font-size: 10px; color: #94a3b8; font-weight: 500; }

.icon-btn { display: flex; align-items: center; justify-content: center; width: 28px; height: 28px; border: 1.5px solid #e2e8f0; border-radius: 6px; background: #f8fafc; color: #64748b; cursor: pointer; transition: all .15s; flex-shrink: 0; }
.icon-btn:hover { background: #eff6ff; border-color: #bfdbfe; color: #2563eb; }
.icon-btn svg { width: 13px; height: 13px; display: block; }
.copy-icon:hover { color: #16a34a; border-color: #bbf7d0; background: #f0fdf4; }

.network-badge { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; }
.net-classic  { background: #eff6ff; color: #1d4ed8; }
.net-gold     { background: #fffbeb; color: #92400e; }
.net-platinum { background: #f1f5f9; color: #374151; }

.security-note { display: flex; align-items: center; gap: 7px; margin-top: 16px; padding: 10px 14px; background: #fef9c3; border-radius: 8px; font-size: 11px; color: #854d0e; font-weight: 600; }
.security-note svg { width: 14px; height: 14px; flex-shrink: 0; }

/* Card block badge */
.card-block-badge { padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: 700; }
.card-block-badge.active-badge { background: #dcfce7; color: #16a34a; }
.card-block-badge.blocked      { background: #fee2e2; color: #dc2626; }

.block-btn { padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer; width: auto; height: auto; border: 1.5px solid; }
.block-btn.block   { background: #fef2f2; color: #dc2626; border-color: #fecaca; }
.block-btn.block:hover   { background: #fee2e2; }
.block-btn.unblock { background: #f0fdf4; color: #16a34a; border-color: #bbf7d0; }
.block-btn.unblock:hover { background: #dcfce7; }
.block-btn:disabled { opacity: .5; cursor: not-allowed; }

/* Card controls */
.controls-section { margin-top: 16px; padding: 14px; background: #f8fafc; border-radius: 10px; border: 1.5px solid #e2e8f0; }
.controls-head { font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 12px; }
.control-row { display: flex; align-items: center; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f1f5f9; }
.control-row:last-child { border-bottom: none; padding-bottom: 0; }
.control-name { font-size: 13px; font-weight: 600; color: #1e293b; }
.control-desc { font-size: 11px; color: #94a3b8; margin-top: 1px; }

/* Toggle switch */
.toggle-label { display: flex; align-items: center; cursor: pointer; }
.toggle-label input[type="checkbox"] { display: none; }
.toggle-track { width: 36px; height: 20px; background: #e2e8f0; border-radius: 10px; position: relative; transition: background .2s; flex-shrink: 0; }
.toggle-thumb { width: 14px; height: 14px; background: #fff; border-radius: 50%; position: absolute; top: 3px; left: 3px; transition: transform .2s; box-shadow: 0 1px 3px rgba(0,0,0,.2); }
.toggle-label input:checked + .toggle-track { background: #2563eb; }
.toggle-label input:checked + .toggle-track .toggle-thumb { transform: translateX(16px); }
.toggle-label input:disabled + .toggle-track { opacity: .4; cursor: not-allowed; }

.no-card-hint { display: flex; align-items: center; gap: 8px; margin-top: 16px; padding: 12px 14px; background: #f8fafc; border: 1.5px dashed #cbd5e1; border-radius: 10px; font-size: 13px; color: #94a3b8; font-weight: 500; }
.no-card-hint svg { width: 16px; height: 16px; flex-shrink: 0; }

/* History */
.history-title { font-size: 16px; font-weight: 700; color: #1e293b; margin-bottom: 14px; }
.history-table-wrap { background: #fff; border: 1.5px solid #e2e8f0; border-radius: 14px; overflow: hidden; }
.history-table { width: 100%; border-collapse: collapse; }
.history-table thead tr { background: #f8fafc; border-bottom: 2px solid #e2e8f0; }
.history-table th { padding: 12px 16px; font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: .6px; text-align: left; }
.history-table tbody tr { border-bottom: 1px solid #f1f5f9; }
.history-table tbody tr:last-child { border-bottom: none; }
.history-table td { padding: 12px 16px; font-size: 13px; }

.mono-cell { font-family: 'Courier New', monospace; font-size: 12px; color: #475569; }
.date-cell { color: #64748b; font-size: 12px; }
.note-cell { color: #64748b; font-style: italic; }
.muted     { color: #cbd5e1; }

.type-pill { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; }
.type-classic  { background: #eff6ff; color: #1d4ed8; }
.type-gold     { background: #fffbeb; color: #92400e; }
.type-platinum { background: #f1f5f9; color: #374151; }

.status-pill { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; }
.status-pending  { background: #fffbeb; color: #92400e; }
.status-approved { background: #f0fdf4; color: #16a34a; }
.status-rejected { background: #fff1f2; color: #dc2626; }

@keyframes spin { to { transform: rotate(360deg); } }
@media (max-width: 1100px) { .cards-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 700px)  { .cards-grid { grid-template-columns: 1fr; } .action-panel { flex-direction: column; } .action-left { border-right: none; border-bottom: 1px solid #f1f5f9; } }
</style>
