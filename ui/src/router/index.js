import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/Register', name: 'Register', component: () => import('../views/Register.vue') },
    { path: '/Login', name: 'Login', component: () => import('../views/Login.vue') },
    { path: '/ForgotPassword', name: 'ForgotPassword', component: () => import('../views/ForgotPassword.vue') },
    { path: '/VerifyOtp', name: 'VerifyOtp', component: () => import('../views/VerifyOtp.vue') },
    { path: '/CreateAccountoption', name: 'CreateAccountoption', component: () => import('../views/CreateAccountoption.vue') },
    { path: '/CreateBankAccount', name: 'CreateBankAccount', component: () => import('../views/CreateBankAccount.vue') },
    { path: '/CreateBankAccountSenior', name: 'CreateBankAccountSenior', component: () => import('../views/CreateBankAccountSenior.vue') },
    { path: '/CreateBankAccountMinor', name: 'CreateBankAccountMinor', component: () => import('../views/CreateBankAccountMinor.vue') },
    { path: '/Dashboard', name: 'Dashboard', meta: { requiresAuth: true }, component: () => import('../views/Dashboard.vue') },
    { path: '/Profile', name: 'Profile', meta: { requiresAuth: true }, component: () => import('../views/Profile.vue') },
    { path: '/EditProfile', name: 'EditProfile', meta: { requiresAuth: true }, component: () => import('../views/EditProfile.vue') },
    { path: '/Security', name: 'Security', meta: { requiresAuth: true }, component: () => import('../views/Security.vue') },
    { path: '/TransactionStatement', name: 'TransactionStatement', meta: { requiresAuth: true }, component: () => import('../views/TransactionStatement.vue') },
    { path: '/SendMoney', name: 'SendMoney', meta: { requiresAuth: true }, component: () => import('../views/SendMoney.vue') },
    { path: '/DepositMoney', redirect: '/Dashboard' },
    { path: '/MyCards', name: 'MyCards', meta: { requiresAuth: true }, component: () => import('../views/MyCards.vue') },
    { path: '/AccountDetails', name: 'AccountDetails', meta: { requiresAuth: true }, component: () => import('../views/AccountDetails.vue') },
    { path: '/Beneficiaries', name: 'Beneficiaries', meta: { requiresAuth: true }, component: () => import('../views/Beneficiaries.vue') },
    { path: '/ScheduledTransfers', name: 'ScheduledTransfers', meta: { requiresAuth: true }, component: () => import('../views/ScheduledTransfers.vue') },
    { path: '/Loans', name: 'Loans', meta: { requiresAuth: true }, component: () => import('../views/Loans.vue') },
    { path: '/FixedDeposits', name: 'FixedDeposits', meta: { requiresAuth: true }, component: () => import('../views/FixedDeposits.vue') },
    { path: '/Notifications', name: 'Notifications', meta: { requiresAuth: true }, component: () => import('../views/Notifications.vue') },
    { path: '/Support', name: 'Support', meta: { requiresAuth: true }, component: () => import('../views/Support.vue') },
    // Admin portal (separate auth)
    { path: '/AdminLogin', name: 'AdminLogin', component: () => import('../views/AdminLogin.vue') },
    { path: '/Admin/Dashboard', name: 'AdminDashboard', meta: { isAdmin: true }, component: () => import('../views/AdminDashboard.vue') },
    { path: '/Admin/Accounts', name: 'AdminAccounts', meta: { isAdmin: true }, component: () => import('../views/AdminAccounts.vue') },
    { path: '/Admin/CardRequests', name: 'AdminCardRequests', meta: { isAdmin: true }, component: () => import('../views/AdminCardRequests.vue') },
    { path: '/Admin/Loans', name: 'AdminLoans', meta: { isAdmin: true }, component: () => import('../views/AdminLoans.vue') },
    { path: '/Admin/Support', name: 'AdminSupport', meta: { isAdmin: true }, component: () => import('../views/AdminSupport.vue') },
  ]
})

router.beforeEach((to, from, next) => {
  if (to.meta.isAdmin) {
    const adminToken = localStorage.getItem('adminToken')
    if (!adminToken) return next({ name: 'AdminLogin' })
  } else if (to.meta.requiresAuth) {
    const token = localStorage.getItem('token')
    if (!token) return next({ name: 'Login' })
  }
  next()
})

export default router
