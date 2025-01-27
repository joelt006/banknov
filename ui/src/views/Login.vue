<template>
  <div class="login-container">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Username:</label>
        <input 
          type="text" 
          id="username" 
          v-model="username" 
          required 
        />
      </div>
      <div>
        <label for="password">Password:</label>
        <input 
          type="password" 
          id="password" 
          v-model="password" 
          required 
        />
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
    async handleLogin() {
      try {

        const csrfToken = document.cookie
          .split('; ')
          .find(row => row.startsWith('csrftoken'))
          ?.split('=')[1];

        const response = await axios.post(
          'http://127.0.0.1:8000/accounts/login/',
          {
            username: this.username,
            password: this.password,
          },
          {
            headers: { 'X-CSRFToken': csrfToken },
            withCredentials: true, 
          }
        );

        if (response.status === 200) {
          alert(response.data.message); 
          this.errorMessage = '';
          this.$router.push('/dashboard'); // Example route
        }
      } catch (error) {
        // Handle error
        if (error.response && error.response.status === 401) {
          this.errorMessage = 'Invalid username or password.';
        } else {
          this.errorMessage = 'An error occurred. Please try again.';
          console.error('Login error:', error);
        }
      }
    },
  },
};
</script>

<style>
.login-container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.login-container h1 {
  text-align: center;
}

.login-container .error {
  color: red;
  text-align: center;
  margin-top: 10px;
}
</style>


