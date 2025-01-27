<template>
    <div class="edit-profile">
      <h2>Edit Profile</h2>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="job">Job</label>
          <input type="text" id="job" v-model="form.job" />
        </div>
        <div class="form-group">
          <label for="income">Income</label>
          <input type="number" id="income" v-model="form.income" />
        </div>
        <div class="form-group">
          <label for="address">Address</label>
          <input type="text" id="address" v-model="form.address" />
        </div>
        <div v-if="error" class="error">
          {{ error }}
        </div>
        <button type="submit">Save Changes</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'EditProfile',
    setup() {
      const form = ref({
        job: '',
        income: '',
        address: '',
      });
      const error = ref('');
      const router = useRouter();
  
      const fetchProfile = async () => {
        try {
          const response = await axios.get('/api/profile/', {
            headers: {
              Authorization: `Token ${localStorage.getItem('token')}`,
            },
          });
          form.value.job = response.data.job || '';
          form.value.income = response.data.income || '';
          form.value.address = response.data.address || '';
        } catch (err) {
          console.error(err);
          error.value = 'Failed to fetch profile data.';
        }
      };
  
      const submitForm = async () => {
        try {
          await axios.post('/api/edit-profile/', form.value, {
            headers: {
              Authorization: `Token ${localStorage.getItem('token')}`,
            },
          });
          router.push('/profile');
        } catch (err) {
          console.error(err);
          error.value = 'Failed to update profile.';
        }
      };
  
      fetchProfile();
  
      return {
        form,
        error,
        submitForm,
      };
    },
  };
  </script>
  
  <style scoped>
  .edit-profile {
    max-width: 600px;
    margin: 0 auto;
  }
  
  .form-group {
    margin-bottom: 1em;
  }
  
  .error {
    color: red;
    margin-bottom: 1em;
  }
  </style>
  