<template>
  <div>
    <h2>Profile</h2>
    <form @submit.prevent="updateProfile">
      <label for="account_holder_name">Account Holder Name:</label>
      <input type="text" v-model="profile.account_holder_name" required /><br />
      <label for="date_of_birth">Date of Birth:</label>
      <input type="date" v-model="profile.date_of_birth" required /><br />
      <label for="current_address">Current Address:</label>
      <input type="text" v-model="profile.current_address" required /><br />
      <label for="permanent_address">Permanent Address:</label>
      <input type="text" v-model="profile.permanent_address" required /><br />
      <label for="sex">Sex:</label>
      <input type="text" v-model="profile.sex" required /><br />
      <label for="annual_income">Annual Income:</label>
      <input type="number" v-model="profile.annual_income" required /><br />
      <label for="occupation">Occupation:</label>
      <input type="text" v-model="profile.occupation" required /><br />
      <label for="country">Country:</label>
      <input type="text" v-model="profile.country" required /><br />
      <label for="state">State:</label>
      <input type="text" v-model="profile.state" required /><br />
      <label for="city">City:</label>
      <input type="text" v-model="profile.city" required /><br />
      <label for="street">Street:</label>
      <input type="text" v-model="profile.street" required /><br />
      <label for="pincode">Pincode:</label>
      <input type="number" v-model="profile.pincode" required /><br />
      <label for="phone_number">Phone Number:</label>
      <input type="text" v-model="profile.phone_number" required /><br />
      <label for="email">Email:</label>
      <input type="email" v-model="profile.email" required /><br />
      <label for="aadhar_number">Aadhar Number:</label>
      <input type="text" v-model="profile.aadhar_number" required /><br />
      <label for="passport_number">Passport Number:</label>
      <input type="text" v-model="profile.passport_number" required /><br />
      <label for="voter_id_number">Voter ID Number:</label>
      <input type="text" v-model="profile.voter_id_number" required /><br />
      <label for="pan_card_number">PAN Card Number:</label>
      <input type="text" v-model="profile.pan_card_number" required /><br />
      <button type="submit">Update Profile</button>
    </form>
    <p v-if="message">{{ message }}</p>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios';
import router from '@/router';

export default {
  data() {
    return {
      profile: {
        account_holder_name: '',
        date_of_birth: '',
        current_address: '',
        permanent_address: '',
        sex: '',
        annual_income: '',
        occupation: '',
        country: '',
        state: '',
        city: '',
        street: '',
        pincode: '',
        phone_number: '',
        email: '',
        aadhar_number: '',
        passport_number: '',
        voter_id_number: '',
        pan_card_number: ''
      },
      message: '',
      error: ''
    };
  },
  async created() {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://127.0.0.1:8000/accounts/profile/', {
        headers: {
          'Authorization': `Token ${token}`
        }
      });
      this.profile = response.data.bank_account;
    } catch (error) {
      this.error = error.response.data.error;
      if (error.response.status === 401) {
        router.push('/login');
      }
    }
  },
  methods: {
    async updateProfile() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.put('http://127.0.0.1:8000/accounts/profile/', this.profile, {
          headers: {
            'Authorization': `Token ${token}`
          }
        });
        this.message = response.data.message;
      } catch (error) {
        this.error = error.response.data.error;
      }
    }
  }
};
</script>

