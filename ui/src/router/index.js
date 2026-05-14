import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/Register', name: 'Register', component: () => import('../views/Register.vue') },
    { path: '/Login', name: 'Login', component: () => import('../views/Login.vue') },
    { path: '/VerifyOtp', name: 'VerifyOtp', component: () => import('../views/VerifyOtp.vue') },
    { path: '/CreateAccountoption', name: 'CreateAccountoption', component: () => import('../views/CreateAccountoption.vue') },
    { path: '/CreateBankAccount', name: 'CreateBankAccount', component: () => import('../views/CreateBankAccount.vue') },
    { path: '/CreateBankAccountSenior', name: 'CreateBankAccountSenior', component: () => import('../views/CreateBankAccountSenior.vue') },
    { path: '/CreateBankAccountMinor', name: 'CreateBankAccountMinor', component: () => import('../views/CreateBankAccountMinor.vue') },
    { path: '/Dashboard', name: 'Dashboard', meta: { requiresAuth: true }, component: () => import('../views/Dashboard.vue') },
    { path: '/Profile', name: 'Profile', meta: { requiresAuth: true }, component: () => import('../views/Profile.vue') },
    { path: '/EditProfile', name: 'EditProfile', meta: { requiresAuth: true }, component: () => import('../views/EditProfile.vue') },
    { path: '/TransactionStatement', name: 'TransactionStatement', meta: { requiresAuth: true }, component: () => import('../views/TransactionStatement.vue') },
    { path: '/SendMoney', name: 'SendMoney', meta: { requiresAuth: true }, component: () => import('../views/SendMoney.vue') },
    { path: '/DepositMoney', name: 'DepositMoney', meta: { requiresAuth: true }, component: () => import('../views/DepositMoney.vue') },
    { path: '/MyCards', name: 'MyCards', meta: { requiresAuth: true }, component: () => import('../views/MyCards.vue') },
    { path: '/BankAdmin', name: 'BankAdmin', meta: { requiresAuth: true }, component: () => import('../views/BankAdmin.vue') },
    // Admin portal (separate auth)
    { path: '/AdminLogin', name: 'AdminLogin', component: () => import('../views/AdminLogin.vue') },
    { path: '/Admin/Dashboard', name: 'AdminDashboard', meta: { isAdmin: true }, component: () => import('../views/AdminDashboard.vue') },
    { path: '/Admin/Accounts', name: 'AdminAccounts', meta: { isAdmin: true }, component: () => import('../views/AdminAccounts.vue') },
    { path: '/Admin/CardRequests', name: 'AdminCardRequests', meta: { isAdmin: true }, component: () => import('../views/AdminCardRequests.vue') },
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
