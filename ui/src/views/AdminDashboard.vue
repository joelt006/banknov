<template>
  <div class="admin-dashboard">

    <!-- KPI Cards -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-icon blue">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        </div>
        <div class="kpi-body">
          <div class="kpi-label">Total Customers</div>
          <div class="kpi-value">{{ stats.total_customers ?? '—' }}</div>
          <div class="kpi-sub">Registered users</div>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-icon green">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
        </div>
        <div class="kpi-body">
          <div class="kpi-label">Total Accounts</div>
          <div class="kpi-value">{{ totalAccounts }}</div>
          <div class="kpi-sub">Standard · Minor · Senior</div>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-icon indigo">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
        </div>
        <div class="kpi-body">
          <div class="kpi-label">Total Deposits</div>
          <div class="kpi-value">₹{{ formatAmount(stats.total_balance) }}</div>
          <div class="kpi-sub">Across all accounts</div>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-icon purple">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>
        </div>
        <div class="kpi-body">
          <div class="kpi-label">Total Transactions</div>
          <div class="kpi-value">{{ stats.total_transactions ?? '—' }}</div>
          <div class="kpi-sub">All time</div>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-icon red">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
        </div>
        <div class="kpi-body">
          <div class="kpi-label">Frozen Accounts</div>
          <div class="kpi-value">{{ stats.frozen_accounts ?? '0' }}</div>
          <div class="kpi-sub">Currently suspended</div>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-icon amber">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
        </div>
        <div class="kpi-body">
          <div class="kpi-label">Minor Accounts</div>
          <div class="kpi-value">{{ stats.total_minor_accounts ?? '—' }}</div>
          <div class="kpi-sub">Under 18</div>
        </div>
      </div>
    </div>

    <!-- Charts row -->
    <div class="charts-row">

      <!-- Daily transaction bar chart -->
      <div class="chart-card wide">
        <div class="chart-header">
          <div>
            <h3>Transaction Volume</h3>
            <p>Last 7 days</p>
          </div>
          <div class="legend">
            <span class="dot indigo"></span> Transactions per day
          </div>
        </div>
        <div class="bar-chart" v-if="stats.daily_chart">
          <div class="bars">
            <div class="bar-col" v-for="d in stats.daily_chart" :key="d.date">
              <div class="bar-wrap">
                <div class="bar-fill" :style="{ height: barHeight(d.count) + '%' }" :title="`${d.count} txns · ₹${d.amount}`">
                  <span class="bar-tip" v-if="d.count > 0">{{ d.count }}</span>
                </div>
              </div>
              <div class="bar-label">{{ d.date }}</div>
            </div>
          </div>
        </div>
        <div v-else class="chart-empty">No transaction data yet</div>
      </div>

      <!-- Account type breakdown -->
      <div class="chart-card">
        <div class="chart-header">
          <div>
            <h3>Account Types</h3>
            <p>Distribution</p>
          </div>
        </div>
        <div class="donut-wrap" v-if="stats.total_accounts !== undefined">
          <div class="donut" :style="donutStyle"></div>
          <div class="donut-center">
            <div class="donut-total">{{ totalAccounts }}</div>
            <div class="donut-lbl">Total</div>
          </div>
        </div>
        <div class="donut-legend">
          <div class="dl-row">
            <span class="dl-dot" style="background:#6366f1"></span>
            <span class="dl-label">Standard</span>
            <span class="dl-val">{{ stats.total_accounts ?? 0 }}</span>
          </div>
          <div class="dl-row">
            <span class="dl-dot" style="background:#8b5cf6"></span>
            <span class="dl-label">Minor</span>
            <span class="dl-val">{{ stats.total_minor_accounts ?? 0 }}</span>
          </div>
          <div class="dl-row">
            <span class="dl-dot" style="background:#f59e0b"></span>
            <span class="dl-label">Senior</span>
            <span class="dl-val">{{ stats.total_senior_accounts ?? 0 }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent transactions -->
    <div class="table-card">
      <div class="table-head">
        <div>
          <h3>Recent Transactions</h3>
          <p>Latest 10 transactions across all accounts</p>
        </div>
        <RouterLink to="/Admin/Accounts" class="view-btn">Manage Accounts →</RouterLink>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr><th>#</th><th>Sender</th><th>Receiver</th><th>Amount</th><th>Type</th><th>Status</th><th>Date</th></tr>
          </thead>
          <tbody>
            <tr v-if="recentTxns.length === 0">
              <td colspan="7" class="empty">No transactions yet</td>
            </tr>
            <tr v-for="t in recentTxns" :key="t.id">
              <td class="mono muted">#{{ t.id }}</td>
              <td class="muted small">{{ t.sender || '—' }}</td>
              <td class="muted small">{{ t.receiver || '—' }}</td>
              <td class="bold">₹{{ formatAmount(t.amount) }}</td>
              <td><span class="badge blue">{{ t.transaction_type }}</span></td>
              <td>
                <span class="badge" :class="t.status === 'Completed' ? 'green' : 'amber'">{{ t.status }}</span>
              </td>
              <td class="muted small">{{ formatDate(t.date) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<script>
import adminApiClient from '@/services/adminApiClient';

export default {
  name: 'AdminDashboard',
  data() {
    return { stats: {}, transactions: [], loading: true };
  },
  computed: {
    totalAccounts() {
      return (this.stats.total_accounts || 0) + (this.stats.total_minor_accounts || 0) + (this.stats.total_senior_accounts || 0);
    },
    recentTxns() { return this.transactions.slice(0, 10); },
    donutStyle() {
      const std = this.stats.total_accounts || 0;
      const min = this.stats.total_minor_accounts || 0;
      const sen = this.stats.total_senior_accounts || 0;
      const total = std + min + sen || 1;
      const s = (std / total) * 360;
      const m = (min / total) * 360;
      const sn = (sen / total) * 360;
      return {
        background: `conic-gradient(#6366f1 0deg ${s}deg, #8b5cf6 ${s}deg ${s + m}deg, #f59e0b ${s + m}deg ${s + m + sn}deg, #e2e8f0 ${s + m + sn}deg 360deg)`,
      };
    },
  },
  async created() {
    try {
      const [statsRes, txnRes] = await Promise.all([
        adminApiClient.get('/accounts/admin/stats/'),
        adminApiClient.get('/accounts/admin/transactions/'),
      ]);
      this.stats = statsRes.data;
      this.transactions = txnRes.data;
    } finally {
      this.loading = false;
    }
  },
  methods: {
    barHeight(count) {
      const max = Math.max(...(this.stats.daily_chart || []).map(d => d.count), 1);
      return count === 0 ? 2 : Math.max((count / max) * 100, 4);
    },
    formatAmount(v) {
      return parseFloat(v || 0).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },
    formatDate(d) {
      return new Date(d).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
    },
  },
};
</script>

<style scoped>
.admin-dashboard { display: flex; flex-direction: column; gap: 24px; }

/* KPI */
.kpi-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.kpi-card {
  background: #fff; border-radius: 16px; padding: 22px;
  display: flex; align-items: center; gap: 16px;
  border: 1px solid #e2e8f0; box-shadow: 0 1px 4px rgba(0,0,0,.04);
  transition: box-shadow .18s;
}
.kpi-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,.08); }
.kpi-icon { width: 52px; height: 52px; border-radius: 14px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.kpi-icon svg { width: 22px; height: 22px; }
.kpi-icon.blue   { background: #eff6ff; color: #2563eb; }
.kpi-icon.green  { background: #f0fdf4; color: #16a34a; }
.kpi-icon.indigo { background: #eef2ff; color: #6366f1; }
.kpi-icon.purple { background: #faf5ff; color: #7c3aed; }
.kpi-icon.red    { background: #fef2f2; color: #dc2626; }
.kpi-icon.amber  { background: #fffbeb; color: #d97706; }
.kpi-label { font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: .5px; }
.kpi-value { font-size: 26px; font-weight: 800; color: #0f172a; line-height: 1.2; }
.kpi-sub { font-size: 11px; color: #94a3b8; margin-top: 2px; }

/* Charts */
.charts-row { display: grid; grid-template-columns: 1fr 320px; gap: 20px; }
.chart-card {
  background: #fff; border-radius: 16px; padding: 24px;
  border: 1px solid #e2e8f0; box-shadow: 0 1px 4px rgba(0,0,0,.04);
}
.chart-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.chart-header h3 { font-size: 16px; font-weight: 700; color: #0f172a; }
.chart-header p { font-size: 12px; color: #94a3b8; margin-top: 2px; }
.legend { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #64748b; }
.dot { width: 10px; height: 10px; border-radius: 50%; }
.dot.indigo { background: #6366f1; }

/* Bar chart */
.bar-chart { height: 180px; }
.bars { display: flex; align-items: flex-end; gap: 8px; height: 100%; padding-bottom: 28px; position: relative; }
.bar-col { display: flex; flex-direction: column; align-items: center; flex: 1; height: 100%; }
.bar-wrap { flex: 1; display: flex; align-items: flex-end; width: 100%; }
.bar-fill {
  width: 100%; background: linear-gradient(180deg, #6366f1, #818cf8);
  border-radius: 6px 6px 0 0; position: relative; min-height: 3px;
  transition: height .4s ease;
}
.bar-tip {
  position: absolute; top: -22px; left: 50%; transform: translateX(-50%);
  font-size: 11px; font-weight: 700; color: #6366f1; white-space: nowrap;
}
.bar-label { font-size: 10px; color: #94a3b8; margin-top: 6px; white-space: nowrap; }
.chart-empty { display: flex; align-items: center; justify-content: center; height: 150px; color: #94a3b8; font-size: 14px; }

/* Donut */
.donut-wrap { position: relative; width: 130px; height: 130px; margin: 0 auto 20px; }
.donut {
  width: 130px; height: 130px; border-radius: 50%;
  mask: radial-gradient(farthest-side, transparent calc(100% - 22px), black calc(100% - 22px));
  -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 22px), black calc(100% - 22px));
}
.donut-center {
  position: absolute; inset: 0; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
}
.donut-total { font-size: 24px; font-weight: 800; color: #0f172a; }
.donut-lbl { font-size: 11px; color: #94a3b8; }
.donut-legend { display: flex; flex-direction: column; gap: 10px; }
.dl-row { display: flex; align-items: center; gap: 10px; }
.dl-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.dl-label { flex: 1; font-size: 13px; color: #475569; }
.dl-val { font-size: 13px; font-weight: 700; color: #0f172a; }

/* Table */
.table-card { background: #fff; border-radius: 16px; border: 1px solid #e2e8f0; overflow: hidden; }
.table-head {
  display: flex; justify-content: space-between; align-items: center;
  padding: 20px 24px; border-bottom: 1px solid #f1f5f9;
}
.table-head h3 { font-size: 16px; font-weight: 700; color: #0f172a; }
.table-head p { font-size: 12px; color: #94a3b8; margin-top: 2px; }
.view-btn { font-size: 13px; font-weight: 600; color: #6366f1; }
.view-btn:hover { text-decoration: underline; }
.table-wrap { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th { padding: 11px 16px; text-align: left; font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: .5px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; }
.data-table td { padding: 13px 16px; font-size: 13px; color: #1e293b; border-bottom: 1px solid #f8fafc; }
.data-table tr:last-child td { border-bottom: none; }
.data-table tr:hover td { background: #f8fafc; }
.mono { font-family: 'Courier New', monospace; }
.muted { color: #64748b; }
.small { font-size: 12px; }
.bold { font-weight: 700; }
.empty { text-align: center; color: #94a3b8; padding: 32px !important; }

.badge { padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; }
.badge.blue  { background: #eff6ff; color: #2563eb; }
.badge.green { background: #f0fdf4; color: #16a34a; }
.badge.amber { background: #fffbeb; color: #d97706; }

@media (max-width: 1100px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 900px) { .charts-row { grid-template-columns: 1fr; } }
@media (max-width: 640px) { .kpi-grid { grid-template-columns: 1fr 1fr; } }
</style>
