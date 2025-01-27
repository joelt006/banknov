<template>
    <div>
      <h1>Choose Account Type</h1>
      <ul>
       <li><RouterLink to="/CreateBankAccount">CreateBankAccount</RouterLink></li>
       <li><RouterLink to="/CreateBankAccountMinor">CreateBankAccountMinor</RouterLink></li>
       <li><RouterLink to="/CreateBankAccountSenior">CreateBankAccountSenior</RouterLink></li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CreateAccountOptions'
  }
  </script>
  