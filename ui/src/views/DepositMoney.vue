<template>
    <div>
      <h2>Deposit Money</h2>
      <form @submit.prevent="depositMoney">
        <label for="account_number">Account Number:</label>
        <input type="text" v-model="accountNumber" required /><br />
        <label for="amount">Amount:</label>
        <input type="number" v-model="amount" required /><br />
        <button type="submit">Deposit Money</button>
      </form>
      <p v-if="message">{{ message }}</p>
      <p v-if="error">{{ error }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        accountNumber: '',
        amount: '',
        message: '',
        error: ''
      };
    },
    methods: {
      async depositMoney() {
        try {
          const response = await axios.post('http://127.0.0.1:8000/transactions/deposit-money/', {
            account_number: this.accountNumber,
            amount: this.amount
          }, {
            headers: {
              'Authorization': `Token ${localStorage.getItem('token')}`
            }
          });
          this.message = `Deposit successful! New balance: ${response.data.new_balance}`;
        } catch (error) {
          this.error = error.response ? error.response.data.error : 'An error occurred';
        }
      }
    }
  };
  </script>
  
  <style>
  </style>
  