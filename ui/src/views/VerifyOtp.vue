<template>
  <div>
    <h2>Verify OTP</h2>
    <form @submit.prevent="verifyOTP">
      <label for="email">Email:</label>
      <input type="email" v-model="email" required /><br />
      
      <label for="otp">OTP:</label>
      <input type="text" v-model="otp" required /><br />
      
      <button type="submit">Verify OTP</button>
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
      email: '',
      otp: '',
      message: '',
      error: ''
    };
  },
  methods: {
    async verifyOTP() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/accounts/verify_otp/', {
          email: this.email,
          otp: this.otp
        });
        
        this.message = response.data.message;
        this.error = '';
      } catch (error) {
        this.error = error.response?.data?.error || 'An error occurred';
        this.message = '';   
      }
    }
  }
};
</script>

<style>
</style>
