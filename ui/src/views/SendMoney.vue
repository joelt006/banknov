<template>
  <div class="send-money">
    <h1>Send Money</h1>
    <form @submit.prevent="sendMoney" class="form">
      <div class="form-group">
        <label for="recipientAccount">Recipient Account:</label>
        <input 
          type="text" 
          v-model="recipientAccount" 
          id="recipientAccount" 
          required 
          placeholder="Enter recipient account number" 
        />
      </div>
      <div class="form-group">
        <label for="amount">Amount:</label>
        <input 
          type="number" 
          v-model="amount" 
          id="amount" 
          required 
          min="0.01" 
          step="0.01" 
          placeholder="Enter amount to send" 
        />
      </div>
      <button type="submit" class="btn">Send</button>
    </form>
    <p v-if="message" :class="{'success-message': isSuccess, 'error-message': !isSuccess}">
      {{ message }}
    </p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      recipientAccount: '',
      amount: null,
      message: '',
      isSuccess: false,
    };
  },
  methods: {
    async sendMoney() {
      try {
        const response = await axios.post(
          'http://127.0.0.1:8000/transactions/send-money/',
          {
            recipient_account_number: this.recipientAccount,
            amount: this.amount,
          },
          { withCredentials: true }
        );
        this.message = response.data.message || 'Transaction successful!';
        this.isSuccess = true;
      } catch (error) {
        this.message = error.response?.data?.error || 'Transaction failed';
        this.isSuccess = false;
        console.error('Error sending money:', error);
      }
    },
  },
};
</script>

<style scoped>
.send-money {
  padding: 20px;
  text-align: center;
}

.form {
  margin: 0 auto;
  max-width: 300px;
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.btn {
  padding: 10px 15px;
  background-color: blue;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 16px;
}

.btn:hover {
  background-color: darkblue;
}

.success-message {
  color: green;
  margin-top: 20px;
}

.error-message {
  color: red;
  margin-top: 20px;
}
</style>
