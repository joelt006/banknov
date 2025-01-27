import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
      
    {
      path: '/Register',
      name: 'Register',
     
      component: () => import('../views/Register.vue')
    },
    {
      path: '/Login',
      name: 'Login',
     
      component: () => import('../views/Login.vue')
    },
    {
      path: '/CreateBankAccount',
      name: 'CreateBankAccount',
     
      component: () => import('../views/CreateBankAccount.vue')
    },
    {
      path: '/CreateBankAccountSenior',
      name: 'CreateBankAccountSenior',
     
      component: () => import('../views/CreateBankAccountSenior.vue')
    },
    {
      path: '/CreateBankAccountMinor',
      name: 'CreateBankAccountMinor',
     
      component: () => import('../views/CreateBankAccountMinor.vue')
    },
    {
      path: '/CreateAccountoption',
      name: 'CreateAccountoption',
     
      component: () => import('../views/CreateAccountoption.vue')
    },
  
    {
      path: '/VerifyOtp',
      name: 'VerifyOtp',
     
      component: () => import('../views/VerifyOtp.vue')
    },
    {
      path:'/Dashboard',
      name: 'Dashboard',
      component:()  => import('../views/Dashboard.vue')
    },  
    {
      path: '/Profile',
      name: 'Profile',
     
      component: () => import('../views/Profile.vue')
    },
    {
      path: '/TransactionStatement',
      name: 'TransactionStatement',
     
      component: () => import('../views/TransactionStatement.vue')
    },
    {
      path: '/SendMoney',
      name: 'SendMoney',
     
      component: () => import('../views/SendMoney.vue')
    },
    {
      path: '/DepositMoney',
      name: 'DepositMoney',
     
      component: () => import('../views/DepositMoney.vue')
    }
  ]
})

export default router
