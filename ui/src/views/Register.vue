<template>
  <div>
    <h2>Register</h2>
    <form @submit.prevent="register">
      <label for="username">Username:</label>
      <input type="text" v-model="username" required /><br />
      <label for="email">Email:</label>
      <input type="email" v-model="email" required /><br />
      <label for="password">Password:</label>
      <input type="password" v-model="password" required /><br />
      <label for="account_number">Account Number:</label>
      <input type="text" v-model="accountNumber" required /><br />
      <button type="submit">Register</button>
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
      username: '',
      email: '',
      password: '',
      accountNumber: '',
      message: '',
      error: ''
    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/accounts/register/', {
          username: this.username,
          email: this.email,
          password: this.password,
          account_number: this.accountNumber
        });
        if (response.data.isOTPSent) {
          this.message = response.data.message;
          this.$router.push('/VerifyOtp');
        } else {
          this.message = 'Registration successful, but OTP was not sent.';
        }
      } catch (error) {
        this.error = error.response?.data?.error || 'An error occurred during registration.';
      }
    }
  }
};
</script>
