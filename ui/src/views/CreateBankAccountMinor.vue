<template>
    <div class="create-bank-account-minor">
      <h2>Create Bank Account for Minor</h2>
      <form @submit.prevent="submitForm">
        <div>
        <label for="accountHolderName">Account Holder Name</label>
        <input type="text" id="accountHolderName" v-model="accountHolderName" name="accountHolderName" required />
      </div>
      <div>
        <label for="guardian_name">Guardian Name</label>
        <input type="text" id="guardian_name" v-model="guardian_name" name="guardian_name" required />
      </div>
      <div>
        <label for="dateOfBirth">Date of Birth</label>
        <input type="date" id="dateOfBirth" v-model="dateOfBirth" name="dateOfBirth" required />
      </div>
      <div>
        <label for="currentAddress">Current Address</label>
        <textarea id="currentAddress" v-model="currentAddress" name="currentAddress" required></textarea>
      </div>
      <div>
        <label for="permanentAddress">Permanent Address</label>
        <input type="text" id="permanentAddress" v-model="permanentAddress" name="permanentAddress" required />
      </div>
      <div>
        <label for="sex">Sex</label>
        <input type="text" id="sex" v-model="sex" name="sex" required />
      </div>
      <div>
        <label for="annualIncome">Annual Income</label>
        <input type="number" id="annualIncome" v-model="annualIncome" name="annualIncome" required />
      </div>
      <div>
        <label for="occupation">Occupation</label>
        <input type="text" id="occupation" v-model="occupation" name="occupation" />
      </div>
      <div>
        <label for="country">Country</label>
        <input type="text" id="country" v-model="country" name="country" required />
      </div>
      <div>
        <label for="state">State</label>
        <input type="text" id="state" v-model="state" name="state" required />
      </div>
      <div>
        <label for="city">City</label>
        <input type="text" id="city" v-model="city" name="city" required />
      </div>
      <div>
        <label for="street">Street</label>
        <input type="text" id="street" v-model="street" name="street" required />
      </div>
      <div>
        <label for="pincode">Pincode</label>
        <input type="text" id="pincode" v-model="pincode" name="pincode" required />
      </div>
      <div>
        <label for="phoneNumber">Phone Number</label>
        <input type="text" id="phoneNumber" v-model="phoneNumber" name="phoneNumber" required />
      </div>
      <div>
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" name="email" />
      </div>
      <div>
        <label for="aadharNumber">Aadhar Number</label>
        <input type="text" id="aadharNumber" v-model="aadharNumber" name="aadharNumber" />
      </div>
      <div>
        <label for="passportNumber">Passport Number</label>
        <input type="text" id="passportNumber" v-model="passportNumber" name="passportNumber" />
      </div>
      <div>
        <label for="voterIdNumber">Voter ID Number</label>
        <input type="text" id="voterIdNumber" v-model="voterIdNumber" name="voterIdNumber" />
      </div>
      <div>
        <label for="panCardNumber">PAN Card Number</label>
        <input type="text" id="panCardNumber" v-model="panCardNumber" name="panCardNumber" />
      </div>
      <div>
        <label for="photo">Photo</label>
        <input type="file" id="photo" @change="onFileChange" name="photo" />
      </div>
      <button type="submit">Create Account</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'CreateBankAccountMinor',
    data() {
      return {
      accountHolderName: '',
      guardian_name:'',
      dateOfBirth: '',
      currentAddress: '',
      permanentAddress: '',
      sex: '',
      annualIncome: 0,
      occupation: '',
      country: 'India',
      state: 'Kerala',
      city: 'Delhi',
      street: 'Main Lane',
      pincode: '123456',
      phoneNumber: '',
      email: '',
      aadharNumber: '',
      passportNumber: '',
      voterIdNumber: '',
      panCardNumber: '',
      photo: null,
      message: ''
    };
    },
    methods: {
      async submitForm() {
        try {
          await axios.post('http://127.0.0.1:8000/accounts/CreateBankAccountForMinor/', this.form);
          this.$router.push('/profile');
        } catch (err) {
          console.error(err);
          this.error = 'Failed to create bank account for minor.';
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .create-bank-account-minor {
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
  