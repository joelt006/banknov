<!-- 
<template>
  <div class="dashboard">
    <h1>Welcome, {{ username }}</h1>
    <p>Your balance: {{ balance }}</p>
    <div class="links">
      <router-link to="/SendMoney">Send Money</router-link>
      <router-link to="/DepositMoney">Deposit Money</router-link>
      <router-link to="/TransactionStatement">Transaction Statement</router-link>
      <router-link to="/profile">Profile</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      balance: '0.00',
    };
  },
  async created() {
    try {
      const [userResponse, balanceResponse] = await Promise.all([
        axios.get('http://127.0.0.1:8000/accounts/user', {
          withCredentials: true, 
        }),
        axios.get('http://127.0.0.1:8000/accounts/balance', {
          withCredentials: true, 
        }),
      ]);

      if (userResponse?.data?.username) {
        this.username = userResponse.data.username;
      } else {
        console.error('Unexpected user response structure:', userResponse);
        this.username = 'Guest'; 
      }

      if (balanceResponse?.data?.balance) {
        this.balance = balanceResponse.data.balance;
      } else {
        console.error('Unexpected balance response structure:', balanceResponse);
        this.balance = '0.00';
      }
    } catch (error) {
      console.error('Error fetching user info or balance:', error);
      if (error.response) {
        console.error('Server responded with:', error.response.data);
      } else {
        console.error('Request error:', error.message);
      }
    }
  },
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.links {
  margin-top: 20px;
}

.links a {
  margin-right: 10px;
  text-decoration: none;
  color: blue;
}
</style>


<style>
.dashboard {
  text-align: center;
}

.links {
  margin-top: 20px;
}

.links a {
  display: block;
  margin: 10px 0;
}
</style> -->


<template>
  <div class="dashboard">
    <h1>Welcome, {{ username }}</h1>
    <p>Your balance: {{ balance }}</p>
    <div class="links">
      <router-link to="/SendMoney">Send Money</router-link>
      <router-link to="/DepositMoney">Deposit Money</router-link>
      <router-link to="/TransactionStatement">Transaction Statement</router-link>
      <router-link to="/profile">Profile</router-link>
      <button @click="logout" class="logout-button">Logout</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      balance: '0.00',
    };
  },
  async created() {
    try {
      const [userResponse, balanceResponse] = await Promise.all([
        axios.get('http://127.0.0.1:8000/accounts/user', {
          withCredentials: true,
        }),
        axios.get('http://127.0.0.1:8000/accounts/balance', {
          withCredentials: true,
        }),
      ]);

      if (userResponse?.data?.username) {
        this.username = userResponse.data.username;
      } else {
        console.error('Unexpected user response structure:', userResponse);
        this.username = 'Guest'; 
      }

      if (balanceResponse?.data?.balance) {
        this.balance = balanceResponse.data.balance;
      } else {
        console.error('Unexpected balance response structure:', balanceResponse);
        this.balance = '0.00';
      }
    } catch (error) {
      console.error('Error fetching user info or balance:', error);
      if (error.response) {
        console.error('Server responded with:', error.response.data);
      } else {
        console.error('Request error:', error.message);
      }
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('authToken');  // Example of removing token from local storage
      sessionStorage.removeItem('authToken'); // Example for session storage
      document.cookie = 'authToken=; Max-Age=-99999999'; // Example for clearing a cookie

      // Redirect to login page
      this.$router.push('/login');
    },
  },
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.links {
  margin-top: 20px;
}

.links a {
  margin-right: 10px;
  text-decoration: none;
  color: blue;
}

.logout-button {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #0013e6;
  color: rgb(10, 10, 10);
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.logout-button:hover {
  background-color: #0013e6;
}
</style>

<style>
.dashboard {
  text-align: center;
}

.links {
  margin-top: 20px;
}

.links a {
  display: block;
  margin: 10px 0;
}
</style>

